import uuid
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class OrderNotificationEnum(Enum):
    ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED = 'ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED'
    ORDER_NOTIFICATION_TYPE_ENUM_OK = 'ORDER_NOTIFICATION_TYPE_ENUM_OK'


class OrderResponse(BaseModel):
    uuid: str
    name: str = None
    completed: bool = None
    date: str = None


class OrderListRequest(BaseModel):
    pass


class OrderListResponse(BaseModel):
    notification_type: str = OrderNotificationEnum.ORDER_NOTIFICATION_TYPE_ENUM_OK.value
    orders: List[OrderResponse]


class OrderCreateRequest(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    completed: bool
    date: str


class OrderCreateResponse(BaseModel):
    notification_type: str = OrderNotificationEnum.ORDER_NOTIFICATION_TYPE_ENUM_OK.value
    order: OrderResponse
    
    
class OrderReadRequest(BaseModel):
    uuid: str


class OrderReadResponse(BaseModel):
    notification_type: str = OrderNotificationEnum.ORDER_NOTIFICATION_TYPE_ENUM_OK.value
    order: OrderResponse


class OrderUpdateRequest(BaseModel):
    uuid: str
    name: str
    completed: bool
    date: str
    
    
class OrderDeleteRequest(BaseModel):
    uuid: str


class OrderDeleteResponse(BaseModel):
    notification_type: str = OrderNotificationEnum.ORDER_NOTIFICATION_TYPE_ENUM_OK.value
    success: bool
