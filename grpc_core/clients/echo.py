import grpc
# from fastapi import Request
from grpc_core.protos.echo import echo_pb2_grpc
from grpc_core.servers.interceptors import KeyAuthClientInterceptor
from settings import settings


async def grpc_echo_client(request):  # request: Request
    """
    Создает асинхронный gRPC клиент для сервиса OrderService.

    Эта функция создает незащищенный gRPC канал с сервером, используя параметры хоста и порта,
    указанные в настройках, и возвращает клиентский объект для взаимодействия с OrderService.

    Возвращает:
    -----------
    order_pb2_grpc.OrderServiceStub
        Клиентский объект для взаимодействия с gRPC сервисом OrderService.
    """
    auth = request.headers.get("rpc-auth")
    channel = grpc.aio.insecure_channel(
        f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}',
        interceptors=[
            KeyAuthClientInterceptor(auth),
        ],
    )
    client = echo_pb2_grpc.EchoServiceStub(channel)
    return client
