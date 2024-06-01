from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderNotificationTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: _ClassVar[OrderNotificationTypeEnum]
    ORDER_NOTIFICATION_TYPE_ENUM_OK: _ClassVar[OrderNotificationTypeEnum]
ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED: OrderNotificationTypeEnum
ORDER_NOTIFICATION_TYPE_ENUM_OK: OrderNotificationTypeEnum

class Order(_message.Message):
    __slots__ = ("uuid", "name", "completed", "date")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    completed: bool
    date: str
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., completed: bool = ..., date: _Optional[str] = ...) -> None: ...

class CreateOrderRequest(_message.Message):
    __slots__ = ("name", "completed", "date")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    completed: bool
    date: str
    def __init__(self, name: _Optional[str] = ..., completed: bool = ..., date: _Optional[str] = ...) -> None: ...

class CreateOrderResponse(_message.Message):
    __slots__ = ("notification_type", "order")
    NOTIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    notification_type: OrderNotificationTypeEnum
    order: Order
    def __init__(self, notification_type: _Optional[_Union[OrderNotificationTypeEnum, str]] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class ReadOrderRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReadOrderResponse(_message.Message):
    __slots__ = ("notification_type", "order")
    NOTIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    notification_type: OrderNotificationTypeEnum
    order: Order
    def __init__(self, notification_type: _Optional[_Union[OrderNotificationTypeEnum, str]] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class UpdateOrderRequest(_message.Message):
    __slots__ = ("uuid", "name", "completed", "date")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    name: str
    completed: bool
    date: str
    def __init__(self, uuid: _Optional[str] = ..., name: _Optional[str] = ..., completed: bool = ..., date: _Optional[str] = ...) -> None: ...

class UpdateOrderResponse(_message.Message):
    __slots__ = ("notification_type", "order")
    NOTIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    notification_type: OrderNotificationTypeEnum
    order: Order
    def __init__(self, notification_type: _Optional[_Union[OrderNotificationTypeEnum, str]] = ..., order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class DeleteOrderRequest(_message.Message):
    __slots__ = ("uuid",)
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class DeleteOrderResponse(_message.Message):
    __slots__ = ("notification_type", "success")
    NOTIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    notification_type: OrderNotificationTypeEnum
    success: bool
    def __init__(self, notification_type: _Optional[_Union[OrderNotificationTypeEnum, str]] = ..., success: bool = ...) -> None: ...

class ListOrdersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOrdersResponse(_message.Message):
    __slots__ = ("notification_type", "orders")
    NOTIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    notification_type: OrderNotificationTypeEnum
    orders: _containers.RepeatedCompositeFieldContainer[Order]
    def __init__(self, notification_type: _Optional[_Union[OrderNotificationTypeEnum, str]] = ..., orders: _Optional[_Iterable[_Union[Order, _Mapping]]] = ...) -> None: ...
