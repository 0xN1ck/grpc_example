# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order/order.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from grpc_core.protos.check import check_pb2 as check_dot_check__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11order/order.proto\x12\x05order\x1a\x11\x63heck/check.proto\"D\n\x05Order\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tcompleted\x18\x03 \x01(\x08\x12\x0c\n\x04\x64\x61te\x18\x04 \x01(\t\"C\n\x12\x43reateOrderRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tcompleted\x18\x02 \x01(\x08\x12\x0c\n\x04\x64\x61te\x18\x03 \x01(\t\"o\n\x13\x43reateOrderResponse\x12;\n\x11notification_type\x18\x01 \x01(\x0e\x32 .order.OrderNotificationTypeEnum\x12\x1b\n\x05order\x18\x02 \x01(\x0b\x32\x0c.order.Order\" \n\x10ReadOrderRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"m\n\x11ReadOrderResponse\x12;\n\x11notification_type\x18\x01 \x01(\x0e\x32 .order.OrderNotificationTypeEnum\x12\x1b\n\x05order\x18\x02 \x01(\x0b\x32\x0c.order.Order\"Q\n\x12UpdateOrderRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tcompleted\x18\x03 \x01(\x08\x12\x0c\n\x04\x64\x61te\x18\x04 \x01(\t\"o\n\x13UpdateOrderResponse\x12;\n\x11notification_type\x18\x01 \x01(\x0e\x32 .order.OrderNotificationTypeEnum\x12\x1b\n\x05order\x18\x02 \x01(\x0b\x32\x0c.order.Order\"\"\n\x12\x44\x65leteOrderRequest\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"c\n\x13\x44\x65leteOrderResponse\x12;\n\x11notification_type\x18\x01 \x01(\x0e\x32 .order.OrderNotificationTypeEnum\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\x13\n\x11ListOrdersRequest\"o\n\x12ListOrdersResponse\x12;\n\x11notification_type\x18\x01 \x01(\x0e\x32 .order.OrderNotificationTypeEnum\x12\x1c\n\x06orders\x18\x02 \x03(\x0b\x32\x0c.order.Order*n\n\x19OrderNotificationTypeEnum\x12,\n(ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED\x10\x00\x12#\n\x1fORDER_NOTIFICATION_TYPE_ENUM_OK\x10\x01\x32\xb8\x03\n\x0cOrderService\x12\x44\n\x0b\x43reateOrder\x12\x19.order.CreateOrderRequest\x1a\x1a.order.CreateOrderResponse\x12>\n\tReadOrder\x12\x17.order.ReadOrderRequest\x1a\x18.order.ReadOrderResponse\x12\x44\n\x0bUpdateOrder\x12\x19.order.UpdateOrderRequest\x1a\x1a.order.UpdateOrderResponse\x12\x44\n\x0b\x44\x65leteOrder\x12\x19.order.DeleteOrderRequest\x1a\x1a.order.DeleteOrderResponse\x12\x41\n\nListOrders\x12\x18.order.ListOrdersRequest\x1a\x19.order.ListOrdersResponse\x12S\n\x10\x43heckStatusOrder\x12\x1e.check.CheckStatusOrderRequest\x1a\x1f.check.CheckStatusOrderResponseb\x06proto3')

_ORDERNOTIFICATIONTYPEENUM = DESCRIPTOR.enum_types_by_name['OrderNotificationTypeEnum']
OrderNotificationTypeEnum = enum_type_wrapper.EnumTypeWrapper(_ORDERNOTIFICATIONTYPEENUM)
ORDER_NOTIFICATION_TYPE_ENUM_UNSPECIFIED = 0
ORDER_NOTIFICATION_TYPE_ENUM_OK = 1


_ORDER = DESCRIPTOR.message_types_by_name['Order']
_CREATEORDERREQUEST = DESCRIPTOR.message_types_by_name['CreateOrderRequest']
_CREATEORDERRESPONSE = DESCRIPTOR.message_types_by_name['CreateOrderResponse']
_READORDERREQUEST = DESCRIPTOR.message_types_by_name['ReadOrderRequest']
_READORDERRESPONSE = DESCRIPTOR.message_types_by_name['ReadOrderResponse']
_UPDATEORDERREQUEST = DESCRIPTOR.message_types_by_name['UpdateOrderRequest']
_UPDATEORDERRESPONSE = DESCRIPTOR.message_types_by_name['UpdateOrderResponse']
_DELETEORDERREQUEST = DESCRIPTOR.message_types_by_name['DeleteOrderRequest']
_DELETEORDERRESPONSE = DESCRIPTOR.message_types_by_name['DeleteOrderResponse']
_LISTORDERSREQUEST = DESCRIPTOR.message_types_by_name['ListOrdersRequest']
_LISTORDERSRESPONSE = DESCRIPTOR.message_types_by_name['ListOrdersResponse']
Order = _reflection.GeneratedProtocolMessageType('Order', (_message.Message,), {
  'DESCRIPTOR' : _ORDER,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.Order)
  })
