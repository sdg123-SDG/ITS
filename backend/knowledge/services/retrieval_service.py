import logging
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel, RunnableLambda
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
        2、使用HyDE对query进行假设性的生成，以弥补原query和文档之间的差异
        3. 根据多路问题分别检索向量库，合并文档并去重（初筛召回）
        4. 利用 Reranker (重排序模型) 对召回的文档进行精准打分，保留最相关的 Top-K (精排过滤)
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

        reranker_model_name = 'C:/Users/sdg17/.cache/huggingface/hub/models--BAAI--bge-reranker-large/snapshots/55611d7bca2a7133960a6d3b71e083071bbfc312'
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
        重排序函数
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
            你需要通过从多个视角生成问题，来克服基于距离的相似性搜索的一些局限性。请将备选问题汇总在列表中，每个备选问题之间使用逗号间隔开。

            原始问题：{query}
            """
        )
        # 2、多查询链
        expend_query_chain = (
                multi_query_prompt
                | self.llm
                | StrOutputParser()
        )
        # 3、HyDE提示模板
        hyde_prompt = PromptTemplate.from_template(
            """
            请根据常识和推理，为问题编写一段看起来合理且详细的回答性段落，哪怕你不确定真实答案。

            问题：{query}
            """
        )
        # 4、假设生成链
        hyde_chain = (
           hyde_prompt
           | self.llm
           | StrOutputParser()
        )
        # 并行执行：同时生成 多查询 + HyDE答案
        parallel_chain = RunnableParallel(
            queries=expend_query_chain,
            hyde=hyde_chain
        )

        multi_query_chain = (
                RunnableLambda(lambda x: {"query_num": multi_query_num, "query": query})
                | parallel_chain
                # 合并为最终检索列表：N个问题 + 1个答案 + 原始问题（全覆盖）
                | RunnableLambda(lambda x: [q.strip() for q in x["queries"].split(",") if q.strip()] + [x["hyde"], query])
                # 多路检索
                | RunnableLambda(lambda x: self.retriever.batch(x))
                | self.get_unique_docs  # 文档去重
        )

        unique_docs = multi_query_chain.invoke({'query': query, 'query_num': multi_query_num})

        final_docs = self.custom_rerank_documents(query=query, documents=unique_docs, top_n=1)

        return final_docs


if __name__ == '__main__':
    retrieval_service = RetrievalService(k=5)
    r = retrieval_service.rephrase_retriever(3, "如何使用U盘安装Windows7")
    for i in r:
        print(i.page_content)
