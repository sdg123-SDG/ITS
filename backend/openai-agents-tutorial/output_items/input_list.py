from agents import Agent, set_tracing_disabled, OpenAIResponsesModel, function_tool, Runner
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)
set_tracing_disabled(disabled=True)

@function_tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    print(f"  >>> [工具调用] 正在查询 {city} 的天气...")
    return f"{city}是晴天，气温 28 度"

async def main():
    # 1.创建一个Agent，并设置第一轮输出
    agent = Agent(
        name='天气专家',
        instructions='你是一个天气专家，你需要根据用户的输入，给出一个简单的天气预报。',
        model=OpenAIResponsesModel(openai_client=client, model=os.getenv("MODEL")),
        tools=[get_weather]
    )

    result1 = await Runner.run(agent, input='武汉的天气怎么样')
    print(f'  >>> [结果] {result1.final_output}\n')

    # 2.查看历史记录
    history = result1.to_input_list()
    print(f'审查历史记录：')
    for i, item in enumerate(history):

        print(f'  {i}. {item}')
    
    # 3.基于历史记录，生成新的输入
    print('基于历史记录，生成新的输入：')
    new_input = history + [{"role": "user", "content": "那这种天气适合去跑步吗？"}]
    result2 = await Runner.run(agent, input=new_input)
    print(f'  >>> [结果] {result2.final_output}\n')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
