from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from google.protobuf.json_format import MessageToDict, ParseDict
from grpc import aio

from grpc_core.protos.order import order_pb2
from grpc_core.protos.order import order_pb2_grpc
from grpc_core.servers.schemas.order import OrderCreateRequest, OrderReadRequest, OrderUpdateRequest
from grpc_core.servers.handlers.order import OrderHandler

from models.order import Order
from settings import settings


class GrpcParseMessage:

    @staticmethod
    def rpc_to_dict(request) -> dict:
        """ Переводит ответ grpc сервера в json """
        return MessageToDict(
            request,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            always_print_fields_with_no_presence=True
        )

    @staticmethod
    def dict_to_rpc(data: dict, request_message, ignore_unknown_fields: bool = True):
        """ Переводит json в запрос grpc сервера """
        return ParseDict(
            data,
            request_message,
            ignore_unknown_fields=ignore_unknown_fields,
        )


class OrderService(order_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.message = GrpcParseMessage()

    async def CreateOrder(self, request, context):
        request = OrderCreateRequest(**self.message.rpc_to_dict(request))
        logger.info(f'Received request is for create order: {request}')

        result = await OrderHandler.create_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.CreateOrderResponse(),
        )
        return response

    async def ListOrders(self, request, context):
        logger.info(f'Received request is for list orders')

        result = await OrderHandler.list_orders()

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.ListOrdersResponse(),
        )
        return response

    async def ReadOrder(self, request, context):
        logger.info(f'Received request is for read order: {request}')
        request = OrderReadRequest(**self.message.rpc_to_dict(request))

        result = await OrderHandler.read_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.ReadOrderResponse(),
        )
        return response

    async def UpdateOrder(self, request, context):
        logger.info(f'Received request is for update order: {request}')
        request = OrderUpdateRequest(**self.message.rpc_to_dict(request))

        result = await OrderHandler.update_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.UpdateOrderResponse(),
        )
        return response

    async def DeleteOrder(self, request, context):
        logger.info(f'Received request is for delete order: {request}')
        request = OrderReadRequest(**self.message.rpc_to_dict(request))

        result = await OrderHandler.delete_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.DeleteOrderResponse(),
        )
        return response


class Server:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.SERVER_ADDRESS = f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}'
            self.server = aio.server(ThreadPoolExecutor(max_workers=10))
            self.server.add_insecure_port(self.SERVER_ADDRESS)
            self.initialized = True

    def register(self):
        order_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderService(), self.server
        )

    async def run(self):
        await Order.create_table(if_not_exists=True)
        self.register()
        await self.server.start()
        logger.info(f'*** Service gRPC started: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

    async def stop(self):
        logger.info('*** Service gRPC stop ***')
        await self.server.stop(grace=False)
