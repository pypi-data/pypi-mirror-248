
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.session.v2 import querier_pb2 as sentinel_dot_session_dot_v2_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QuerySessions = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySessions', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsResponse.FromString)
        self.QuerySessionsForAccount = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySessionsForAccount', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountResponse.FromString)
        self.QuerySessionsForNode = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySessionsForNode', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeResponse.FromString)
        self.QuerySessionsForSubscription = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySessionsForSubscription', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionResponse.FromString)
        self.QuerySessionsForAllocation = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySessionsForAllocation', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationResponse.FromString)
        self.QuerySession = channel.unary_unary('/sentinel.session.v2.QueryService/QuerySession', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionResponse.FromString)
        self.QueryParams = channel.unary_unary('/sentinel.session.v2.QueryService/QueryParams', request_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, response_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QuerySessions(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySessionsForAccount(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySessionsForNode(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySessionsForSubscription(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySessionsForAllocation(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySession(self, request, context):
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
    rpc_method_handlers = {'QuerySessions': grpc.unary_unary_rpc_method_handler(servicer.QuerySessions, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsResponse.SerializeToString), 'QuerySessionsForAccount': grpc.unary_unary_rpc_method_handler(servicer.QuerySessionsForAccount, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountResponse.SerializeToString), 'QuerySessionsForNode': grpc.unary_unary_rpc_method_handler(servicer.QuerySessionsForNode, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeResponse.SerializeToString), 'QuerySessionsForSubscription': grpc.unary_unary_rpc_method_handler(servicer.QuerySessionsForSubscription, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionResponse.SerializeToString), 'QuerySessionsForAllocation': grpc.unary_unary_rpc_method_handler(servicer.QuerySessionsForAllocation, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationResponse.SerializeToString), 'QuerySession': grpc.unary_unary_rpc_method_handler(servicer.QuerySession, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsRequest.FromString, response_serializer=sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.session.v2.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QuerySessions(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySessions', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySessionsForAccount(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySessionsForAccount', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAccountResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySessionsForNode(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySessionsForNode', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForNodeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySessionsForSubscription(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySessionsForSubscription', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForSubscriptionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySessionsForAllocation(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySessionsForAllocation', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionsForAllocationResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySession(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QuerySession', sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QuerySessionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.session.v2.QueryService/QueryParams', sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, sentinel_dot_session_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
