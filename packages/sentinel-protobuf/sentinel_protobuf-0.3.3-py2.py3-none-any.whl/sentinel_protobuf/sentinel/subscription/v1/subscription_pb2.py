
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+sentinel/subscription/v1/subscription.proto\x12\x18sentinel.subscription.v1\x1a\x1ecosmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1esentinel/types/v1/status.proto"\x8e\x03\n\x0cSubscription\x12\n\n\x02id\x18\x01 \x01(\x04\x12\r\n\x05owner\x18\x02 \x01(\t\x12\x0c\n\x04node\x18\x03 \x01(\t\x12.\n\x05price\x18\x04 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x120\n\x07deposit\x18\x05 \x01(\x0b2\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00\x12\x0c\n\x04plan\x18\x06 \x01(\x04\x12\r\n\x05denom\x18\x07 \x01(\t\x124\n\x06expiry\x18\x08 \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12<\n\x04free\x18\t \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\x12)\n\x06status\x18\n \x01(\x0e2\x19.sentinel.types.v1.Status\x127\n\tstatus_at\x18\x0b \x01(\x0b2\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01BIZ?github.com/sentinel-official/hub/x/subscription/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.subscription.v1.subscription_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z?github.com/sentinel-official/hub/x/subscription/legacy/v1/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _SUBSCRIPTION.fields_by_name['price']._options = None
    _SUBSCRIPTION.fields_by_name['price']._serialized_options = b'\xc8\xde\x1f\x00'
    _SUBSCRIPTION.fields_by_name['deposit']._options = None
    _SUBSCRIPTION.fields_by_name['deposit']._serialized_options = b'\xc8\xde\x1f\x00'
    _SUBSCRIPTION.fields_by_name['expiry']._options = None
    _SUBSCRIPTION.fields_by_name['expiry']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _SUBSCRIPTION.fields_by_name['free']._options = None
    _SUBSCRIPTION.fields_by_name['free']._serialized_options = b'\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00'
    _SUBSCRIPTION.fields_by_name['status_at']._options = None
    _SUBSCRIPTION.fields_by_name['status_at']._serialized_options = b'\xc8\xde\x1f\x00\x90\xdf\x1f\x01'
    _SUBSCRIPTION._serialized_start = 193
    _SUBSCRIPTION._serialized_end = 591
