import asyncio
import random
from loguru import logger

from google.protobuf.wrappers_pb2 import BoolValue

from opentelemetry import trace

from grpc_core.protos.check import check_pb2_grpc, check_pb2


class CheckStatusOrderService(check_pb2_grpc.CheckStatusOrderServiceServicer):
    async def CheckStatusOrder(self, request, context):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("CheckStatusOrder.CheckStatusOrder") as span:
            uuid = request.uuid

            await asyncio.sleep(1)
            logger.info(f'Осталось времени в цепочке вызовов: {context.time_remaining()}')

            response = check_pb2.CheckStatusOrderResponse(
                uuid=uuid,
                completed=BoolValue(value=random.choice([True, False])),
            )
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
