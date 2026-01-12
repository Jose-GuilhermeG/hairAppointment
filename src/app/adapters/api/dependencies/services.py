from redis import Redis

from src.configs.settings import REDIS_HOST , REDIS_PASSWORD , REDIS_PORT , SESSION_EXPIRE_TIME


redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password =REDIS_PASSWORD or None,
    decode_responses=True
)