
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from ....sentinel.swap.v1 import swap_pb2 as sentinel_dot_swap_dot_v1_dot_swap__pb2
from ....sentinel.swap.v1 import params_pb2 as sentinel_dot_swap_dot_v1_dot_params__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1esentinel/swap/v1/querier.proto\x12\x10sentinel.swap.v1\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bsentinel/swap/v1/swap.proto\x1a\x1dsentinel/swap/v1/params.proto"O\n\x11QuerySwapsRequest\x12:\n\npagination\x18\x01 \x01(\x0b2&.cosmos.base.query.v1beta1.PageRequest"#\n\x10QuerySwapRequest\x12\x0f\n\x07tx_hash\x18\x01 \x01(\x0c"\x14\n\x12QueryParamsRequest"~\n\x12QuerySwapsResponse\x12+\n\x05swaps\x18\x01 \x03(\x0b2\x16.sentinel.swap.v1.SwapB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b2\'.cosmos.base.query.v1beta1.PageResponse"?\n\x11QuerySwapResponse\x12*\n\x04swap\x18\x01 \x01(\x0b2\x16.sentinel.swap.v1.SwapB\x04\xc8\xde\x1f\x00"E\n\x13QueryParamsResponse\x12.\n\x06params\x18\x01 \x01(\x0b2\x18.sentinel.swap.v1.ParamsB\x04\xc8\xde\x1f\x002\xfd\x02\n\x0cQueryService\x12p\n\nQuerySwaps\x12#.sentinel.swap.v1.QuerySwapsRequest\x1a$.sentinel.swap.v1.QuerySwapsResponse"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/sentinel/swaps\x12w\n\tQuerySwap\x12".sentinel.swap.v1.QuerySwapRequest\x1a#.sentinel.swap.v1.QuerySwapResponse"!\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/swaps/{tx_hash}\x12\x81\x01\n\x0bQueryParams\x12$.sentinel.swap.v1.QueryParamsRequest\x1a%.sentinel.swap.v1.QueryParamsResponse"%\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/modules/swap/paramsB7Z-github.com/sentinel-official/hub/x/swap/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.swap.v1.querier_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/swap/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _QUERYSWAPSRESPONSE.fields_by_name['swaps']._options = None
    _QUERYSWAPSRESPONSE.fields_by_name['swaps']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSWAPRESPONSE.fields_by_name['swap']._options = None
    _QUERYSWAPRESPONSE.fields_by_name['swap']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYPARAMSRESPONSE.fields_by_name['params']._options = None
    _QUERYPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\xc8\xde\x1f\x00'
    _QUERYSERVICE.methods_by_name['QuerySwaps']._options = None
    _QUERYSERVICE.methods_by_name['QuerySwaps']._serialized_options = b'\x82\xd3\xe4\x93\x02\x11\x12\x0f/sentinel/swaps'
    _QUERYSERVICE.methods_by_name['QuerySwap']._options = None
    _QUERYSERVICE.methods_by_name['QuerySwap']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1b\x12\x19/sentinel/swaps/{tx_hash}'
    _QUERYSERVICE.methods_by_name['QueryParams']._options = None
    _QUERYSERVICE.methods_by_name['QueryParams']._serialized_options = b'\x82\xd3\xe4\x93\x02\x1f\x12\x1d/sentinel/modules/swap/params'
    _QUERYSWAPSREQUEST._serialized_start = 208
    _QUERYSWAPSREQUEST._serialized_end = 287
    _QUERYSWAPREQUEST._serialized_start = 289
    _QUERYSWAPREQUEST._serialized_end = 324
    _QUERYPARAMSREQUEST._serialized_start = 326
    _QUERYPARAMSREQUEST._serialized_end = 346
    _QUERYSWAPSRESPONSE._serialized_start = 348
    _QUERYSWAPSRESPONSE._serialized_end = 474
    _QUERYSWAPRESPONSE._serialized_start = 476
    _QUERYSWAPRESPONSE._serialized_end = 539
    _QUERYPARAMSRESPONSE._serialized_start = 541
    _QUERYPARAMSRESPONSE._serialized_end = 610
    _QUERYSERVICE._serialized_start = 613
    _QUERYSERVICE._serialized_end = 994
