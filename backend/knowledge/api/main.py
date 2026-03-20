"""

创建FastAPI实例 并且管理所有的路由

"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from api.router import router


def create_fast_api() -> FastAPI:
    # 1. 创建FastApi实例
    app = FastAPI(title="Knowledge API")

    # 2. 配置CORS中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # 允许前端访问的域名
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有HTTP方法
        allow_headers=["*"],  # 允许所有HTTP头
    )

    # 3. 注册各种路由
    app.include_router(router=router)

    # 4.返回创建的FastAPI
    return app


if __name__ == '__main__':
    print("1.准备启动Web服务器")
    try:
        uvicorn.run(app=create_fast_api(), host="127.0.0.1", port=8001)
        logger.info("2.启动Web服务器成功...")
    except KeyboardInterrupt as e:
        logger.error(f"2.启动Web服务器失败: {str(e)}")
