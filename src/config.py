import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    return os.getenv("ZHIPU_API_KEY")

def get_model_config():
    return {
        "model": os.getenv("CHAT_MODEL", "glm-4-flash"),
        "api_key": get_api_key(),
        "base_url": os.getenv("OPENAI_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        "temperature": float(os.getenv("MODEL_TEMPERATURE", "0")),
    }
