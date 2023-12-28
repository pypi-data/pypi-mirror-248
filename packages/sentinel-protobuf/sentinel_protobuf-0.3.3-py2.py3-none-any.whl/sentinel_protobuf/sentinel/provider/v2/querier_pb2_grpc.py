
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.provider.v2 import querier_pb2 as sentinel_dot_provider_dot_v2_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QueryProviders = channel.unary_unary('/sentinel.provider.v2.QueryService/QueryProviders', request_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersRequest.SerializeToString, response_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersResponse.FromString)
        self.QueryProvider = channel.unary_unary('/sentinel.provider.v2.QueryService/QueryProvider', request_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderRequest.SerializeToString, response_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderResponse.FromString)
        self.QueryParams = channel.unary_unary('/sentinel.provider.v2.QueryService/QueryParams', request_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, response_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QueryProviders(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryProvider(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryParams(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'QueryProviders': grpc.unary_unary_rpc_method_handler(servicer.QueryProviders, request_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersRequest.FromString, response_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersResponse.SerializeToString), 'QueryProvider': grpc.unary_unary_rpc_method_handler(servicer.QueryProvider, request_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderRequest.FromString, response_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsRequest.FromString, response_serializer=sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.provider.v2.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QueryProviders(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.provider.v2.QueryService/QueryProviders', sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersRequest.SerializeToString, sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProvidersResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryProvider(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.provider.v2.QueryService/QueryProvider', sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderRequest.SerializeToString, sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryProviderResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.provider.v2.QueryService/QueryParams', sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, sentinel_dot_provider_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
