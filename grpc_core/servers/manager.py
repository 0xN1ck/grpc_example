import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.wrappers_pb2 import BoolValue
from grpc import aio
from grpc_reflection.v1alpha import reflection
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorServer, GrpcAioInstrumentorClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.proto.grpc import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace.status import Status, StatusCode

from grpc_core.protos.check import check_pb2_grpc, check_pb2
from grpc_core.protos.order import order_pb2
from grpc_core.protos.order import order_pb2_grpc
from grpc_core.protos.echo import echo_pb2
from grpc_core.protos.echo import echo_pb2_grpc
from grpc_core.servers.interceptors import AuthInterceptor
from grpc_core.servers.schemas.order import OrderCreateRequest, OrderReadRequest, OrderUpdateRequest
from grpc_core.servers.handlers.order import OrderHandler
from grpc_core.clients.check import grpc_check_client

from models.order import Order
from settings import settings


class GrpcParseMessage:

    @staticmethod
    def rpc_to_dict(request) -> dict:
        """ Переводит ответ grpc сервера в json. """
        return MessageToDict(
            request,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            # always_print_fields_with_no_presence=True
        )

    @staticmethod
    def dict_to_rpc(data: dict, request_message, ignore_unknown_fields: bool = True):
        """ Переводит json в запрос grpc сервера. """
        return ParseDict(
            data,
            request_message,
            ignore_unknown_fields=ignore_unknown_fields,
        )


