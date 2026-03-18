from langchain_chroma import Chroma
from config.settings import settings
from langchain_openai.embeddings import OpenAIEmbeddings
import logging
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

    def add_documents(self, documents: list, batch: int = 16) -> int:
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
        has_added = 0
        try:
            for i in range(0, total_documents_chunks, batch):
                bath = documents[i:i + batch]
                self.vector_database.add_documents(bath)
                has_added += len(bath)
                logger.info(f"已添加向量数据库中：{has_added}/{total_documents_chunks}")
        except Exception as e:
            logger.error(f"添加向量数据库失败：{e}")

        return has_added
