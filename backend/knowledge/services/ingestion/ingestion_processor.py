import os
import logging

# 注意：为了跨平台兼容性，建议这里的包名统一使用小写目录
from repositories.vector_store_repository import VectorStoreRepository
from utils.markdown_utils import MarkDownUtils

from langchain_community.document_loaders import TextLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IngestionProcessor:
    """
    文档摄入类：（载入：加载、切分、存储）
    支持 Markdown (.md) 和 PDF (.pdf) 格式
    """

    def __init__(self):
        self.vector_store = VectorStoreRepository()
        self.document_spliter = RecursiveCharacterTextSplitter(
            chunk_size=1500,  # 长文档内容分块的阈值
            chunk_overlap=200,  # 给一定重合度
            separators=[
                "\n## ",
                "\n**",  # 修复：补充了缺失的逗号
                "\n\n",
                "\n",
                " ",
                "。"
            ]
        )

    def ingest_file(self, file_path: str) -> int:
        """
        文档完整操作
        包含阶段：文件的加载->文档的切割->文档的存储
        Args:
            file_path:文件的路径

        Returns:
          int: 保存成功的文档数
        """
        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return 0

        # 1. 获取文件后缀名，动态选择加载器
        file_extension = os.path.splitext(file_path)[1].lower()
        documents = []

        try:
            if file_extension in ['.md', '.txt']:
                logger.info(f"正在使用 TextLoader 加载文本/MD文件: {file_path}")
                text_loader = TextLoader(file_path=file_path, encoding="utf-8")
                documents = text_loader.load()
                # 针对 MD 文件提取特定标题
                title = MarkDownUtils.extract_title(file_path)

            elif file_extension == '.pdf':
                logger.info(f"正在使用 UnstructuredPDFLoader 加载 PDF 文件: {file_path}")
                pdf_loader = UnstructuredPDFLoader(
                    file_path=file_path,
                    mode='elements',
                    strategy='hi_res',
                    infer_table_structure=True,
                    language=['eng', 'chi_sim']
                )
                documents = pdf_loader.load()
                # PDF 默认使用文件名作为标题
                title = os.path.splitext(os.path.basename(file_path))[0]

            else:
                logger.error(f"暂不支持的文件格式: {file_extension}")
                return 0

        except Exception as e:
            logger.error(f"文件：{file_path} 加载失败, 原因:{str(e)}")
            raise Exception(f"文件：{file_path} 加载失败, 原因:{str(e)}")

        # 统一注入基础标题 metadata
        for doc in documents:
            doc.metadata['title'] = title

        # 2.切分文档得到文档块列表
        final_document_chunks = []
        for doc in documents:
            # a.如果文档内容不大，直接将这内容作为一个chunk(不用切分)
            if len(doc.page_content) < 3000:
                doc.page_content = f"文档来源:{title}\n{doc.page_content}"
                final_document_chunks.append(doc)
            else:
                # b.如果内容比较大，仅对当前长文档进行切分 (修复了原代码 split_documents(documents) 的问题)
                documents_chunks_list = self.document_spliter.split_documents([doc])

                # 遍历切分后的块，注入标题上下文
                for document_chunk in documents_chunks_list:
                    document_chunk.page_content = f"文档来源:{title}\n{document_chunk.page_content}"

                final_document_chunks.extend(documents_chunks_list)

        # 3.切分后文档块的元数据校验(非常重要：UnstructuredPDFLoader 会生成复杂嵌套字典，必须过滤)
        clean_documents_chunks = filter_complex_metadata(final_document_chunks)

        # 4. 无效性检查（校验page_content是否合法，剔除纯空白块）
        valid_documents_chunks = [document for document in clean_documents_chunks if
                                  document.page_content and document.page_content.strip()]

        if not valid_documents_chunks:
            logger.warning(f"文件 {file_path} 切分后的文档块没有任何有效内容")
            return 0

        # 5.存储文档块到向量数据库
        total_documents_chunks = self.vector_store.add_documents(valid_documents_chunks)

        logger.info(f"文件 {file_path} 摄入完成，共计 {total_documents_chunks} 个有效文档块入库。")

        # 6.返回保存成功的文档块数
        return total_documents_chunks