class OrderService(order_pb2_grpc.OrderServiceServicer):
    """
    gRPC сервис для управления заказами, реализующий методы сервиса OrderService, описанные в order.proto.

    Методы:
    -------
    __init__() -> None
        Инициализация экземпляра OrderService. Создает объект для парсинга gRPC сообщений.

    async def CreateOrder(self, request, context)
        Обрабатывает gRPC запрос на создание заказа. Преобразует запрос в объект OrderCreateRequest,
        вызывает обработчик для создания заказа и возвращает ответ.

    async def ListOrders(self, request, context)
        Обрабатывает gRPC запрос на получение списка заказов. Вызывает обработчик для получения списка
        заказов и возвращает ответ.

    async def ReadOrder(self, request, context)
        Обрабатывает gRPC запрос на чтение заказа. Преобразует запрос в объект OrderReadRequest,
        вызывает обработчик для чтения заказа и возвращает ответ.

    async def UpdateOrder(self, request, context)
        Обрабатывает gRPC запрос на обновление заказа. Преобразует запрос в объект OrderUpdateRequest,
        вызывает обработчик для обновления заказа и возвращает ответ.

    async def DeleteOrder(self, request, context)
        Обрабатывает gRPC запрос на удаление заказа. Преобразует запрос в объект OrderReadRequest,
        вызывает обработчик для удаления заказа и возвращает ответ.
    """
    def __init__(self) -> None:
        """
        Инициализация экземпляра OrderService.

        Создает объект GrpcParseMessage для преобразования сообщений между
        форматами gRPC и внутренними форматами данных.
        """
        self.message = GrpcParseMessage()

    async def CreateOrder(self, request, context) -> order_pb2.CreateOrderResponse:
        """
        Обрабатывает gRPC запрос на создание заказа.

        Преобразует запрос из формата gRPC в объект OrderCreateRequest, передает его в обработчик
        OrderHandler.create_order для создания заказа и возвращает результат.

        Параметры:
        ----------
        request : order_pb2.CreateOrderRequest
            gRPC сообщение с данными для создания заказа.
        context : grpc.aio.ServicerContext
            Контекст сервиса gRPC, содержащий информацию о текущем RPC.

        Возвращает:
        -----------
        order_pb2.CreateOrderResponse
            gRPC сообщение с результатом операции создания заказа.

        Логгирует:
        ----------
        Информационное сообщение о полученном запросе на создание заказа.

        Исключения:
        -----------
        Может выбрасывать исключения в случае ошибок при обработке запроса.
        """
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CreateOrder") as span:
            request = OrderCreateRequest(**self.message.rpc_to_dict(request))
            logger.info(f'Получен запрос на создание заказа: {request}')

            result = await OrderHandler.create_order(
                request=request
            )

            response = self.message.dict_to_rpc(
                data=result.dict(),
                request_message=order_pb2.CreateOrderResponse(),
            )

            span.set_attribute("rpc.grpc.status_code", "OK")
            span.add_event("Successful response", {"response": str(response)})

            return response

    async def ListOrders(self, request, context) -> order_pb2.ListOrdersResponse:
        """
        Обрабатывает gRPC запрос на получение списка заказов.

        Вызывает обработчик OrderHandler.list_orders для получения списка заказов и возвращает результат.

        Параметры:
        ----------
        request : order_pb2.ListOrdersRequest
            gRPC сообщение с данными для запроса списка заказов.
        context : grpc.aio.ServicerContext
            Контекст сервиса gRPC, содержащий информацию о текущем RPC.

        Возвращает:
        -----------
        order_pb2.ListOrdersResponse
            gRPC сообщение с результатом операции получения списка заказов.

        Логгирует:
        ----------
        Информационное сообщение о полученном запросе на получение списка заказов.

        Исключения:
        -----------
        Может выбрасывать исключения в случае ошибок при обработке запроса.
        """
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CreateOrder") as span:
            try:
                logger.info(f'Получен запрос на получение списка заказов')

                result = await OrderHandler.list_orders()

                response = self.message.dict_to_rpc(
                    data=result.dict(),
                    request_message=order_pb2.ListOrdersResponse(),
                )

                span.set_attribute("rpc.grpc.status_code", "OK")
                span.add_event("Successful response", {"response": str(response)})

                return response

            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.add_event("Error response", {"error": str(e)})

    async def ReadOrder(self, request, context) -> order_pb2.ReadOrderResponse:
        """
        Обрабатывает gRPC запрос на чтение заказа.

        Преобразует запрос из формата gRPC в объект OrderReadRequest, передает его в обработчик OrderHandler.read_order
        для получения данных о заказе и возвращает результат.

        Параметры:
        ----------
        request : order_pb2.ReadOrderRequest
            gRPC сообщение с данными для чтения заказа.
        context : grpc.aio.ServicerContext
            Контекст сервиса gRPC, содержащий информацию о текущем RPC.

        Возвращает:
        -----------
        order_pb2.ReadOrderResponse
            gRPC сообщение с результатом операции чтения заказа.

        Логгирует:
        ----------
        Информационное сообщение о полученном запросе на чтение заказа.

        Исключения:
        -----------
        Может выбрасывать исключения в случае ошибок при обработке запроса.
        """
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CreateOrder") as span:
            logger.info(f'Получен запрос на чтение заказа: {request}')
            request = OrderReadRequest(**self.message.rpc_to_dict(request))

            result = await OrderHandler.read_order(
                request=request
            )

            response = self.message.dict_to_rpc(
                data=result.dict(),
                request_message=order_pb2.ReadOrderResponse(),
            )

            span.set_attribute("rpc.grpc.status_code", "OK")
            span.add_event("Successful response", {"response": str(response)})

            return response

    async def UpdateOrder(self, request, context) -> order_pb2.UpdateOrderResponse:
        """
        Обрабатывает gRPC запрос на обновление заказа.

        Преобразует запрос из формата gRPC в объект OrderUpdateRequest, передает его в обработчик
        OrderHandler.update_order для обновления данных заказа и возвращает результат.

        Параметры:
        ----------
        request : order_pb2.UpdateOrderRequest
            gRPC сообщение с данными для обновления заказа.
        context : grpc.aio.ServicerContext
            Контекст сервиса gRPC, содержащий информацию о текущем RPC.

        Возвращает:
        -----------
        order_pb2.UpdateOrderResponse
            gRPC сообщение с результатом операции обновления заказа.

        Логгирует:
        ----------
        Информационное сообщение о полученном запросе на обновление заказа.

        Исключения:
        -----------
        Может выбрасывать исключения в случае ошибок при обработке запроса.
        """
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CreateOrder") as span:
            logger.info(f'Получен запрос на обновление заказа: {request}')
            request = OrderUpdateRequest(**self.message.rpc_to_dict(request))

            result = await OrderHandler.update_order(
                request=request
            )

            response = self.message.dict_to_rpc(
                data=result.dict(),
                request_message=order_pb2.UpdateOrderResponse(),
            )

            span.set_attribute("rpc.grpc.status_code", "OK")
            span.add_event("Successful response", {"response": str(response)})

            return response

    async def DeleteOrder(self, request, context) -> order_pb2.DeleteOrderResponse:
        """
        Обрабатывает gRPC запрос на удаление заказа.

        Преобразует запрос из формата gRPC в объект OrderReadRequest, передает его в обработчик OrderHandler.delete_order
        для удаления заказа и возвращает результат в формате gRPC.

        Параметры:
        ----------
        request : order_pb2.DeleteOrderRequest
            gRPC сообщение с данными для удаления заказа.
        context : grpc.aio.ServicerContext
            Контекст сервиса gRPC, содержащий информацию о текущем RPC.

        Возвращает:
        -----------
        order_pb2.DeleteOrderResponse
            gRPC сообщение с результатом операции удаления заказа.

        Логгирует:
        ----------
        Информационное сообщение о полученном запросе на удаление заказа.

        Исключения:
        -----------
        Может выбрасывать исключения в случае ошибок при обработке запроса.
        """
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CreateOrder") as span:
            logger.info(f'Получен запрос на удаление заказа: {request}')
            request = OrderReadRequest(**self.message.rpc_to_dict(request))

            result = await OrderHandler.delete_order(
                request=request
            )

            response = self.message.dict_to_rpc(
                data=result.dict(),
                request_message=order_pb2.DeleteOrderResponse(),
            )

            span.set_attribute("rpc.grpc.status_code", "OK")
            span.add_event("Successful response", {"response": str(response)})

            return response

    async def CheckStatusOrder(self, request, context):
        metadata = context.invocation_metadata()
        auth = None
        for key, value in metadata:
            if key == 'rpc-auth':
                auth = value
        client = await grpc_check_client(auth=auth)
        response = await client.CheckStatusOrder(
            check_pb2.CheckStatusOrderRequest(uuid=request.uuid)
        )
        return response


