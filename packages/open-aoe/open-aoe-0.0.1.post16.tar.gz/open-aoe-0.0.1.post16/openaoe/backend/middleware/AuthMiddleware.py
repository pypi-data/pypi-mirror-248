from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from openaoe.backend.util.jwt_util import check_jwt_if_valid
from openaoe.backend.util.rate_limit_util import check_if_rate_limited
from openaoe.backend.util.log import log
from openaoe.backend.util import redis_ops
from openaoe.backend.service.service_redis_key import Key
from openaoe.backend.config.constant import *
from openaoe.backend.util.time_util import get_human_friendly_date
from openaoe.backend.util.run_async import run_async


logger = log("AuthMiddleware")


def get_api_type(path: str):
    try:
        s = path.split("/")
        if "gw" in path:
            return s[4]
        return path.split("/")[2]
    except:
        return ""


def get_record_api_type(path: str):
    t = get_api_type(path)
    if t not in RECORD_APIS:
        return None
    return t


# 异步记录请求
# zincrby date-type 1 token
async def record_req(path, uid):
    t = get_record_api_type(path)
    # omit some types
    if not t:
        return
    date = get_human_friendly_date()

    # zset-key
    z_key = Key.get_statistics_zset_key(t, date)
    if not redis_ops.zincrby(z_key, 1, uid):
        logger.error("record request: %s failed", t)


def check_special_uid(uid, path):
    uid = str(uid)
    # 检查是否为特殊uid
    if uid == USER_ID_FOR_OPENAI_CHECK:
        return "/check" in path
    elif "/check" in path:
        return uid == USER_ID_FOR_OPENAI_CHECK
    elif "/assistants" in path or "/files" in path or "/threads" in path:
        return uid in OPENAI_PROXY_ACCESS_UIDS
    else:
        return True


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_type = get_api_type(request.url.path)
        try:
            jwt = request.headers.get("alles-apin-token")
            uid = check_jwt_if_valid(jwt)
            if not check_special_uid(uid, request.url.path):
                logger.error(f"uid: {uid} request check openai or use special uid: -99 request other api: forbidden")
                raise Exception("invalid token")
        except:
            return Response(
                content='Invalid alles-apin-token to access resource',
                status_code=401
            )
        if uid == "":
            logger.error(f"jwt={jwt} is invalid, return 401")
            return Response(
                content='This request is blocked by Alles-APIN due to auth failed.',
                status_code=401
            )

        rate_limit_res = check_if_rate_limited(uid, api_type)
        if rate_limit_res == RATE_LIMIT_RPM_EXCEED:
            logger.error(f"user={uid} access  trigger the rate limitation")
            return Response(
                content='This request is blocked by Alles-APIN due to request rate limited. If you want higher RPM, '
                        'ask admin for help.',
                status_code=429
            )
        elif rate_limit_res == RATE_LIMIT_QUOTA_EXCEED:
            logger.error(f"user={uid} access  trigger the quota limitation")
            return Response(
                content='This request is blocked by Alles-APIN due to user quota limited. If you want higher quota, '
                        'ask Team owner for help.',
                status_code=429
            )
        # store request variable, reference: https://www.starlette.io/requests/#other-state
        request.state.uid = uid
        await run_async(record_req, request.url.path, uid)
        response = await call_next(request)
        return response
