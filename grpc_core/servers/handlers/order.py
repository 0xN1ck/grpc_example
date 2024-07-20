import datetime

from loguru import logger

from models.order import Order
from grpc_core.servers.schemas.order import (OrderResponse, OrderCreateResponse, OrderListResponse, OrderReadResponse,
                                             OrderDeleteResponse)


class OrderHandler:
    def __init__(self):
        pass

    @staticmethod
    async def list_orders():
        orders = await Order.select()
        logger.success(f'List orders: {orders}')
        response = OrderListResponse(
            orders=[OrderResponse(**order) for order in orders]
        )
        return response

    @staticmethod
    async def create_order(request):
        order = await Order.insert(Order(**request.dict()))
        logger.success(f'Created order: {order}')
        response = OrderCreateResponse(
            order=OrderResponse(**order[0])
        )
        return response

    @staticmethod
    async def read_order(request):
        order = await Order.select().where(Order.uuid == request.uuid).first()
        logger.success(f'Read order: {order}')
        response = OrderReadResponse(order=OrderResponse(**order))
        return response

    @staticmethod
    async def update_order(request):
        await Order.update(
            {
                Order.name: request.name,
                Order.completed: request.completed,
                Order.date: request.date
            }
        ).where(Order.uuid == request.uuid)
        order = await Order.select().where(Order.uuid == request.uuid).first()
        logger.success(f'Update order: {order}')
        response = OrderReadResponse(
            order=OrderResponse(**order)
        )
        return response

    @staticmethod
    async def delete_order(request):
        if (order := await Order.select().where(Order.uuid == request.uuid).first()):
            await Order.delete().where(Order.uuid == request.uuid)
            logger.success(f'Delete order: {order}')
            response = OrderDeleteResponse(
                success=True
            )
            return response
        else:
            response = OrderDeleteResponse(
                success=False
            )
            return response

    @staticmethod
    async def update_after_check_order(request):
        await Order.update(
            {
                Order.completed: request.completed.value,
                Order.date: f"{datetime.datetime.utcnow()}Z"
            }
        ).where(Order.uuid == request.uuid)
        order = await Order.select().where(Order.uuid == request.uuid).first()
        logger.success(f'Update order: {order}')
        response = OrderReadResponse(
            order=OrderResponse(**order)
        )
        return response
