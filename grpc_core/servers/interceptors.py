from functools import partial

import grpc
import jwt
from grpc.aio import ClientCallDetails

from settings import settings


class AuthInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, key):
        self._valid_metadata = key

    @staticmethod
    async def deny(_, context, details):
        await context.abort(grpc.StatusCode.UNAUTHENTICATED, details)

        # self._deny = grpc.unary_unary_rpc_method_handler(deny)

    async def intercept_service(self, continuation, handler_call_details):
        metadatums = handler_call_details.invocation_metadata
        try:
            resault = next(filter(lambda x: x.key == 'rpc-auth', metadatums))
            if jwt.decode(resault.value, settings.SECRET_KEY, algorithms=['HS256']):
                return await continuation(handler_call_details)
        except StopIteration:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Токен не найден"))
        except jwt.ExpiredSignatureError:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Время жизни токена истекло"))
        except jwt.InvalidTokenError:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Токен не валиден"))


class KeyAuthClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, secret_key):
        self.secret_key: str = secret_key

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(("rpc-auth", self.secret_key))
        new_details = ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )
        response = await continuation(new_details, request)
        return response
