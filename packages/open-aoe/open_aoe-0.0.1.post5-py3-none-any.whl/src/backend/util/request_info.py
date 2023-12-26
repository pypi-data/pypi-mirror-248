#! /bin/python
import random

from fastapi import Request

def set_request_uid(request: Request, uid: str):
    request.state.uid = uid


def get_request_uid(request: Request):
    return request.state.uid


# 记录model_name, 用于计算OpenAI的token消耗
def set_request_model(request: Request, model: str):
    request.state.model = model


def get_request_model(request: Request):
    return request.state.model


def set_request_api_keys(request: Request, vendor: str, l):
    try:
        request.state.vendor_keys_map[vendor] = l
    except :
        vendor_keys_map = {vendor: l}
        request.state.vendor_keys_map = vendor_keys_map


def get_request_api_key_list(request: Request, vendor: str):
    try:
        return request.state.vendor_keys_map[vendor]
    except:
        return []


def get_request_api_key(request: Request, vendor: str, model_name=None):
    if vendor not in request.state.vendor_keys_map:
        return []

    l = request.state.vendor_keys_map[vendor]
    if len(l) == 1:
        return l[0]

    # 过滤当前模型的黑名单api_key
    blacklist = get_request_blacklist(request)
    if blacklist and model_name and blacklist.get(model_name):
        kvs = blacklist.get(model_name)
        if len(kvs) < len(l):
            for item in l:
                if kvs.get(item):
                    l.remove(item)

    # random choice
    return random.choice(l)


# 判断当前api_keys列表是否支持rotate
def could_api_keys_rotate(request: Request, vendor: str):
    if vendor not in request.state.vendor_keys_map:
        return False

    l = request.state.vendor_keys_map[vendor]
    return len(l) > 1


# 记录messages, 用于计算OpenAI的token消耗
def set_request_messages(request: Request, messages):
    request.state.messages = messages


def get_request_messages(request: Request):
    return request.state.messages


def set_request_keys_need_rotate(request: Request, api_key, reason, res_headers=None):
    request.state.rotate = True
    request.state.api_key = api_key
    request.state.error_reason = reason
    request.state.res_headers = res_headers


def get_request_state_api_key(request: Request):
    try:
        return request.state.api_key
    except:
        return ""


def get_request_state_error_reason(request: Request):
    try:
        return request.state.error_reason
    except:
        return ""


def is_request_keys_need_rotate(request: Request):
    try:
        return request.state.rotate
    except:
        return False


def set_request_vendor_name(request: Request, vendor: str):
    request.state.vendor = vendor


def get_request_vendor_name(request: Request):
    return request.state.vendor


def set_request_blacklist(request: Request, blacklist: dict):
    request.state.blacklist = blacklist


def get_request_blacklist(request: Request):
    return request.state.blacklist


def get_request_state_res_headers(request: Request):
    try:
        return request.state.res_headers
    except:
        return {}
