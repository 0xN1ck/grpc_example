from functools import partial

import grpc
import jwt
from grpc.aio import ClientCallDetails


class AuthInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, key):
        # При инициализации создаем атрибут _valid_metadata,
        # который будет хранить секретный ключ для валидации токена пользователя
        self._valid_metadata = key

    @staticmethod
    async def deny(_, context, details):
        # Функция, предназначенная для отправки сообщений пользователю при отработках ошибок в функции intercept_service
        await context.abort(grpc.StatusCode.UNAUTHENTICATED, details)

    async def intercept_service(self, continuation, handler_call_details):
        # Получаем кортеж, содержащий метаданные
        metadatums = handler_call_details.invocation_metadata
        try:
            # Получаем токен из метаданных
            resault = next(filter(lambda x: x.key == 'rpc-auth', metadatums))
            if jwt.decode(resault.value, self._valid_metadata, algorithms=['HS256']):
                return await continuation(handler_call_details)
        except StopIteration:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Токен не найден"))
        except jwt.ExpiredSignatureError:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Время жизни токена истекло"))
        except jwt.InvalidTokenError:
            return grpc.unary_unary_rpc_method_handler(partial(self.deny, details="Токен не валиден"))


class KeyAuthClientInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(self, user_token):
        # Получаем токен пользователя
        self.user_token: str = user_token

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        # Добавляем токен в метаданные с ключом rpc-auth и отправляем запрос на сервер
        metadata = []
        if client_call_details.metadata is not None:
            metadata = list(client_call_details.metadata)
        metadata.append(("rpc-auth", self.user_token))
        new_details = ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            metadata,
            client_call_details.credentials,
            client_call_details.wait_for_ready,
        )
        response = await continuation(new_details, request)
        return response
