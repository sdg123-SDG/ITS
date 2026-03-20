from fastapi.routing import APIRouter
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse
from Schemas.request import ChatMessageRequest, UserSessionsRequest
from Services.agent_service import MultiAgentService
from infrastructure.logging.logger import logger
from Services.session_service import session_service
import os

# 1. 定义请求路由器
router = APIRouter()


# 2. 定义对话请求
@router.post("/api/query", summary="智能体对话接口")
async def query(request_context: ChatMessageRequest) -> StreamingResponse:
    """
    SSE返回数据（流式响应）
    响应头中：text/event-stream
    Args:
        request_context: 请求上下文

    Returns:
        StreamingResponse

    """

    # 1. 获取请求上下文的属性
    user_id = request_context.context.user_id
    user_query = request_context.query
    print(request_context.flag)
    logger.info(f"用户 {user_id} 发送的待处理任务 {user_query}")

    # 2. 调用AgentService（智能体的业务服务类）
    async_generator_result = MultiAgentService.process_task(request_context, flag=True)

    # 3. 封装结果到StreamingResponse中
    return StreamingResponse(
        content=async_generator_result,
        status_code=200,
        media_type="text/event-stream"
    )


@router.post("/api/user_sessions")
def get_user_sessions(request: UserSessionsRequest):
    """
    获取用户的所有会话记忆数据。

    Args:
        request: 包含 user_id 的请求体。

    Returns:
        包含用户所有会话信息和记忆的 JSON 响应。
    """
    # 1. 日志记录：记录请求到达
    logger.info("接收到获取用户会话请求")

    # 2. 参数提取：从请求模型中获取目标用户ID
    user_id = request.user_id
    logger.info(f"获取用户 {user_id} 的所有会话记忆数据")

    try:
        # 3. 服务调用 session_service 从底层存储检索所有历史会话
        all_sessions =session_service.get_all_sessions_memory(user_id)
        logger.debug(f"成功获取用户 {user_id} 的 {len(all_sessions)} 个会话")

        # 4. 响应构建：组装并返回标准化的成功 JSON 数据
        return {
            "success": True,
            "user_id": user_id,
            "total_sessions": len(all_sessions),
            "sessions": all_sessions
        }
    except Exception as e:
        # 5. 异常处理：捕获服务层抛出的未知错误，记录日志并返回错误标识
        logger.error(f"获取用户 {user_id} 的会话数据时出错: {str(e)}")
        return {
            "success": False,
            "user_id": user_id,
            "error": str(e)
        }


@router.get("/api/download/{file_name}", summary="下载文件")
async def download_file(file_name: str):
    """
    下载文件
    Args:
        file_name: 文件名

    Returns:
        文件内容
    """
    try:
        # 1. 构建文件路径
        # Use the same directory as the knowledge backend
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge', 'data', 'tmp', file_name)
        
        # 2. 检查文件是否存在
        if not os.path.exists(file_path):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 3. 读取文件内容并返回
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"下载文件失败:原因:{str(e)}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="服务内部出现异常")
