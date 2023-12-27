from fastapi import APIRouter, Request, Header, Body

from openaoe.backend.model.dto.ClaudeDto import ClaudeChatReqDto
from openaoe.backend.service.service_claude import claude_chat_by_slack_svc, claude_chat_anthropic, claude_chat_stream_svc
from openaoe.backend.model.dto.ClaudeSlackDto import ClaudeSlackChatReqDto
from openaoe.backend.util.time_util import get_current_ts_ms
from openaoe.backend.util.log import log
from openaoe.backend.util.example import *

logger = log(__name__)
router = APIRouter()


# deprecated
@router.post("/v1/text/chat_by_slack", tags=["claude"], include_in_schema=False)
async def claude_by_slack_chat(body: ClaudeSlackChatReqDto, token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    ret = claude_chat_by_slack_svc(body)
    # logger.info(f"end /v1/claude/v1/text/chat_by_slack, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/text/chat", tags=["claude"])
async def claude_chat(request: Request, body: ClaudeChatReqDto = Body(openapi_examples=claude_examples()), token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    ret = claude_chat_anthropic(request, body)
    # logger.info(f"call /v1/claude/v1/text/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/text/chat-stream", tags=["claude"])
async def claude_chat_stream(request: Request, body: ClaudeChatReqDto = Body(openapi_examples=claude_examples()), token: str = Header(alias="alles-apin-token")):
    # ts = get_current_ts_ms()
    ret = claude_chat_stream_svc(request, body)
    # logger.info(f"call /v1/claude/v1/text/chat-stream, ts= {get_current_ts_ms() - ts} ms")
    return ret


