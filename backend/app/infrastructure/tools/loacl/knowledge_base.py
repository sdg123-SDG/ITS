from agents import function_tool
import asyncio
import httpx
from typing import Dict
from infrastructure.logging.logger import logger
from Config.settings import settings


@function_tool
async def query_knowledge(query: str) -> Dict:

    """
       查询电脑问题知识库服务,用于检索与用户问题相关的技术文档或解决方案。

       Args:
           query (Optional[str]): 需要查询的具体问题文本。

       Returns:
           dict: 包含查询结果的字典。包含 'question':用户输出问题 ‘answer’:答案
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. 发送请求，异步上下文管理器对象
            response = await client.post(url=f'{settings.KNOWLEDGE_BASE_URL}/query',
                                         json={"question": query},
                                         timeout=60*10
                                         )
            # 2. 抛出异常
            response.raise_for_status()

            # 3. 处理正常的结果
            return response.json()

        except httpx.HTTPError as e:
            logger.error(f"发送请求，获取知识库下的知识失败了:{repr(e)}")
            return {"status": "error", "message": f'发送请求，获取知识库下的知识失败了:{repr(e)}'}
        except Exception as e:
            logger.error(f"未知的错误:{repr(e)}")
            return {"status": "error", "message": f'未知的错误:{repr(e)}'}


async def main():
    r = await query_knowledge(query='电脑不能开机了，怎么办')
    print(r)
if __name__ == '__main__':
    asyncio.run(main())