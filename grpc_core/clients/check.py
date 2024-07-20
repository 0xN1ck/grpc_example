import grpc
from grpc_core.protos.check import check_pb2_grpc
from grpc_core.servers.interceptors import KeyAuthClientInterceptor
from settings import settings


async def grpc_check_client(auth: str):
    """
    Создает асинхронный gRPC клиент для сервиса OrderService.

    Эта функция создает незащищенный gRPC канал с сервером, используя параметры хоста и порта,
    указанные в настройках, и возвращает клиентский объект для взаимодействия с OrderService.

    Возвращает:
    -----------
    order_pb2_grpc.OrderServiceStub
        Клиентский объект для взаимодействия с gRPC сервисом OrderService.
    """
    channel = grpc.aio.insecure_channel(
        f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}',
        interceptors=[
            KeyAuthClientInterceptor(auth),
        ],
    )
    client = check_pb2_grpc.CheckStatusOrderServiceStub(channel)
    return client
