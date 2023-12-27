from openaoe.backend.util.redis_ops import get, set_always, set_ex, zincrby
from openaoe.backend.util.log import log
from openaoe.backend.util import time_util
from openaoe.backend.service.service_redis_key import Key
logger = log(__name__)

redis_prefix_key = "alles-apin::req-record"


async def request_record(uid: str, path: str):
    redis_key = f"{redis_prefix_key}::{uid}::{path}"
    count_str = get(redis_key)
    count = 0
    try:
        if count_str is None or count_str == "":
            count = count + 1
        else:
            count = int(count_str) + 1
        if not set_always(redis_key, str(count)):
            logger.error(f"record failed: uid={uid}，path={path}")
    except Exception as e:
        logger.error(f"Error occured, e={e}")


def set_api_unhealthy(t: str):
    key = Key.get_api_health_key(t)
    # TTL: 180s
    set_ex(key, str(time_util.get_current_ts_ms()), 180)


# 记录OpenAI相关的prompt_token和res_token数
async def set_openai_token(uid: str, model_name: str, prompt_tokens: int, res_tokens: int):
    date = time_util.get_human_friendly_date()
    key = Key.get_openai_token_zset_key(date)

    if prompt_tokens > 0:
        prompt_field = f"prompt:{uid}@{model_name}"
        zincrby(key, prompt_tokens, prompt_field)

    if res_tokens > 0:
        res_field = f"res:{uid}@{model_name}"
        zincrby(key, res_tokens, res_field)


if __name__ == "__main__":
    pass
