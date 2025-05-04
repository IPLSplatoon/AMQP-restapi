from fastapi import Request, HTTPException, APIRouter, Query, Response
from typing import Annotated, Optional

from restapi.rpc import Client

router = APIRouter()


@router.post("/response")
async def rpc_request(
    request: Request,
    routing_key: Annotated[str, Query(description="Routing Key")],
    timeout: Annotated[Optional[int], Query(description="Optional Request Timeout")] = None,
):
    """
    Allows you to send an RPC message to the message broker directly
    """
    try:
        body = await request.body()
        content_type = request.headers.get("content-type")
        client: Client = request.app.rpc_client
        if (response_data := await client.call(routing_key, body, content_type, timeout=timeout)) is None:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        return Response(content=response_data.data, headers=response_data.response_headers)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.post("/one_way", response_model=None)
async def one_way_msg(request: Request, routing_key: Annotated[str, Query(description="Routing Key")]):
    """
    Allows you to send an RPC message to the message broker directly with no response
    """
    body = await request.body()
    content_type = request.headers.get("Content-Type", "application/json")
    client: Client = request.app.rpc_client
    await client.one_way_call(routing_key, body, content_type)
    return Response(status_code=204)
