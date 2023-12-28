
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.node.v2 import querier_pb2 as sentinel_dot_node_dot_v2_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QueryNodes = channel.unary_unary('/sentinel.node.v2.QueryService/QueryNodes', request_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesRequest.SerializeToString, response_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesResponse.FromString)
        self.QueryNodesForPlan = channel.unary_unary('/sentinel.node.v2.QueryService/QueryNodesForPlan', request_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanRequest.SerializeToString, response_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanResponse.FromString)
        self.QueryNode = channel.unary_unary('/sentinel.node.v2.QueryService/QueryNode', request_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeRequest.SerializeToString, response_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeResponse.FromString)
        self.QueryParams = channel.unary_unary('/sentinel.node.v2.QueryService/QueryParams', request_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, response_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QueryNodes(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryNodesForPlan(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryNode(self, request, context):
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
    rpc_method_handlers = {'QueryNodes': grpc.unary_unary_rpc_method_handler(servicer.QueryNodes, request_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesRequest.FromString, response_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesResponse.SerializeToString), 'QueryNodesForPlan': grpc.unary_unary_rpc_method_handler(servicer.QueryNodesForPlan, request_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanRequest.FromString, response_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanResponse.SerializeToString), 'QueryNode': grpc.unary_unary_rpc_method_handler(servicer.QueryNode, request_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeRequest.FromString, response_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsRequest.FromString, response_serializer=sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.node.v2.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QueryNodes(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.node.v2.QueryService/QueryNodes', sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesRequest.SerializeToString, sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryNodesForPlan(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.node.v2.QueryService/QueryNodesForPlan', sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanRequest.SerializeToString, sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodesForPlanResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryNode(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.node.v2.QueryService/QueryNode', sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeRequest.SerializeToString, sentinel_dot_node_dot_v2_dot_querier__pb2.QueryNodeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.node.v2.QueryService/QueryParams', sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, sentinel_dot_node_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
