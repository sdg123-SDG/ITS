from openai import AsyncOpenAI
from agents import Runner, OpenAIResponsesModel, Agent, set_tracing_disabled, SQLiteSession
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

# 实例化OpenAI客户端
client = AsyncOpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

# agent实例化
agent = Agent(
    name='Assistant',
    instructions='回答要非常简洁',
    model=OpenAIResponsesModel(openai_client=client, model=os.getenv("MODEL"))
)

session1 = SQLiteSession(session_id='user1', db_path='session1.db')

async def first_run():
    result1 = await Runner.run(
        agent, 
        input='金门大桥在哪个城市',
        session=session1
    )
    print(f'  >>> [结果] {result1.final_output}\n')

async def second_run():
    result2 = await Runner.run(
        agent, 
        input='我刚才问了你什么',
        session=session1
    )
    print(f'  >>> [结果] {result2.final_output}\n')

async def get_items():
    print("--- Session Items ---")
    items = await session1.get_items()
    for it in items:
        print(it)

async def main():
    await first_run()
    await second_run()
    await get_items()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())