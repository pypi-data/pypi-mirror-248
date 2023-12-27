import json

from openaoe.backend.config.biz_config import baidu_cfg
import requests
from openaoe.backend.util.request_info import *
from openaoe.backend.config.constant import *
from openaoe.backend.model.dto.BaiduDto import BaiduTransGeneralReqDto, BaiduWenxinWorkshopReqDto
from openaoe.backend.util.encrypt_util import md5_generate
from openaoe.backend.util.log import log
from openaoe.backend.util.time_util import get_current_ts_ms
from openaoe.backend.model.dto.ReturnBase import ReturnBase

logger = log(__name__)


def trans_general_svc(request, req_dto: BaiduTransGeneralReqDto):
    base_url = baidu_cfg.get("trans_api_url")
    appid_keys = get_request_api_key(request, VENDOR_BAIDU)
    appid = appid_keys.split("+")[0]
    key = appid_keys.split("+")[1]
    q = req_dto.q
    frm = req_dto.frm
    to = req_dto.to
    salt = get_current_ts_ms()
    sign = md5_generate(f"{appid}{q}{salt}{key}")
    url = f"{base_url}?q={q}&from={frm}&to={to}&appid={appid}&salt={salt}&sign={sign}"
    logger.info(f"calling baidu api url: {url}")
    response = requests.get(url)
    response_json = response.json()
    err_code = response_json.get("error_code")

    if err_code is not None:
        err_msg = response_json.get("error_msg")
        base = ReturnBase(
            msgCode="-1",
            msg=f"call baidu api failed, appid={appid}. Detail reason: {err_msg}"
        )
        return base
    base = ReturnBase(
        data=response_json
    )
    return base


def wenxinworkshop_chat_svc(req_dto: BaiduWenxinWorkshopReqDto):
    return ReturnBase(data="not available now")
    # access_token = get("alles-apin::baidu::bce::access_token")
    # base_url = baidu_cfg.get("wenxinworkshop_url")
    # url = f'{base_url}/chat/completions?access_token={access_token}'
    # messages = []
    # for msg in req_dto.messages:
    #     message = {
    #         "role": msg.role,
    #         "content": msg.content
    #     }
    #     messages.append(message)
    # body = {
    #     "messages": messages,
    #     "stream": req_dto.stream
    # }
    # dumps = json.dumps(body)
    # response = requests.post(url=url, data=dumps)
    # response_json = response.json()
    # if response_json.get("error_code") is not None:
    #     return ReturnBase(
    #         msgCode="-1",
    #         msg="error",
    #         date=response_json
    #     )
    #
    # return ReturnBase(
    #     data= response_json
    # )


if __name__ == "__main__":
    pass
