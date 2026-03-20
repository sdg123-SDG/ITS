import uvicorn
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from infrastructure.logging.logger import logger
from Api.routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI应用生命周期管理

    在应用启动时建立MCP连接，在应用关闭时清理连接。
    确保资源正确初始化和释放。
    """
    # 应用启动时执行
    logger.info("应用启动...")
    
    # 导入MCP客户端
    from infrastructure.tools.mcp.mcp_servers import search_mcp_client, baidu_mcp_client
    
    # 连接MCP服务器
    try:
        logger.info("正在连接MCP服务器...")
        await search_mcp_client.connect()
        await baidu_mcp_client.connect()
        logger.info("MCP服务器连接成功")
    except Exception as e:
        logger.error(f"MCP服务器连接失败: {str(e)}")

    yield  # 应用运行期间

    # 应用关闭时执行
    logger.info("应用关闭...")
    
    # 清理MCP连接
    try:
        await search_mcp_client.cleanup()
        await baidu_mcp_client.cleanup()
        logger.info("MCP服务器连接已清理")
    except Exception as e:
        logger.error(f"MCP服务器连接清理失败: {str(e)}")


def create_fast_api() -> FastAPI:
    # 1. 创建FastApi实例,绑定了生命周期事件
    app = FastAPI(title="ITS API", lifespan=lifespan)

    # 2. 处理跨域
    app.add_middleware(
        CORSMiddleware,
        # CORSMiddleware 会自动拦截后端的响应 并贴上这些标签 Access-Control-Allow-Origin Access-Control-Allow-Methods Access-Control-Allow-Headers
        allow_origins=["*"],  # 生产环境应限制为特定域名
        allow_credentials=True,  # cookie(自定义的key value)(user_id)
        allow_methods=["*"],  # 任意的请求都可以（POST）
        allow_headers=["*"],  # 请求头中带上自己的信息（token）
    )

    # 3. 注册各种路由
    app.include_router(router=router)

    # 4.返回创建的FastAPI
    return app


if __name__ == '__main__':
    print("1.准备启动Web服务器")
    try:
        uvicorn.run(app=create_fast_api(), host="127.0.0.1", port=8000)

        logger.info("2.启动Web服务器成功...")

    except KeyboardInterrupt as e:
        logger.error(f"2.启动Web服务器失败: {str(e)}")
