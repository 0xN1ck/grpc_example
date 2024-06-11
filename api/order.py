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
    """
    Получает список заказов через gRPC сервис OrderService.

    Функция вызывает метод ListOrders gRPC сервиса OrderService для получения списка всех заказов.
    В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными списка заказов.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
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
    """
    Получает данные одного заказа по UUID через gRPC сервис OrderService.

    Функция вызывает метод ReadOrder gRPC сервиса OrderService для получения данных заказа по указанному UUID.
    В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    uuid : str
        Уникальный идентификатор заказа.
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными запрошенного заказа.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
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
    """
    Создает новый заказ через gRPC сервис OrderService.

    Функция вызывает метод CreateOrder gRPC сервиса OrderService для создания нового заказа
    с указанными параметрами. В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    name : str
        Название заказа.
    completed : bool
        Статус выполнения заказа.
    date : str, optional
        Дата создания заказа в формате строки (по умолчанию текущая дата и время в формате UTC с 'Z').
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными созданного заказа.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
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
    """
   Обновляет существующий заказ по UUID через gRPC сервис OrderService.

   Функция вызывает метод UpdateOrder gRPC сервиса OrderService для обновления данных заказа
   с указанными параметрами. В случае ошибки gRPC запроса, выбрасывается HTTPException.

   Параметры:
   ----------
   uuid : str
       Уникальный идентификатор заказа.
   name : str
       Новое название заказа.
   completed : bool
       Новый статус выполнения заказа.
   date : str, optional
       Новая дата обновления заказа в формате строки (по умолчанию текущая дата и время в формате UTC с 'Z').
   client : Any, optional
       Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

   Возвращает:
   -----------
   JSONResponse
       JSON-ответ с обновленными данными заказа.

   Исключения:
   -----------
   HTTPException
       Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
   """
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
    """
    Удаляет заказ по UUID через gRPC сервис OrderService.

    Функция вызывает метод DeleteOrder gRPC сервиса OrderService для удаления заказа с указанным UUID.
    В случае ошибки gRPC запроса, выбрасывается HTTPException.

    Параметры:
    ----------
    uuid : str
        Уникальный идентификатор заказа.
    client : Any, optional
        Клиент gRPC для взаимодействия с сервисом OrderService (по умолчанию используется зависимость grpc_order_client).

    Возвращает:
    -----------
    JSONResponse
        JSON-ответ с данными об удалении заказа.

    Исключения:
    -----------
    HTTPException
        Исключение, выбрасываемое при ошибке gRPC запроса, с кодом состояния 404 и деталями ошибки.
    """
    try:
        order = await client.DeleteOrder(order_pb2.DeleteOrderRequest(uuid=uuid))
    except AioRpcError as e:
        raise HTTPException(status_code=404, detail=e.details())

    return JSONResponse(MessageToDict(order))
