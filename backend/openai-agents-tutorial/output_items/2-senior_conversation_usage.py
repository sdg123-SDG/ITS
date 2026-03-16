from openai import AsyncOpenAI
from agents import Runner, OpenAIResponsesModel, Agent, set_tracing_disabled, SQLiteSession, function_tool
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

@function_tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    print(f"  >>> [工具调用] 正在查询 {city} 的天气...")
    return f"{city}是晴天，气温 28 度"

client = AsyncOpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))
agents = Agent(
    name='Assistant',
    model=OpenAIResponsesModel(openai_client=client, model=os.getenv("MODEL")),
    instructions='请回答问题，请简洁且briefly。',
    tools=[get_weather]
)

session_user1 = SQLiteSession("user123", "conversation_123.db")
session_user2 = SQLiteSession("user1234", "conversation_123.db")

async def first_run():
    result = await Runner.run(
        agents,
        input="武汉的天气如何？",
        session=session_user1,
    )
    print(f'  >>> [结果] {result.final_output}\n')

async def second_run():
    result = await Runner.run(
        agents,
        input="你刚才问了什么？",
        session=session_user1,
    )
    print(f'  >>> [结果] {result.final_output}\n')

async def third_run():
    result = await Runner.run(
        agents,
        input="你刚才问了什么？",
        session=session_user2,
    )
    print(f'  >>> [结果] {result.final_output}\n')

async def main():
    await first_run()
    await second_run()
    await third_run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


