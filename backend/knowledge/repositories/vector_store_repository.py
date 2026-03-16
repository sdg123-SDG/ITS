from langchain_chroma import Chroma
from config.settings import settings
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreRepository:
    """
    作用：对向量数据库场景做读写
    """

    def __init__(self):
        """
        创建向量数据库实例
        存储向量数据、支持搜索
        """
        self.embedding = OpenAIEmbeddings(
            model='text-embedding-3-large', 
            api_key=settings.API_KEY, 
            base_url=settings.BASE_URL
        )

        self.vector_database = Chroma(
            persist_directory=settings.VECTOR_STORE_PATH,                     
            collection_name="its-knowledge",
            embedding_function=self.embedding
        )

    def add_documents(self, documents: list, batch: int=16)->int:
        """ 
            documents 是切割后的文档块chunk, 而后续调用 OpenAI Embeddings 模型生成向量时，模型会先把每个 chunk 转换成 token, 再进行编码"""
        """
        作用：将切割后的文档块保存到向量数据库中
        参数：
            documents: 切割后的文档
            batch: 批次大小
        返回：
            成功添加到向量数据库中文档块的数量(服务前端展示)
        """

        # 1.获取文档块数量
        total_documents_chunks = len(documents)

        # 2.批量保存到向量数据库中
        has_added=0
        try:
            for i in range(0, total_documents_chunks, batch):
                bath = documents[i:i+batch]
                self.vector_database.add_documents(bath)
                has_added += len(bath)
                logger.info(f"已添加向量数据库中：{has_added}/{total_documents_chunks}")
        except Exception as e:
            logger.error(f"添加向量数据库失败：{e}")

        return has_added
    
    def embedd_document(self,text:str)->List[float]:
        """
          对query进行向量化
        Args:
            text: 输入文本

        Returns:
            List[float]: 嵌入后的浮点数列表

        """
        return self.embedding.embed_query(text)

    def embedd_documents(self, texts:List[str])->List[List[float]]:
        """
        对字符串列表进行向量化
        Args:
         texts: 输入文本字符串列表

        Returns:
            List[List[float]]: 嵌入后的多个文本的浮点数列表

        """
        return self.embedding.embed_documents(texts)


    def search_similarity_with_score(self,user_question:str,top_k:int=5)->List[tuple[Document, float]]:
        """
         相似性检索带文档分数
         分数（chroma向量数据库）：返回是L2距离得分（分数值越小越相似），不是余弦相似度的得分（分数余额高越相似） 距离得分：1-余弦相似度得分
        Args:
            user_question:

        Returns:
            List[Document]: 返回基于向量检索的相似性文档列表

        """
        return self.vector_database.similarity_search_with_score(user_question,top_k)

