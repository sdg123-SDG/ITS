import asyncio
import re
from collections.abc import AsyncGenerator
from agents.run import Runner, RunConfig
from multi_agent.orchestrator_agent import orchestrator_agent
from Schemas.request import ChatMessageRequest
from Services.session_service import session_service
from Services.stream_response_service import process_stream_response
from utils.response_util import ResponseFactory
from infrastructure.logging.logger import logger
import traceback
from Schemas.response import ContentKind


class MultiAgentService:
    """
    多智能体业务服务类
    todo:
    process_task:方法前面加上async 以及返回值类型一定是AsyncGenerator
    """

    @classmethod
    async def process_task(cls, request: ChatMessageRequest, flag: bool) -> AsyncGenerator:
        """
        多智能体处理任务入口
        Args:
            request:  请求上下文

        Returns:
            AsyncGenerator：异步生成器对象（必须）
        """
        try:
            # 1. 获取请求上下文的信息
            user_id = request.context.user_id
            session_id = request.context.session_id
            user_query = request.query

            # 2. 准备历史对话
            chat_history = session_service.prepare_history(user_id, session_id, user_query)

            # 3. 运行Agent
            streaming_result = Runner.run_streamed(
                starting_agent=orchestrator_agent,
                input=chat_history,  # 列表
                context=user_query,  # 问题
                max_turns=5,  # COT(思考 行动 观察)--->迭代多少次（不是异常重试）
                run_config=RunConfig(tracing_disabled=True)
            )

            # 4. 处理Agent的事件流（事件流）
            async for chunk in process_stream_response(streaming_result):
                yield chunk

            # 5. 获取Agent的结果
            agent_result = streaming_result.final_output

            format_agent_result = re.sub(r'\n+', '\n', agent_result)
            # 6. 存储历史对话
            chat_history.append({"role": "assistant", "content": format_agent_result})

            session_service.save_history(user_id, session_id, chat_history)
        except asyncio.CancelledError:
            # 常见于前端断开连接/请求取消时：不要抛出堆栈影响日志观感
            yield "data: " + ResponseFactory.build_finish().model_dump_json() + "\n\n"
            return
        except Exception as e:
            # 记录错误日志
            logger.error(f"AgentService.process_query执行出错: {str(e)}")
            logger.debug(f"异常详情: {traceback.format_exc()}")

            text = f"❌ 系统错误: {str(e)}"
            yield "data: " + ResponseFactory.build_text(
                text, ContentKind.PROCESS
            ).model_dump_json() + "\n\n"

            # 如果允许重试，则启动重试流程
            if flag:
                text = f"🔄 正在尝试自动重试..."
                yield "data: " + ResponseFactory.build_text(
                    text, ContentKind.PROCESS
                ).model_dump_json() + "\n\n"

                # 递归调用进行重试
                async for item in MultiAgentService.process_task(request,flag=False):
                    yield item
            else:
                # 最终失败时也要显式结束 SSE，避免前端一直等待
                yield "data: " + ResponseFactory.build_finish().model_dump_json() + "\n\n"