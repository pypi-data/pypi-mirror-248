from src.backend.util.redis_ops import env
from src.backend.config import constant


def is_us():
    return env == constant.ENV_US
