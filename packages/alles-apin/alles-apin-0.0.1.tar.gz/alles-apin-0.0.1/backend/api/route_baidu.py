from fastapi import APIRouter, Header, Request
from ..util.time_util import get_current_ts_ms
from ..util.log import log

from ..model.dto.BaiduDto import BaiduTransGeneralReqDto, BaiduWenxinWorkshopReqDto
from ..service.service_baidu import trans_general_svc, wenxinworkshop_chat_svc

logger = log(__name__)
router = APIRouter()


@router.post("/v1/trans/general", include_in_schema=False)
async def trans_general(request: Request, body: BaiduTransGeneralReqDto, token: str = Header(alias="alles-apin-token")):
    """
    NOT Available now
    """
    ts = get_current_ts_ms()
    logger.info("start /v1/trans/general")
    ret = trans_general_svc(request, body)
    logger.info(f"end /v1/trans/general, ts= {get_current_ts_ms() - ts} ms")
    return ret


@router.post("/v1/wenxinworkshop/chat", include_in_schema=False)
async def trans_general(body: BaiduWenxinWorkshopReqDto, token: str = Header(alias="alles-apin-token")):
    """
    NOT Available now
    """
    ts = get_current_ts_ms()
    logger.info("start /v1/wenxinworkshop/chat")
    ret = wenxinworkshop_chat_svc(body)
    logger.info(f"end /v1/wenxinworkshop/chat, ts= {get_current_ts_ms() - ts} ms")
    return ret
