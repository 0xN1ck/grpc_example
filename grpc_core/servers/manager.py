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
        """ Переводит ответ grpc сервера в json. """
        return MessageToDict(
            request,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            always_print_fields_with_no_presence=True
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
        request = OrderCreateRequest(**self.message.rpc_to_dict(request))
        logger.info(f'Получен запрос на создание заказа: {request}')

        result = await OrderHandler.create_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.CreateOrderResponse(),
        )
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
        logger.info(f'Получен запрос на получение списка заказов')

        result = await OrderHandler.list_orders()

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.ListOrdersResponse(),
        )
        return response

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
        logger.info(f'Получен запрос на чтение заказа: {request}')
        request = OrderReadRequest(**self.message.rpc_to_dict(request))

        result = await OrderHandler.read_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.ReadOrderResponse(),
        )
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
        logger.info(f'Получен запрос на обновление заказа: {request}')
        request = OrderUpdateRequest(**self.message.rpc_to_dict(request))

        result = await OrderHandler.update_order(
            request=request
        )

        response = self.message.dict_to_rpc(
            data=result.dict(),
            request_message=order_pb2.UpdateOrderResponse(),
        )
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
        logger.info(f'Получен запрос на удаление заказа: {request}')
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
            self.SERVER_ADDRESS = f'{settings.GRPC_HOST_LOCAL}:{settings.GRPC_PORT}'
            self.server = aio.server(ThreadPoolExecutor(max_workers=10))
            self.server.add_insecure_port(self.SERVER_ADDRESS)
            self.initialized = True

    def register(self) -> None:
        """
        Регистрирует сервисы gRPC на сервере.

        Регистрирует сервис OrderService на gRPC сервере.
        """
        order_pb2_grpc.add_OrderServiceServicer_to_server(
            OrderService(), self.server
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
        Логгирует информацию о остановке сервера.
        """
        logger.info('*** Сервис gRPC остановлен ***')
        await self.server.stop(grace=False)
