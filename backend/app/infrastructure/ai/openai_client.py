from Config.settings import settings
from agents import OpenAIResponsesModel
from openai import AsyncOpenAI

# 主模型
API_KEY = settings.API_KEY
BASE_URL = settings.BASE_URL
MODEL_NAME = settings.MAIN_MODEL_NAME

# 子模型
SUB_API_KEY = settings.API_KEY
SUB_BASE_URL = settings.BASE_URL
SUB_MODEL_NAME = settings.MAIN_MODEL_NAME

# 创建 OpenAI 客户端
main_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)
sub_client = AsyncOpenAI(
    api_key=SUB_API_KEY,
    base_url=SUB_BASE_URL
)


# 创建模型对象
main_model = OpenAIResponsesModel(
    openai_client=main_client,
    model=MODEL_NAME
)
sub_model = OpenAIResponsesModel(
    openai_client=sub_client,
    model='gpt-5-nano'
)
