from __future__ import annotations

import threading

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

from config import config
from logger import get_logger

logger = get_logger()


class MongoConnection:
    """Process-wide singleton holding a single pooled MongoClient.

    pymongo's MongoClient is thread-safe and maintains its own connection
    pool with automatic reconnection, so we only guard against creating
    more than one client per process.
    """

    _instance: MongoConnection | None = None
    _lock = threading.Lock()

    def __new__(cls) -> MongoConnection:
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            if cls._instance is not None:
                return cls._instance

            instance = super().__new__(cls)
            instance._client = None
            cls._instance = instance
            return cls._instance

    def _build_client(self) -> MongoClient | None:
        if not config.MONGO_URI:
            logger.error("MONGO_URI is not set; cannot connect to MongoDB.")
            return None

        try:
            client = MongoClient(
                config.MONGO_URI,
                maxPoolSize=50,
                minPoolSize=5,
                serverSelectionTimeoutMS=5000,
                retryWrites=True,
                retryReads=True,
            )
            # Force an early round-trip to fail fast on bad config.
            client.admin.command("ping")
            logger.info("MongoDB client initialized and reachable.")
            return client
        except PyMongoError as exc:
            logger.error(f"Failed to initialize MongoDB client: {exc}")
            return None

    @property
    def client(self) -> MongoClient | None:
        if self._client is not None:
            return self._client

        with self._lock:
            if self._client is None:
                self._client = self._build_client()
            return self._client

    @property
    def db(self) -> Database | None:
        client = self.client
        if client is None:
            return None
        return client[config.MONGO_DB_NAME]

    def close(self) -> None:
        if self._client is None:
            return
        self._client.close()
        self._client = None
        logger.info("MongoDB client closed.")


class DataAccess:
    """Thin facade passed into repositories.

    Repositories call `data_access.collection("articles")` etc. This keeps
    them decoupled from the singleton and easy to mock in tests.
    """

    def __init__(self, connection: MongoConnection | None = None):
        self._conn = connection or MongoConnection()

    def collection(self, name: str):
        # Sentinel: return None if the DB is unavailable so callers can
        # degrade gracefully instead of crashing the request.
        db = self._conn.db
        if db is None:
            logger.error(f"Requested collection '{name}' but DB is unavailable.")
            return None
        return db[name]