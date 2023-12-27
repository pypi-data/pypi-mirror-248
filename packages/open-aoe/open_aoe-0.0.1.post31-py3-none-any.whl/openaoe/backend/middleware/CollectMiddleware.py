import json
import os
import re
import time
import uuid
import requests

from sys import exc_info
from concurrent.futures import ThreadPoolExecutor

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import StreamingResponse

from openaoe.backend.util.log import log


logger = log("collector")

PLATFORM_PREFIX = "apin_"
PLATFORM_SESSION_TYPE = os.getenv("INFER_STORE_SESSION_TYPE", "5")
INFER_STORE_ENDPOINT = os.getenv("INFER_STORE_ENDPOINT", "http://106.14.134.80:60060")

URL_FILTER_PATTERN = os.getenv("INFER_STORE_FILTER", ".*/v1/[claude|google|minimax|openai|xunfei]+/.*")


class CollectMiddleware(BaseHTTPMiddleware):


    async def set_body(self, request: Request):
        """复用request body

        Args:
            request (Request):

        Returns:
            _type_:
        """
        receive_ = await request._receive()

        async def receive():
            return receive_

        request._receive = receive


    async def dispatch(self,
                       request: Request,
                       call_next: RequestResponseEndpoint
    ) -> Response:
        # 白名单
        if re.match(URL_FILTER_PATTERN, request.url.path):
            request_time = int(round(time.time() * 1000))

            await self.set_body(request)
            request_body = await request.body()

            response = await call_next(request)

            if isinstance(response, StreamingResponse):
                return CollectResponse(request, response, request_body=request_body, request_time=request_time)

            return response

        return await call_next(request)


executor = ThreadPoolExecutor(max_workers=5)


CLAUDE_TEXT_CHAT = "claude/v1/text/chat"

GOOGLE_TEXT_PALM_CHAT = "google/v1/palm/chat"
GOOGLE_TEXT_PALM_TEXT = "google/v1/palm/text"

MINIMAX_TEXT_CHAT = "minimax/v1/text/chat"

OPENAI_TEXT_CHAT_API = "v1/openai/v2/text/chat"
OPENAI_API = "v1/openai/v1"

XUFEI_API = "xunfei/v1/spark/chat"


