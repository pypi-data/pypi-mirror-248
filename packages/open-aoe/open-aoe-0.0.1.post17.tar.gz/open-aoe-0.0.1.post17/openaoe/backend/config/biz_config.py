import sys

from openaoe.backend.util.redis_ops import get
from openaoe.backend.util.log import log
from openaoe.backend.model.base.PoolConfigBase import PoolConfig
from multiprocessing import Lock
from .constant import *
import os

logger = log(__name__)


logger.info("start to init configuration.")

# pool config
# {
#   "users": {
#       "openai-gpt35": {
#           "user-id-1": "gpt35-pool-a"
#       }
#   },
#   "keys": {
#       "gpt35-pool-a": []
#   },
#   "blacklist": {
#       "gpt-3.5-turbo": {
#           "sk-***": 140938080
#       },
#       "all": ["sk-***"]
#   }
# }
lock = Lock()
# 进程间共享
d = {}
pool_config_str = get(REDIS_KEY_POOLS_CONFIG)
if not pool_config_str:
    logger.error("empty pools config, exit error")
    sys.exit(-1)
p = PoolConfig.convert(pool_config_str)
p.set_keys(d, lock)


def _get_key_list(uid: str, vendor: str):
    key_name = p.get_user_vendor_key_name(uid, vendor)
    return p.get_keys(key_name, d, lock)


def _set_key_list(uid: str, vendor: str, keys: []):
    key_name = p.get_user_vendor_key_name(uid, vendor)
    with lock:
        d[key_name] = keys
    logger.info(f"set keys for vendor: {key_name}, after: {d[key_name]}")


def get_openai_key_gpt35(uid: str):
    return _get_key_list(uid, VENDOR_OPENAI_GPT35)


def get_openai_key_gpt40(uid: str):
    return _get_key_list(uid, VENDOR_OPENAI_GPT4)


def set_openai_key_gpt35(uid: str, list):
    _set_key_list(uid, VENDOR_OPENAI_GPT35, list)


def set_openai_key_gpt40(uid: str, list):
    _set_key_list(uid, VENDOR_OPENAI_GPT4, list)


def get_vendor_keys(uid: str, vendor: str):
    return _get_key_list(uid, vendor)


def set_vendor_keys(uid: str, vendor: str, l):
    _set_key_list(uid, vendor, l)


def get_blacklist():
    return p.get_blacklist(lock)


def add_blacklist_item(model_name, api_key, end_timestamp):
    p.add_blacklist_item(lock, model_name, api_key, end_timestamp)
    logger.info(f"[blacklist-add]model: {model_name}, api_key: {api_key}, end_timestamp: {end_timestamp}")


def update_blacklist(blacklist):
    p.update_blacklist(lock, blacklist)


def app_abs_path():
    return os.path.dirname(os.path.abspath(__file__)).split("/backend")[0]


def img_out_path():
    abs_path = app_abs_path()
    return f'{abs_path}/frontend/dist/tmp/img/out'


def img_in_path():
    abs_path = app_abs_path()
    return f'{abs_path}/frontend/dist/tmp/img/in'



mini_max_cfg = {
    "api_url": "https://api.minimax.chat/v1/text/chatcompletion?GroupId=",
    "group_id": "1683526222209693"
}

# openai config
openai_cfg = {
    "api_url": ["https://api.openai.com/v1"]
}

# baidu config
baidu_bce_aksks = get("alles-apin::baidu::bce::aksk").split(",")
baidu_bce_access_tokens = get("alles-apin::baidu::bce::access-token").split(",")
baidu_cfg = {
    "trans_api_url": "https://fanyi-api.baidu.com/api/trans/vip/translate",
    "wenxinworkshop_url": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop",
    "bce_aksks": baidu_bce_aksks,
    "bce_access_tokens": baidu_bce_access_tokens,
}

# palm config
google_cfg = {
    "api_urls": ["http://us.alles-apin.openxlab.org.cn/google/v1beta2/models"]
}

# spark config
xunfei_cfg = {
    "spark_chat_url": "wss://spark-api.xf-yun.com/v2.1/chat"
}

# claude config
claude_cfg = {
    "claude_infos": []
}


# slack config
# deprecated
slack_infos = get("alles-apin::claude::slack::info").split(",")
logger.info(f"slack_claude_infos={slack_infos}")
if slack_infos is None or slack_infos[0] == "" or len(slack_infos) == 0:
    logger.error(f"get slack_infos from redis is None, exit with code 1")
    exit(1)
claude_slack_cfg = {
    "slack_infos": slack_infos
}

jwt_secret = get("alles-apin::auth::jwt::secret")
if jwt_secret is None or jwt_secret == "":
    logger.error("jwt secret is empty, application start failed!")
    exit(1)
jwt_cfg = {
    "jwt_secret": jwt_secret
}


logger.info(f'current active environment is: {os.environ.get("region")}')
logger.info("init configuration successfully.")
logger.info(f"pools config: {d}")

if __name__ == "__main__":
    pass
