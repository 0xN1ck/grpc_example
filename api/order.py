import typing as t
from datetime import datetime
from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from grpc.aio import AioRpcError
from google.protobuf.json_format import MessageToDict

from grpc_core.protos.order import order_pb2
from grpc_core.clients.order import grpc_order_client


router = APIRouter(prefix='/order', tags=['Order'])


@router.get("")
async def list_orders(client: t.Any = Depends(grpc_order_client)) -> JSONResponse:
    try:
        orders = await client.ListOrders(order_pb2.ListOrdersRequest())
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(orders))


@router.get("/{uuid:str}")
async def single_order(
        uuid: str,
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    try:
        order = await client.ReadOrder(order_pb2.ReadOrderRequest(uuid=uuid))
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_order(
        name: str,
        completed: bool,
        date: str = f'{datetime.utcnow()}Z',
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    try:
        order = await client.CreateOrder(
            order_pb2.CreateOrderRequest(
                name=name,
                completed=completed,
                date=date
            )
        )
    except AioRpcError as e:
        logger.error(e.details())
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))


@router.patch("/{uuid:str}")
async def update_order(
        uuid: str,
        name: str,
        completed: bool,
        date: str = f'{datetime.utcnow()}Z',
        client: t.Any = Depends(grpc_order_client),
) -> JSONResponse:
    try:
        order = await client.UpdateOrder(
            order_pb2.UpdateOrderRequest(
                uuid=uuid,
                name=name,
                completed=completed,
                date=date
            )
        )
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))


@router.delete("/{uuid:str}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    uuid: str,
    client: t.Any = Depends(grpc_order_client)
) -> JSONResponse:
    try:
        order = await client.DeleteOrder(order_pb2.DeleteOrderRequest(uuid=uuid))
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))