class PromptRequest:


    def __init__(self,
                 request: Request,
                 response: StreamingResponse,
                 **kwargs) -> None:
        self.bytes_data = []
        self.request = request
        self.response = response

        self.request_body = kwargs.pop('request_body', None)

        self.status_code = self.response.status_code
        self.content_type = response.headers.get('content-type')
        self.json_header = "application/json"

        self.SSE_HEADER = "text/event-stream"
        self.SSE_DEFAULT_SEPARATOR = "\r\n"
        self._sep = self.SSE_DEFAULT_SEPARATOR
        self.SSE_DATA_PATTERN = f'data: (.*){self._sep}'

        self.model = "default"
        self.prompt = "default"
        self.messages = []
        self.payload = None
        self.output = None
        self.request_time = str(kwargs.pop("request_time", 0))
        self.response_time = None
        self.uid = ""


    def store_chunk(self, data):
        if isinstance(data, bytes):
            self.bytes_data.append(data)


    def complete(self):
        self.response_time = str(int(round(time.time() * 1000)))


    def collect_json(self):
        try:
            dto = json.loads(self.bytes_data[0])
            if dto:
                msg_code = dto.get("msgCode")
                if msg_code == '10000':
                    return dto.get('data')

            logger.warn(f"ignore this collection, status_code: {self.status_code}, data: {self.bytes_data}")
        except Exception as ex:
            logger.exception("collect application/json data error", exc_info=ex)


    def collect_sse(self):
        content = ""
        for b_data in self.bytes_data:
            str_data = b_data.decode('utf-8')

            data_groups = re.findall(self.SSE_DATA_PATTERN, str_data)
            for data in data_groups:
                try:
                    dto = json.loads(data)
                    success = dto.get("success")
                    msg = dto.get('msg')
                    # 成功标志是字符串
                    if success == 'true' and msg:
                        content = content + msg
                    elif msg:
                        logger.warn("failed message: %s", msg)
                except Exception as ex:
                    if isinstance(data, str):
                        content = content + data
                    else:
                        logger.exception("collect text/event-stream data error", exc_info=ex)

        return None if len(content) == 0 else content


    def collect(self):

        if self.status_code != 200:
            logger.warn(f"ignore this collection, status_code: {self.status_code}, data: {self.output}")
            return

        # 空响应
        if len(self.bytes_data) == 0:
            logger.warn(f"ignore this collection, response body is empty")
            return

        if self.content_type and self.SSE_HEADER in self.content_type:
            self.output = self.collect_sse()
        else:
            self.output = self.collect_json()

        return self.output


    @staticmethod
    def handle_exception(result):
        ex = result.exception()
        if ex:
            logger.exception("send infer-store request error", exc_info=ex)


    def send_result(self):
        self.complete()

        def send():
            self.uid = self.request.state.uid
            request_body = json.loads(self.request_body)
            self.prompt = request_body.get('prompt')
            self.model = request_body.get('model', "")
            self.messages = request_body.get('messages', [])
            self.payload = request_body.get('payload', None)

            # logger.info("request body: %s, response body: %s", request_body, self.bytes_data)

            # 根据模型不同，处理不同的输入
            path = self.request.url.path
            input = []
            output = self.collect()

            # if OPENAI_TEXT_CHAT_API in path:
            #    input = self.request_body
            # elif OPENAI_API in path or \
            #     MINIMAX_TEXT_CHAT in path:
            #     """ `openai/mnimax`
            #         {
            #             messages: [
            #                 {text: "你好", sender_type: "USER"},
            #                 {text: "请用大海写一首绝句", sender_type: "USER"}
            #             ],
            #             model: "abab5-chat",
            #             prompt: "hello",
            #             role_meta: {user_name: "USER", bot_name: "BOT"},
            #             stream: true,
            #             type: "json"
            #         }
            #     """
            #     input = self.messages
            #     if self.prompt and len(self.prompt) > 0:
            #         input.append({
            #             "text": self.prompt,
            #             "sender_type": "user"
            #         })
            # elif CLAUDE_TEXT_CHAT in path :
            #     """ `claude`
            #         {
            #             max_tokens: 5000,
            #             messages: [
            #                 {role: "user", content: "你好"},
            #                 {role: "user", content: "请用大海写一首绝句"},
            #                 {role: "user", content: "你好"}
            #             ],
            #             model: "claude-1",
            #             prompt: "",
            #         }
            #     """
            #     for msg in self.messages:
            #         msg_new = {}
            #         for key, value in msg.items():
            #             if key == "role":
            #                 msg_new['sender_type'] = value
            #             elif key == "content":
            #                 msg_new['text'] = value
            #             else:
            #                 msg_new[key] = value
            #         input.append(msg_new)

            #     if self.prompt and len(self.prompt) > 0:
            #         input.append({
            #             "text": self.prompt,
            #             "sender_type": "user"
            #         })
            # elif GOOGLE_TEXT_PALM_CHAT in path:
            #     """ `google`
            #     """
            #     for msg in self.messages:
            #         msg_new = {}
            #         for key, value in msg.items():
            #             if key == "author":
            #                 msg_new['sender_type'] = "user" if value == 0 else 'bot'
            #             elif key == "content":
            #                 msg_new['text'] = value
            #             else:
            #                 msg_new[key] = value
            #         input.append(msg_new)
            if GOOGLE_TEXT_PALM_TEXT in path:
                self.model = "palm"
                # text = self.prompt.get('text')
                # if text is None:
                #     return

                # input.append({
                #         "text": text,
                #         "sender_type": "user"
                #     })
            elif XUFEI_API in path:
                self.model = "spark"
            #     payload = self.payload
            #     if payload is None:
            #         return

            #     message = payload.get('message')
            #     if message is None:
            #         return

            #     texts = message.get('text')
            #     if texts is None:
            #         return

            #     for text in texts:
            #         msg_new = {}
            #         for key, value in text.items():
            #             if key == "role":
            #                 msg_new['sender_type'] = value if value == 'user' else 'assistant'
            #             elif key == "content":
            #                 msg_new['text'] = value
            #             else:
            #                 msg_new[key] = value
            #         input.append(msg_new)

            input = request_body

            # 无输入和输出，不上报
            if len(input) == 0 or output is None:
                return

            if not isinstance(input, str):
                input = json.dumps(input, ensure_ascii=False)

            if not isinstance(output, str):
                output = json.dumps(output, ensure_ascii=False)

            session_id = str(uuid.uuid4())
            model_id = PLATFORM_PREFIX + self.model
            uid = PLATFORM_PREFIX + str(self.uid)

            data = json.dumps({
                "uid": uid,
                "model_id": model_id,
                "session_id": session_id,
                "session_type": PLATFORM_SESSION_TYPE,
                "request_id": session_id,
                "request_ts": self.request_time,
                "input": input,
                "response_ts": self.response_time,
                "output": output
            }, ensure_ascii=False)

            # logger.info("send request: %s", data)
            logger.info("send infer-store request, uid: %s", uid)
            response = requests.post(INFER_STORE_ENDPOINT + "/StoreData", data=data.encode("utf-8"), timeout=5)

            if response.status_code != 200:
                logger.error("send infer-store request error: {}".format(response.text))

        sub = executor.submit(send)
        sub.add_done_callback(self.handle_exception)


class CollectResponse(StreamingResponse, PromptRequest):


    def __init__(self,
                 request: Request,
                 response: StreamingResponse,
                 **kwargs) -> None:
        self._info = response._info

        StreamingResponse.__init__(self, response.body_iterator, response.status_code)
        self.raw_headers = response.raw_headers

        PromptRequest.__init__(self, request, response, **kwargs)


    async def stream_response(self, send) -> None:
        if self._info:
            await send({"type": "http.response.debug", "info": self._info})

        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )
        async for chunk in self.body_iterator:
            if not isinstance(chunk, bytes):
                chunk = chunk.encode(self.charset)

            # 收集每次响应的chunk
            self.store_chunk(chunk)

            await send({"type": "http.response.body", "body": chunk, "more_body": True})

        # 上报结果
        self.send_result()

        await send({"type": "http.response.body", "body": b"", "more_body": False})
