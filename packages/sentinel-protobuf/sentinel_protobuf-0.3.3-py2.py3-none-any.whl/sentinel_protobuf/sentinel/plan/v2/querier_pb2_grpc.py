
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.plan.v2 import querier_pb2 as sentinel_dot_plan_dot_v2_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QueryPlans = channel.unary_unary('/sentinel.plan.v2.QueryService/QueryPlans', request_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansRequest.SerializeToString, response_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansResponse.FromString)
        self.QueryPlansForProvider = channel.unary_unary('/sentinel.plan.v2.QueryService/QueryPlansForProvider', request_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderRequest.SerializeToString, response_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderResponse.FromString)
        self.QueryPlan = channel.unary_unary('/sentinel.plan.v2.QueryService/QueryPlan', request_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanRequest.SerializeToString, response_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QueryPlans(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPlansForProvider(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPlan(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'QueryPlans': grpc.unary_unary_rpc_method_handler(servicer.QueryPlans, request_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansRequest.FromString, response_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansResponse.SerializeToString), 'QueryPlansForProvider': grpc.unary_unary_rpc_method_handler(servicer.QueryPlansForProvider, request_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderRequest.FromString, response_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderResponse.SerializeToString), 'QueryPlan': grpc.unary_unary_rpc_method_handler(servicer.QueryPlan, request_deserializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanRequest.FromString, response_serializer=sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.plan.v2.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QueryPlans(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.plan.v2.QueryService/QueryPlans', sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansRequest.SerializeToString, sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPlansForProvider(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.plan.v2.QueryService/QueryPlansForProvider', sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderRequest.SerializeToString, sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlansForProviderResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPlan(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.plan.v2.QueryService/QueryPlan', sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanRequest.SerializeToString, sentinel_dot_plan_dot_v2_dot_querier__pb2.QueryPlanResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
