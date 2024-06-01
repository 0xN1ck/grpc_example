import grpc
from grpc_core.protos.order import order_pb2_grpc
from settings import settings


async def grpc_order_client():
    channel = grpc.aio.insecure_channel(f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}')
    client = order_pb2_grpc.OrderServiceStub(channel)
    return client
