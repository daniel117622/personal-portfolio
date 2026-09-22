import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "blog")
    USE_MOCK: bool = os.getenv("USE_MOCK", "true").lower() in {"1", "true", "yes"}


config = Config()