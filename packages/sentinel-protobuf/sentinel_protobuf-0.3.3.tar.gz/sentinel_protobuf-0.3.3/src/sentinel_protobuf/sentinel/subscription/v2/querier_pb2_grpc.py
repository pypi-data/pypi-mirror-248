
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.subscription.v2 import querier_pb2 as sentinel_dot_subscription_dot_v2_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QuerySubscriptions = channel.unary_unary('/sentinel.subscription.v2.QueryService/QuerySubscriptions', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsResponse.FromString)
        self.QuerySubscriptionsForAccount = channel.unary_unary('/sentinel.subscription.v2.QueryService/QuerySubscriptionsForAccount', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountResponse.FromString)
        self.QuerySubscriptionsForNode = channel.unary_unary('/sentinel.subscription.v2.QueryService/QuerySubscriptionsForNode', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeResponse.FromString)
        self.QuerySubscriptionsForPlan = channel.unary_unary('/sentinel.subscription.v2.QueryService/QuerySubscriptionsForPlan', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanResponse.FromString)
        self.QuerySubscription = channel.unary_unary('/sentinel.subscription.v2.QueryService/QuerySubscription', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionResponse.FromString)
        self.QueryAllocations = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryAllocations', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsResponse.FromString)
        self.QueryAllocation = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryAllocation', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationResponse.FromString)
        self.QueryPayouts = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryPayouts', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsResponse.FromString)
        self.QueryPayoutsForAccount = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryPayoutsForAccount', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountResponse.FromString)
        self.QueryPayoutsForNode = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryPayoutsForNode', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeResponse.FromString)
        self.QueryPayout = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryPayout', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutResponse.FromString)
        self.QueryParams = channel.unary_unary('/sentinel.subscription.v2.QueryService/QueryParams', request_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, response_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QuerySubscriptions(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySubscriptionsForAccount(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySubscriptionsForNode(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySubscriptionsForPlan(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuerySubscription(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryAllocations(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryAllocation(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPayouts(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPayoutsForAccount(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPayoutsForNode(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryPayout(self, request, context):
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
    rpc_method_handlers = {'QuerySubscriptions': grpc.unary_unary_rpc_method_handler(servicer.QuerySubscriptions, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsResponse.SerializeToString), 'QuerySubscriptionsForAccount': grpc.unary_unary_rpc_method_handler(servicer.QuerySubscriptionsForAccount, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountResponse.SerializeToString), 'QuerySubscriptionsForNode': grpc.unary_unary_rpc_method_handler(servicer.QuerySubscriptionsForNode, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeResponse.SerializeToString), 'QuerySubscriptionsForPlan': grpc.unary_unary_rpc_method_handler(servicer.QuerySubscriptionsForPlan, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanResponse.SerializeToString), 'QuerySubscription': grpc.unary_unary_rpc_method_handler(servicer.QuerySubscription, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionResponse.SerializeToString), 'QueryAllocations': grpc.unary_unary_rpc_method_handler(servicer.QueryAllocations, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsResponse.SerializeToString), 'QueryAllocation': grpc.unary_unary_rpc_method_handler(servicer.QueryAllocation, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationResponse.SerializeToString), 'QueryPayouts': grpc.unary_unary_rpc_method_handler(servicer.QueryPayouts, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsResponse.SerializeToString), 'QueryPayoutsForAccount': grpc.unary_unary_rpc_method_handler(servicer.QueryPayoutsForAccount, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountResponse.SerializeToString), 'QueryPayoutsForNode': grpc.unary_unary_rpc_method_handler(servicer.QueryPayoutsForNode, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeResponse.SerializeToString), 'QueryPayout': grpc.unary_unary_rpc_method_handler(servicer.QueryPayout, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutResponse.SerializeToString), 'QueryParams': grpc.unary_unary_rpc_method_handler(servicer.QueryParams, request_deserializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsRequest.FromString, response_serializer=sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.subscription.v2.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QuerySubscriptions(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QuerySubscriptions', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySubscriptionsForAccount(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QuerySubscriptionsForAccount', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForAccountResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySubscriptionsForNode(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QuerySubscriptionsForNode', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForNodeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySubscriptionsForPlan(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QuerySubscriptionsForPlan', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionsForPlanResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuerySubscription(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QuerySubscription', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QuerySubscriptionResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryAllocations(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryAllocations', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryAllocation(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryAllocation', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryAllocationResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPayouts(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryPayouts', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPayoutsForAccount(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryPayoutsForAccount', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForAccountResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPayoutsForNode(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryPayoutsForNode', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutsForNodeResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryPayout(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryPayout', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryPayoutResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryParams(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.subscription.v2.QueryService/QueryParams', sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsRequest.SerializeToString, sentinel_dot_subscription_dot_v2_dot_querier__pb2.QueryParamsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
