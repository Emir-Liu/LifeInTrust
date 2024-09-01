"""index route """

from fastapi import APIRouter

from .util import ret_json

router = APIRouter(tags=["index"])


@router.get("/")
async def index() -> dict:
    """index api

    test connection

    Returns:
        dict: {"status": 0, "msg": "hello world"}
    """
    return ret_json
