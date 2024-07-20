import asyncio

from loguru import logger

from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode

from grpc_core.servers.utils import GrpcParseMessage
from grpc_core.protos.check import check_pb2
from grpc_core.protos.order import order_pb2
from grpc_core.protos.order import order_pb2_grpc
from grpc_core.servers.schemas.order import OrderCreateRequest, OrderReadRequest, OrderUpdateRequest
from grpc_core.servers.handlers.order import OrderHandler
from grpc_core.clients.check import grpc_check_client


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
        # Получаем трассировщик для текущего модуля
        tracer = trace.get_tracer(__name__)
        # Создаем и начинаем новый span для текущего метода ListOrders
        with tracer.start_as_current_span("ListOrders") as span:
            try:
                logger.info(f'Получен запрос на получение списка заказов')
                result = await OrderHandler.list_orders()
                response = self.message.dict_to_rpc(
                    data=result.dict(),  # Преобразуем результат в словарь
                    request_message=order_pb2.ListOrdersResponse(),  # Создаем новый экземпляр ListOrdersResponse
                )

                # Устанавливаем атрибут статус-кода RPC в span
                span.set_attribute("rpc.grpc.status_code", "OK")
                # Добавляем событие успешного ответа в span
                span.add_event("Successful response", {"response": str(response)})
                return response

            except Exception as e:
                # Устанавливаем статус span как ошибочный и добавляем сообщение об ошибке
                span.set_status(Status(StatusCode.ERROR, str(e)))
                # Добавляем событие ошибки в span с деталями об ошибке
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
        with tracer.start_as_current_span("ReadOrder") as span:
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
        with tracer.start_as_current_span("UpdateOrder") as span:
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
        with tracer.start_as_current_span("DeleteOrder") as span:
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

    async def CheckStatusOrder(self, request, context) -> order_pb2.UpdateOrderResponse:
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("OrderService.CheckStatusOrder") as span:
            metadata = context.invocation_metadata()
            auth = None
            for key, value in metadata:
                if key == 'rpc-auth':
                    auth = value

            await asyncio.sleep(1)
            logger.info(f'Осталось времени в цепочке вызовов: {context.time_remaining()}')

            client = await grpc_check_client(auth=auth)
            response = await client.CheckStatusOrder(
                check_pb2.CheckStatusOrderRequest(uuid=request.uuid),
                timeout=context.time_remaining()
            )

            await OrderHandler.update_after_check_order(response)

            span.set_attribute("rpc.grpc.status_code", "OK")
            span.add_event(
                "Successful response",
                {
                    "response": str({
                        "uuid": response.uuid,
                        "completed": response.completed.value,
                    })
                }
            )

            return response

