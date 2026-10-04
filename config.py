import os
from dotenv import load_dotenv

from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class Config:
    MONGO_URI    : str  = os.getenv("MONGO_URI", "mongodb://mongo_db:27017")
    MONGO_DB_NAME: str  = os.getenv("MONGO_DB_NAME", "blog_db")
    USE_MOCK     : bool = os.getenv("USE_MOCK", "true").lower() in {"1", "true", "yes"}

    def __init__(self): 
        # Log the configuration state as soon as the instance is created
        logger.info(
            "Config initialized | "
            f"MONGO_DB_NAME: '{self.MONGO_DB_NAME}' | "
            f"USE_MOCK: {self.USE_MOCK} | "
            f"MONGO_URI: '{self.MONGO_URI}'"
        )


config = Config()