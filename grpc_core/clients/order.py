import grpc
from fastapi import Request
from grpc_core.protos.order import order_pb2_grpc
from grpc_core.servers.interceptors import KeyAuthClientInterceptor
from settings import settings


async def grpc_order_client(request: Request):
    # Так как мы используем FastApi для демонстрации, прокинем токен в заголовок запроса
    auth = request.headers.get("rpc-auth")
    # При создании канала используем параметр interceptors для добавления нашего перехватчика, в который передаем токен
    channel = grpc.aio.insecure_channel(
        f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}',
        interceptors=[
            KeyAuthClientInterceptor(auth),
        ],
    )
    client = order_pb2_grpc.OrderServiceStub(channel)
    return client
