import json

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from openaoe.backend.middleware.AuthMiddleware import get_api_type
from openaoe.backend.util.request_record_util import set_api_unhealthy, set_openai_token
from openaoe.backend.config.constant import API_OPENAI, USER_ID_FOR_OPENAI_CHECK
from openaoe.backend.util.log import log
from openaoe.backend.util.openai_token_calculate import calculate_tokens_from_messages
from openaoe.backend.util.run_async import run_async


logger = log(__name__)


async def record_api(uid, status_code, response, t: str, request):
    if len(t) == 0:
        return
    if uid == USER_ID_FOR_OPENAI_CHECK:
        return

    try:
        if response.headers["content-type"] == "application/json":
            resp_body = [section async for section in response.__dict__['body_iterator']]
            # Repairing FastAPI response
            response.__setattr__('body_iterator', aiwrap(resp_body))
        elif t.lower() == API_OPENAI:
            # 特殊处理SSE返回
            messages = request.state.messages
            model_name = request.state.model
            if not messages or not model_name:
                logger.warn("record openai token for stream failed, empty messages or model name")
                return
            prompt_tokens = calculate_tokens_from_messages(messages, model_name)
            await set_openai_token(uid, model_name, prompt_tokens, 0)
            return
        else:
            return
    except Exception as e:
        logger.warn(f"record api message failed: {e}")
        return

    try:
        resp_body = json.loads(resp_body[0].decode())
    except:
        return

    if status_code == 200:
        # 区分proxy类别的返回(不纳入OpenAI的健康检测，直接返回)
        if "statusCode" in resp_body:
            return
        if resp_body.get("msgCode") != "10000":
            set_api_unhealthy(t)
        else:
            try:
                # 记录OpenAI的prompt_tokens和completion_tokens
                if t.lower() == API_OPENAI:
                    usage = resp_body.get("data").get("usage")
                    prompt_tokens = usage.get("prompt_tokens")
                    res_tokens = usage.get("completion_tokens")
                    model_name = resp_body.get("data").get("model")
                    await set_openai_token(uid, model_name, prompt_tokens, res_tokens)
            except Exception as e:
                logger.warn(f"record openai token failed: {e}")
    return


class HealthRecordMiddleware(BaseHTTPMiddleware):
    """
    中间件作用：
    1. 对于application/json类型的返回，检查是否msgCode为10000，不是则记录当前供应商模型返回不正常
    2. 对于application/json类型的返回，若请求的供应商模型为OpenAI，则记录prompt_tokens和completion_tokens
    """
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        try:
            uid = request.state.uid
            await record_api(uid, response.status_code, response, get_api_type(request.url.path), request)
        except Exception as e:
            logger.warn(f"get uid failed: {e}")
        return response


class aiwrap:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
