# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from grpc_core.protos.check import check_pb2 as check_dot_check__pb2
from grpc_core.protos.order import order_pb2 as order_dot_order__pb2


class OrderServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateOrder = channel.unary_unary(
                '/order.OrderService/CreateOrder',
                request_serializer=order_dot_order__pb2.CreateOrderRequest.SerializeToString,
                response_deserializer=order_dot_order__pb2.CreateOrderResponse.FromString,
                )
        self.ReadOrder = channel.unary_unary(
                '/order.OrderService/ReadOrder',
                request_serializer=order_dot_order__pb2.ReadOrderRequest.SerializeToString,
                response_deserializer=order_dot_order__pb2.ReadOrderResponse.FromString,
                )
        self.UpdateOrder = channel.unary_unary(
                '/order.OrderService/UpdateOrder',
                request_serializer=order_dot_order__pb2.UpdateOrderRequest.SerializeToString,
                response_deserializer=order_dot_order__pb2.UpdateOrderResponse.FromString,
                )
        self.DeleteOrder = channel.unary_unary(
                '/order.OrderService/DeleteOrder',
                request_serializer=order_dot_order__pb2.DeleteOrderRequest.SerializeToString,
                response_deserializer=order_dot_order__pb2.DeleteOrderResponse.FromString,
                )
        self.ListOrders = channel.unary_unary(
                '/order.OrderService/ListOrders',
                request_serializer=order_dot_order__pb2.ListOrdersRequest.SerializeToString,
                response_deserializer=order_dot_order__pb2.ListOrdersResponse.FromString,
                )
        self.CheckStatusOrder = channel.unary_unary(
                '/order.OrderService/CheckStatusOrder',
                request_serializer=check_dot_check__pb2.CheckStatusOrderRequest.SerializeToString,
                response_deserializer=check_dot_check__pb2.CheckStatusOrderResponse.FromString,
                )


class OrderServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOrders(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckStatusOrder(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateOrder,
                    request_deserializer=order_dot_order__pb2.CreateOrderRequest.FromString,
                    response_serializer=order_dot_order__pb2.CreateOrderResponse.SerializeToString,
            ),
            'ReadOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.ReadOrder,
                    request_deserializer=order_dot_order__pb2.ReadOrderRequest.FromString,
                    response_serializer=order_dot_order__pb2.ReadOrderResponse.SerializeToString,
            ),
            'UpdateOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateOrder,
                    request_deserializer=order_dot_order__pb2.UpdateOrderRequest.FromString,
                    response_serializer=order_dot_order__pb2.UpdateOrderResponse.SerializeToString,
            ),
            'DeleteOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteOrder,
                    request_deserializer=order_dot_order__pb2.DeleteOrderRequest.FromString,
                    response_serializer=order_dot_order__pb2.DeleteOrderResponse.SerializeToString,
            ),
            'ListOrders': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOrders,
                    request_deserializer=order_dot_order__pb2.ListOrdersRequest.FromString,
                    response_serializer=order_dot_order__pb2.ListOrdersResponse.SerializeToString,
            ),
            'CheckStatusOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckStatusOrder,
                    request_deserializer=check_dot_check__pb2.CheckStatusOrderRequest.FromString,
                    response_serializer=check_dot_check__pb2.CheckStatusOrderResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'order.OrderService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/CreateOrder',
            order_dot_order__pb2.CreateOrderRequest.SerializeToString,
            order_dot_order__pb2.CreateOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReadOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/ReadOrder',
            order_dot_order__pb2.ReadOrderRequest.SerializeToString,
            order_dot_order__pb2.ReadOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/UpdateOrder',
            order_dot_order__pb2.UpdateOrderRequest.SerializeToString,
            order_dot_order__pb2.UpdateOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/DeleteOrder',
            order_dot_order__pb2.DeleteOrderRequest.SerializeToString,
            order_dot_order__pb2.DeleteOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/ListOrders',
            order_dot_order__pb2.ListOrdersRequest.SerializeToString,
            order_dot_order__pb2.ListOrdersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckStatusOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/order.OrderService/CheckStatusOrder',
            check_dot_check__pb2.CheckStatusOrderRequest.SerializeToString,
            check_dot_check__pb2.CheckStatusOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
