import asyncio

from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc


class HealthService(health_pb2_grpc.HealthServicer):
    # Асинхронный метод для проверки состояния.
    async def Check(self, request, context):
        # Возвращаем объект HealthCheckResponse со статусом SERVING, указывая, что сервис работает нормально
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING
        )

    # Асинхронный метод для подписки на обновления (мониторинга) состояния.
    async def Watch(self, request, context):
        while True:
            current_status = health_pb2.HealthCheckResponse.SERVING
            response = health_pb2.HealthCheckResponse(status=current_status)
            yield response
            await asyncio.sleep(1)
