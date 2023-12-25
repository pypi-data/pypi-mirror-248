from .redis_ops import env
from ..config import constant


def is_us():
    return env == constant.ENV_US
