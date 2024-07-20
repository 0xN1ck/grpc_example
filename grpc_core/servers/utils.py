from google.protobuf.json_format import MessageToDict, ParseDict


class GrpcParseMessage:

    @staticmethod
    def rpc_to_dict(request) -> dict:
        """ Переводит ответ grpc сервера в json. """
        return MessageToDict(
            request,
            preserving_proto_field_name=True,
            use_integers_for_enums=False,
            # always_print_fields_with_no_presence=True
        )

    @staticmethod
    def dict_to_rpc(data: dict, request_message, ignore_unknown_fields: bool = True):
        """ Переводит json в запрос grpc сервера. """
        return ParseDict(
            data,
            request_message,
            ignore_unknown_fields=ignore_unknown_fields,
        )
