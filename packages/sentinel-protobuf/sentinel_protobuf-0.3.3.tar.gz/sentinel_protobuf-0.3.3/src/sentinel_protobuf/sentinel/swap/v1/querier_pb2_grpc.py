
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.swap.v1 import querier_pb2 as sentinel_dot_swap_dot_v1_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QuerySwaps = channel.unary_unary('/sentinel.swap.v1.QueryService/QuerySwaps', request_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsRequest.SerializeToString, response_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsResponse.FromString)
        self.QuerySwap = channel.unary_unary('/sentinel.swap.v1.QueryService/QuerySwap', request_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapRequest.SerializeToString, response_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapResponse.FromString)
        self.QueryParams = channel.unary_unary('/sentinel.swap.v1.QueryService/QueryParams', request_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsRequest.SerializeToString, response_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QuerySwaps(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySwap(self, request, context):
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
    rpc_method_handlers = {'QuerySwaps': grpc.unary_unary_rpc_method_handler(servicer.QuerySwaps, request_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsRequest.FromString, response_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsResponse.SerializeToString), 'QuerySwap': grpc.unary_unary_rpc_method_handler(servicer.QuerySwap, request_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapRequest.FromString, response_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsRequest.FromString, response_serializer=sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.swap.v1.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QuerySwaps(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.swap.v1.QueryService/QuerySwaps', sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsRequest.SerializeToString, sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySwap(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.swap.v1.QueryService/QuerySwap', sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapRequest.SerializeToString, sentinel_dot_swap_dot_v1_dot_querier__pb2.QuerySwapResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.swap.v1.QueryService/QueryParams', sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsRequest.SerializeToString, sentinel_dot_swap_dot_v1_dot_querier__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
