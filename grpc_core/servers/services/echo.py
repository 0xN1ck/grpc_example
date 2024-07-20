import asyncio
from loguru import logger

from grpc_core.protos.echo import echo_pb2
from grpc_core.protos.echo import echo_pb2_grpc

from grpc_core.servers.utils import GrpcParseMessage


class EchoService(echo_pb2_grpc.EchoServiceServicer):
    def __init__(self):
        self.message = GrpcParseMessage()

    # Асинхронный метод для обработки клиентского стрима.
    async def ClientStream(self, request_iterator, context) -> echo_pb2.DelayedReply:
        # Создание ответа с отложенным ответом.
        response = echo_pb2.DelayedReply()
        # Асинхронный цикл для обработки каждого запроса из стрима.
        async for request in request_iterator:
            logger.info(f'Приняли запрос от стрим клиента: {self.message.rpc_to_dict(request)}')
            response.response.append(request)
        return response

    # Асинхронный метод для обработки серверного стрима.
    async def ServerStream(self, request, context):
        logger.info(f'Приняли запрос от клиента: {self.message.rpc_to_dict(request)}')
        # Цикл для отправки нескольких ответов клиенту.
        for _ in range(3):
            # Отправка текущего запроса обратно в качестве ответа.
            yield request
            logger.info(f'Ответил стрим сервер: {self.message.rpc_to_dict(request)}')
            await asyncio.sleep(1)

    # Асинхронный метод для обработки двунаправленного стрима.
    async def BothStream(self, request_iterator, context):
        # Асинхронный цикл для обработки каждого запроса из стрима.
        async for request in request_iterator:
            logger.info(f'Приняли запрос от стрима клиента: {self.message.rpc_to_dict(request)}')
            # Цикл для отправки нескольких ответов клиенту на каждый запрос.
            for i in range(3):
                # Отправка текущего запроса обратно в качестве ответа.
                yield request
                logger.info(f'Ответил стрим сервер: {self.message.rpc_to_dict(request)}')
                # Асинхронная пауза на 1 секунду.
                await asyncio.sleep(1)

