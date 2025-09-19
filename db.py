from typing import cast
from redis import Redis
import os


class Db:
    def __init__(self):
        self.REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
        self.REDIS_PORT = os.getenv("REDIS_PORT") or 6379
        self.REDIS_USER = os.getenv("REDIS_USER") or "redis"
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or "redis"
        self.db = self._create_connection() 

    def connect(self):
        if not self.db:
            self.db = self._create_connection()
            return self.db
        if not self.db.ping():
            self.db = self._create_connection()

        return self.db

    def close(self):
        if not self.db:
            return
        
        self.db.close()
        self.db = None

    def get(self, key: str) -> dict[str, str] | None:
        self.connect()
        if not self.db:
            return
        data = self.db.get(key)
        self.close()
        return cast(dict[str, str], data) 
    def set(self, key, value) -> None:
        self.connect()
        if not self.db:
            return
        self.db.set(key, value)
        self.close()

    def get_many(self, keys: list[str]) -> list[str]:
        self.connect()
        if not self.db:
            return []
        data = self.db.mget(keys)
        self.close()
        return cast(list[str], data)

    def set_many(self, data: dict[str, str]) -> None:
        self.connect()
        if not self.db:
            return
        self.db.mset(data)
        self.close()

    def _create_connection(self) -> Redis:
        return Redis(
                host=self.REDIS_HOST,
                port=int(self.REDIS_PORT),
                username=self.REDIS_USER,
                password=self.REDIS_PASSWORD,
                decode_responses=True,
                ssl=True,
                ssl_cert_reqs="none"
        )