_sym_db.RegisterMessage(Order)

CreateOrderRequest = _reflection.GeneratedProtocolMessageType('CreateOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEORDERREQUEST,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.CreateOrderRequest)
  })
_sym_db.RegisterMessage(CreateOrderRequest)

CreateOrderResponse = _reflection.GeneratedProtocolMessageType('CreateOrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEORDERRESPONSE,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.CreateOrderResponse)
  })
_sym_db.RegisterMessage(CreateOrderResponse)

ReadOrderRequest = _reflection.GeneratedProtocolMessageType('ReadOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _READORDERREQUEST,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.ReadOrderRequest)
  })
_sym_db.RegisterMessage(ReadOrderRequest)

ReadOrderResponse = _reflection.GeneratedProtocolMessageType('ReadOrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _READORDERRESPONSE,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.ReadOrderResponse)
  })
_sym_db.RegisterMessage(ReadOrderResponse)

UpdateOrderRequest = _reflection.GeneratedProtocolMessageType('UpdateOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEORDERREQUEST,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.UpdateOrderRequest)
  })
_sym_db.RegisterMessage(UpdateOrderRequest)

UpdateOrderResponse = _reflection.GeneratedProtocolMessageType('UpdateOrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEORDERRESPONSE,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.UpdateOrderResponse)
  })
_sym_db.RegisterMessage(UpdateOrderResponse)

DeleteOrderRequest = _reflection.GeneratedProtocolMessageType('DeleteOrderRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEORDERREQUEST,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.DeleteOrderRequest)
  })
_sym_db.RegisterMessage(DeleteOrderRequest)

DeleteOrderResponse = _reflection.GeneratedProtocolMessageType('DeleteOrderResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEORDERRESPONSE,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.DeleteOrderResponse)
  })
_sym_db.RegisterMessage(DeleteOrderResponse)

ListOrdersRequest = _reflection.GeneratedProtocolMessageType('ListOrdersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTORDERSREQUEST,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.ListOrdersRequest)
  })
_sym_db.RegisterMessage(ListOrdersRequest)

ListOrdersResponse = _reflection.GeneratedProtocolMessageType('ListOrdersResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTORDERSRESPONSE,
  '__module__' : 'order.order_pb2'
  # @@protoc_insertion_point(class_scope:order.ListOrdersResponse)
  })
_sym_db.RegisterMessage(ListOrdersResponse)

_ORDERSERVICE = DESCRIPTOR.services_by_name['OrderService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ORDERNOTIFICATIONTYPEENUM._serialized_start=911
  _ORDERNOTIFICATIONTYPEENUM._serialized_end=1021
  _ORDER._serialized_start=47
  _ORDER._serialized_end=115
  _CREATEORDERREQUEST._serialized_start=117
  _CREATEORDERREQUEST._serialized_end=184
  _CREATEORDERRESPONSE._serialized_start=186
  _CREATEORDERRESPONSE._serialized_end=297
  _READORDERREQUEST._serialized_start=299
  _READORDERREQUEST._serialized_end=331
  _READORDERRESPONSE._serialized_start=333
  _READORDERRESPONSE._serialized_end=442
  _UPDATEORDERREQUEST._serialized_start=444
  _UPDATEORDERREQUEST._serialized_end=525
  _UPDATEORDERRESPONSE._serialized_start=527
  _UPDATEORDERRESPONSE._serialized_end=638
  _DELETEORDERREQUEST._serialized_start=640
  _DELETEORDERREQUEST._serialized_end=674
  _DELETEORDERRESPONSE._serialized_start=676
  _DELETEORDERRESPONSE._serialized_end=775
  _LISTORDERSREQUEST._serialized_start=777
  _LISTORDERSREQUEST._serialized_end=796
  _LISTORDERSRESPONSE._serialized_start=798
  _LISTORDERSRESPONSE._serialized_end=909
  _ORDERSERVICE._serialized_start=1024
  _ORDERSERVICE._serialized_end=1464
# @@protoc_insertion_point(module_scope)
