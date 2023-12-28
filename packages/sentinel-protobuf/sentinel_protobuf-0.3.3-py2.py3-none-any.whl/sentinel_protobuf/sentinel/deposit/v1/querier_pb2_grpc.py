
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from ....sentinel.deposit.v1 import querier_pb2 as sentinel_dot_deposit_dot_v1_dot_querier__pb2

class QueryServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.QueryDeposits = channel.unary_unary('/sentinel.deposit.v1.QueryService/QueryDeposits', request_serializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsRequest.SerializeToString, response_deserializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsResponse.FromString)
        self.QueryDeposit = channel.unary_unary('/sentinel.deposit.v1.QueryService/QueryDeposit', request_serializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositRequest.SerializeToString, response_deserializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositResponse.FromString)

class QueryServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def QueryDeposits(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QueryDeposit(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'QueryDeposits': grpc.unary_unary_rpc_method_handler(servicer.QueryDeposits, request_deserializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsRequest.FromString, response_serializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsResponse.SerializeToString), 'QueryDeposit': grpc.unary_unary_rpc_method_handler(servicer.QueryDeposit, request_deserializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositRequest.FromString, response_serializer=sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('sentinel.deposit.v1.QueryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class QueryService(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def QueryDeposits(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.deposit.v1.QueryService/QueryDeposits', sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsRequest.SerializeToString, sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QueryDeposit(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sentinel.deposit.v1.QueryService/QueryDeposit', sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositRequest.SerializeToString, sentinel_dot_deposit_dot_v1_dot_querier__pb2.QueryDepositResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
