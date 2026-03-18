import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder
from hashlib import sha256

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from typing import List
from Repositories.vector_store_repository import VectorStoreRepository
from config.settings import settings


class RetrievalService:
    """
        RAG的检索器
        执行流程：
        1. LLM对用户的query进行改写，生成多个类似的问题（多查询）
        2. 根据多路问题分别检索向量库，合并文档并去重（初筛召回）
        3. 利用 Reranker (重排序模型) 对召回的文档进行精准打分，保留最相关的 Top-K (精排过滤)
    """

    def __init__(self, k: int):
        self.chroma_vector = VectorStoreRepository()
        self.retriever = self.chroma_vector.vector_database.as_retriever(search_type="similarity",
                                                                         search_kwargs={"k": k * 3})
        self.k = k
        self.llm = ChatOpenAI(
            model=settings.MODEL,
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
            temperature=0.0
        )

        reranker_model_name = "BAAI/bge-reranker-large"
        logger.info(f"正在直接加载底层 CrossEncoder 模型: {reranker_model_name}...")
        # 直接实例化 sentence-transformers 的交叉编码器
        self.rerank_model = CrossEncoder(reranker_model_name, max_length=512)

    def format_docs(self, docs: List[Document]):
        return '\n\n'.join(doc.page_content for doc in docs)

    def get_unique_docs(self, docs: list[list[Document]]) -> list[Document]:
        """
        文档去重函数
        去除多个文档列表中的重复文档

        Args:
            docs (list[list[Document]]): 多个文档列表

        Returns:
            list[Document]: 去重后的文档列表
        """
        seen = set()
        unique_docs = []
        for docs_list in docs:
            for doc in docs_list:
                key = sha256(doc.page_content.encode("utf-8")).hexdigest()
                if key not in seen:
                    unique_docs.append(doc)
                    seen.add(key)
        return unique_docs

    def custom_rerank_documents(self, query: str, documents: List[Document], top_n: int) -> List[Document]:
        """
        原生手写的重排序函数
        """
        if not documents:
            return []

        # 1. 构造传入 CrossEncoder 的对：[[query, doc1], [query, doc2], ...]
        sentence_pairs = [[query, doc.page_content] for doc in documents]

        # 2. 直接进行推理打分 (返回的是一个包含分数的列表)
        scores = self.rerank_model.predict(sentence_pairs)

        # 3. 将文档和分数打包在一起: [(doc1, score1), (doc2, score2), ...]
        doc_score_pairs = list(zip(documents, scores))

        # 4. 根据分数从高到低排序
        doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

        # 5. 提取排名前 top_n 的文档并返回
        reranked_docs = [doc for doc, score in doc_score_pairs[:top_n]]

        # 打印调试信息，你可以直观看到分数
        for rank, (doc, score) in enumerate(doc_score_pairs[:top_n]):
            logger.info(f"重排序 Rank {rank + 1} - 分数: {score:.4f}")

        return reranked_docs

    def rephrase_retriever(self, multi_query_num: int, query: str) -> list[Document]:
        # 1、多查询提示模板
        multi_query_prompt = PromptTemplate.from_template(
            """
            你是一名AI语言模型助理。你的任务是生成给定问题的{query_num}个不同版本，以从矢量数据库中检索相关文档。
            你需要通过从多个视角生成问题，来克服基于距离的相似性搜索的一些局限性。请使用换行符分隔备选问题。

            原始问题：{query}
            """
        )
        # 2、多查询链
        expend_query_chain = (
                multi_query_prompt
                | self.llm
                | StrOutputParser()
        )

        multi_query_chain = (
                {
                    'query_num': lambda x: x['query_num'],
                    'query': lambda x: x['query']
                }  # 添加一个参数，用于控制生成多少个查询
                | expend_query_chain  # 生成多个查询
                | (lambda x: x + '\n' + query)
                | (lambda x: [self.retriever.invoke(q) for q in x.split('\n') if q.strip()])  # 遍历检索多个查询
                | self.get_unique_docs  # 文档去重
        )

        unique_docs = multi_query_chain.invoke({'query': query, 'query_num': multi_query_num})

        final_docs = self.custom_rerank_documents(query=query, documents=unique_docs, top_n=self.k)

        return final_docs


if __name__ == '__main__':
    retrieval_service = RetrievalService(k=5)
    r = retrieval_service.rephrase_retriever(3, "如何使用U盘安装Windows7")
    for i in r:
        print(i.page_content)