class HealthService(health_pb2_grpc.HealthServicer):
    async def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )

    async def Watch(self, request, context):
        while True:
            current_status = health_pb2.HealthCheckResponse.SERVING
            response = health_pb2.HealthCheckResponse(status=current_status)
            yield response
            await asyncio.sleep(1)


class EchoService(echo_pb2_grpc.EchoServiceServicer):
    def __init__(self):
        self.message = GrpcParseMessage()

    async def ClientStream(self, request_iterator, context) -> echo_pb2.DelayedReply:
        response = echo_pb2.DelayedReply()
        async for request in request_iterator:
            logger.info(f'Приняли запрос от стрим клиента: {self.message.rpc_to_dict(request)}')
            response.response.append(request)
        return response

    async def ServerStream(self, request, context):
        logger.info(f'Приняли запрос от клиента: {self.message.rpc_to_dict(request)}')
        for _ in range(5):
            yield request
            logger.info(f'Ответил стрим сервер: {self.message.rpc_to_dict(request)}')
            await asyncio.sleep(3)

    async def BothStream(self, request_iterator, context):
        async for request in request_iterator:
            logger.info(f'Приняли запрос от стрима клиента: {self.message.rpc_to_dict(request)}')
            for i in range(5):
                yield request
                logger.info(f'Ответил стрим сервер: {self.message.rpc_to_dict(request)}')
                await asyncio.sleep(1)


