from fastapi import APIRouter, Header, Body, Request
from src.backend.util.log import log
from src.backend.model.dto.XunfeiDto import XunfeiSparkChatReqDto
from src.backend.service.service_xunfei import spark_chat_svc
from src.backend.util.example import *


logger = log(__name__)
router = APIRouter()


@router.post("/v1/spark/chat", tags=["Spark"])
async def trans_general(request: Request, body: XunfeiSparkChatReqDto = Body(openapi_examples=spark_chat_examples()), token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    # logger.info("start /v1/spark/chat")
    ret = spark_chat_svc(request, body)
    # logger.info(f"end /v1/spark/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret
