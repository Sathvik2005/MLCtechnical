from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    mongo_uri: str = os.getenv("MONGO_URI", "")
    database_name: str = os.getenv("MONGO_DB", "codecity")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    redis_url: str = os.getenv("REDIS_URL", "")


settings = Settings()