class CheckStatusOrderService(check_pb2_grpc.CheckStatusOrderServiceServicer):
    async def CheckStatusOrder(self, request, context):
        uuid = request.uuid
        response = check_pb2.CheckStatusOrderResponse(
            uuid=uuid,
            status=BoolValue(value=random.choice([True, False])),
        )
        return response


class Server:
    """
    Singleton класс для настройки и запуска gRPC сервера.

    Класс обеспечивает создание единственного экземпляра сервера, который можно зарегистрировать и запустить.

    Атрибуты:
    ---------
    _instance : Server
        Приватный атрибут, содержащий единственный экземпляр класса Server.
    SERVER_ADDRESS : str
        Адрес сервера в формате 'host:port'.
    server : grpc.aio.Server
        Экземпляр асинхронного gRPC сервера.
    initialized : bool
        Флаг, указывающий, была ли выполнена инициализация.

    Методы:
    -------
    __new__(cls, *args, **kwargs)
        Создает и возвращает единственный экземпляр класса Server.
    __init__() -> None
        Инициализирует сервер, если он еще не инициализирован.
    register() -> None
        Регистрирует сервисы gRPC на сервере.
    async run() -> None
        Запускает сервер и ожидает его завершения.
    async stop() -> None
        Останавливает сервер.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Создает и возвращает единственный экземпляр класса Server.

        Если экземпляр уже существует, возвращает его. В противном случае создает новый экземпляр.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Инициализирует сервер, если он еще не инициализирован.

        Устанавливает адрес сервера, создает сервер gRPC и добавляет незащищенный порт.
        """
        if not hasattr(self, 'initialized'):
            jaeger_exporter = JaegerExporter(
                collector_endpoint=f'{settings.JAEGER_HOST}:{settings.JAEGER_PORT}',
                insecure=True
            )
            span_processor = BatchSpanProcessor(jaeger_exporter)
            trace.set_tracer_provider(
                TracerProvider(resource=Resource.create({SERVICE_NAME: "Order"}))
            )
            trace.get_tracer_provider().add_span_processor(span_processor)
            grpc_server_instrumentor = GrpcAioInstrumentorServer()
            grpc_server_instrumentor.instrument()
            grpc_client_instrumentor = GrpcAioInstrumentorClient()
            grpc_client_instrumentor.instrument()

            self.SERVER_ADDRESS = f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}'
            self.server = aio.server(
                ThreadPoolExecutor(max_workers=10),
                interceptors=[
                    AuthInterceptor(settings.SECRET_KEY),
                ]
            )
            self.server.add_insecure_port(self.SERVER_ADDRESS)

            SERVICE_NAMES = (
                order_pb2.DESCRIPTOR.services_by_name["OrderService"].full_name,
                echo_pb2.DESCRIPTOR.services_by_name["EchoService"].full_name,
                health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self.server)

            self.initialized = True

    def register(self) -> None:
        """
        Регистрирует сервисы gRPC на сервере.

        Регистрирует сервис OrderService на gRPC сервере.
        """
        order_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderService(), self.server
        )
        echo_pb2_grpc.add_EchoServiceServicer_to_server(
            EchoService(), self.server
        )
        health_pb2_grpc.add_HealthServicer_to_server(HealthService(), self.server),
        check_pb2_grpc.add_CheckStatusOrderServiceServicer_to_server(
            CheckStatusOrderService(), self.server
        )

    async def run(self) -> None:
        """
        Запускает сервер и ожидает его завершения.

        Создает таблицу Order, если она еще не существует, регистрирует сервисы и запускает сервер.
        Логгирует информацию о запуске сервера.
        """
        await Order.create_table(if_not_exists=True)
        self.register()
        await self.server.start()
        logger.info(f'*** Сервис gRPC запущен: {self.SERVER_ADDRESS} ***')
        await self.server.wait_for_termination()

    async def stop(self) -> None:
        """
        Останавливает сервер.

        Останавливает gRPC сервер без периода ожидания (grace period).
        Логгирует информацию об остановке сервера.
        """
        logger.info('*** Сервис gRPC остановлен ***')
        await self.server.stop(grace=False)
