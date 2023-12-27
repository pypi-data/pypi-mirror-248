import json

from apscheduler.schedulers.background import BackgroundScheduler
from openaoe.backend.config.biz_config import baidu_cfg
from openaoe.backend.util.redis_ops import set_ex
import requests
from openaoe.backend.util.log import log
from openaoe.backend.util.time_util import get_current_ts_s
from openaoe.backend.config.biz_config import get_blacklist, update_blacklist
logger = log(__name__)


def refresh_baidu_token():
    logger.info("start refresh baidu token")
    aksks = baidu_cfg.get("bce_aksks")[0].split("+")
    client_id = aksks[0]
    client_secret = aksks[1]
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
    response = requests.get(url=url)
    access_token = response.json().get("access_token")
    if access_token is None or access_token == "":
        logger.error("refresh baidu access token failed")
        return

    key = "alles-apin::baidu::bce::access_token"
    b = set_ex(key, access_token, 1209600)
    if not b:
        logger.error("set baidu access token to redis failed")
        return
    logger.info("end refresh baidu token")
    return


def refresh_blacklist():
    blacklist = get_blacklist()
    if not blacklist or len(blacklist) == 0:
        return

    now = get_current_ts_s()
    after_blacklist = {}
    for model_name, kvs in blacklist.items():
        after_model_kvs = {}
        for api_key, end_timestamp in kvs.items():
            # 3s buffer
            if end_timestamp+3 > now:
                after_model_kvs[api_key] = end_timestamp
        if len(after_model_kvs) > 0:
            after_blacklist[model_name] = after_model_kvs
    update_blacklist(after_blacklist)
    if len(after_blacklist) > 0:
        logger.info(f"[blacklist-refresh] current blacklist: {json.dumps(after_blacklist)}")


def start_jobs():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(func=refresh_blacklist, trigger='interval', seconds=5)


if __name__ == "__main__":
    start_jobs()
