#!/bin/python
import json

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from datetime import timedelta

from .AuthMiddleware import get_record_api_type
from openaoe.backend.config.constant import *
from openaoe.backend.util.request_info import *
from openaoe.backend.config.biz_config import *
from openaoe.backend.util.time_util import *


class ApiKeyDetermineMiddleware(BaseHTTPMiddleware):
    """
    1. 根据当前vendor类型和用户id，选择本次请求使用的API KEYS
    2. 在请求结束后，若本次请求使用的API KEY失效，则对全局list轮转
    """
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_name = get_record_api_type(request.url.path)
        uid = get_request_uid(request)

        # set keys
        if api_name != API_OPENAI:
            keys = get_vendor_keys(uid, api_name)
            set_request_api_keys(request, api_name, keys)
        else:
            gpt35_keys = get_openai_key_gpt35(uid)
            gpt4_keys = get_openai_key_gpt40(uid)
            blacklist = get_blacklist()
            set_request_api_keys(request, VENDOR_OPENAI_GPT35, gpt35_keys)
            set_request_api_keys(request, VENDOR_OPENAI_GPT4, gpt4_keys)
            set_request_blacklist(request, blacklist)

        response = await call_next(request)

        # 请求结束后，检查是否需要rotate
        if is_request_keys_need_rotate(request):
            model = get_request_model(request)
            api_key = get_request_state_api_key(request)
            reason = get_request_state_error_reason(request)
            res_headers = get_request_state_res_headers(request)

            end_timestamp = get_key_block_end_timestamp(reason, res_headers)
            # 更新黑名单列表
            add_blacklist_item(model, api_key, end_timestamp)
        return response


def get_key_block_end_timestamp(reason, res_headers):
    if reason == OPENAI_KEY_ERROR_INVALID:
        return -1

    today = get_current_datetime()
    # quota超限，默认解锁时间为下个自然月
    if reason == OPENAI_KEY_ERROR_QUOTA:
        next_month = (today.month + 1) % 12
        year = today.year
        if today.month + 1 > 12:
            year += 1
        end_time = datetime(year=year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=1)
        return end_time.timestamp()
    if reason == OPENAI_KEY_ERROR_RPD or reason == OPENAI_KEY_ERROR_TPD:
        if res_headers and res_headers.get("x-ratelimit-reset-requests"):
            return get_timestamp_after_openai_format_time(res_headers.get("x-ratelimit-reset-requests"))
    if reason == OPENAI_KEY_ERROR_TPM or reason == OPENAI_KEY_ERROR_TPM:
        if res_headers and res_headers.get("x-ratelimit-reset-tokens"):
            return get_timestamp_after_openai_format_time(res_headers.get("x-ratelimit-reset-tokens"))

    # 统一处理
    if "pd" in reason:
        end_time = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute,
                            second=today.second) + timedelta(days=1)
    else:
        end_time = datetime(year=today.year, month=today.month, day=today.day, hour=today.hour, minute=today.minute,
                            second=today.second) + timedelta(minutes=1)
    return end_time.timestamp()
