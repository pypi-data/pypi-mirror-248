
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
from ....sentinel.provider.v2 import params_pb2 as sentinel_dot_provider_dot_v2_dot_params__pb2
from ....sentinel.provider.v2 import provider_pb2 as sentinel_dot_provider_dot_v2_dot_provider__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n"sentinel/provider/v2/querier.proto\x12\x14sentinel.provider.v2\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1esentinel/types/v1/status.proto\x1a!sentinel/provider/v2/params.proto\x1a#sentinel/provider/v2/provider.proto"~\n\x15QueryProvidersRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest\x12)\n\x06status\x18\x02 \x01(\x0e2\x19.sentinel.types.v1.Status"\'\n\x14QueryProviderRequest\x12\x0f\n\x07address\x18\x01 \x01(\t"\x14\n\x12QueryParamsRequest"\x8e\x01\n\x16QueryProvidersResponse\x127\n\tproviders\x18\x01 \x03(\x0b2\x1e.sentinel.provider.v2.ProviderB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"O\n\x15QueryProviderResponse\x126\n\x08provider\x18\x01 \x01(\x0b2\x1e.sentinel.provider.v2.ProviderB\x04\xc8\xde\x1f\x00"I\n\x13QueryParamsResponse\x122\n\x06params\x18\x01 \x01(\x0b2\x1c.sentinel.provider.v2.ParamsB\x04\xc8\xde\x1f\x002\xb3\x03\n\x0cQueryService\x12\x88\x01\n\x0eQueryProviders\x12+.sentinel.provider.v2.QueryProvidersRequest\x1a,.sentinel.provider.v2.QueryProvidersResponse"\x1b\x82\xd3\xe4\x93\x02\x15\x12\x13/sentinel/providers\x12\x8f\x01\n\rQueryProvider\x12*.sentinel.provider.v2.QueryProviderRequest\x1a+.sentinel.provider.v2.QueryProviderResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/providers/{address}\x12\x85\x01\n\x0bQueryParams\x12(.sentinel.provider.v2.QueryParamsRequest\x1a).sentinel.provider.v2.QueryParamsResponse"!\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/params/providerB;Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.provider.v2.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z1github.com/sentinel-official/hub/x/provider/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYPROVIDERSRESPONSE.fields_by_name['providers']._options = None
    _QUERYPROVIDERSRESPONSE.fields_by_name['providers']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPROVIDERRESPONSE.fields_by_name['provider']._options = None
    _QUERYPROVIDERRESPONSE.fields_by_name['provider']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QueryProviders']._options = None
    _QUERYSERVICE.methods_by_name['QueryProviders']._serialized_options = b'\x82\xd3\xe4\x93\x02\x15\x12\x13/sentinel/providers'
    _QUERYSERVICE.methods_by_name['QueryProvider']._options = None
    _QUERYSERVICE.methods_by_name['QueryProvider']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/providers/{address}'
    _QUERYSERVICE.methods_by_name['QueryParams']._options = None
    _QUERYSERVICE.methods_by_name['QueryParams']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/params/provider'
    _QUERYPROVIDERSREQUEST._serialized_start = 260
    _QUERYPROVIDERSREQUEST._serialized_end = 386
    _QUERYPROVIDERREQUEST._serialized_start = 388
    _QUERYPROVIDERREQUEST._serialized_end = 427
    _QUERYPARAMSREQUEST._serialized_start = 429
    _QUERYPARAMSREQUEST._serialized_end = 449
    _QUERYPROVIDERSRESPONSE._serialized_start = 452
    _QUERYPROVIDERSRESPONSE._serialized_end = 594
    _QUERYPROVIDERRESPONSE._serialized_start = 596
    _QUERYPROVIDERRESPONSE._serialized_end = 675
    _QUERYPARAMSRESPONSE._serialized_start = 677
    _QUERYPARAMSRESPONSE._serialized_end = 750
    _QUERYSERVICE._serialized_start = 753
    _QUERYSERVICE._serialized_end = 1188
