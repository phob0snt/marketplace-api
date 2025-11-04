import logging
from typing import Optional
import redis

from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.connect()

    def connect(self):
        try:
            self.client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            self.client.ping()
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.client = None

    def is_blacklisted(self, token: str) -> bool:
        if not self.client:
            return False

        try:
            return self.client.exists(f"blacklist:{token}") > 0
        except Exception as e:
            logger.error(f"Failed to check blacklist: {e}")
            return False

    def close(self):
        if self.client:
            self.client.close()


redis_client = RedisClient()
