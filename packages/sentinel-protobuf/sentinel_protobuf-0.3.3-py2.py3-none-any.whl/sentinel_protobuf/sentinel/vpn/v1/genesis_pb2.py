
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.deposit.v1 import deposit_pb2 as sentinel_dot_deposit_dot_v1_dot_deposit__pb2
from ....sentinel.node.v2 import genesis_pb2 as sentinel_dot_node_dot_v2_dot_genesis__pb2
from ....sentinel.plan.v2 import genesis_pb2 as sentinel_dot_plan_dot_v2_dot_genesis__pb2
from ....sentinel.provider.v2 import genesis_pb2 as sentinel_dot_provider_dot_v2_dot_genesis__pb2
from ....sentinel.session.v2 import genesis_pb2 as sentinel_dot_session_dot_v2_dot_genesis__pb2
from ....sentinel.subscription.v2 import genesis_pb2 as sentinel_dot_subscription_dot_v2_dot_genesis__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsentinel/vpn/v1/genesis.proto\x12\x0fsentinel.vpn.v1\x1a\x14gogoproto/gogo.proto\x1a!sentinel/deposit/v1/deposit.proto\x1a\x1esentinel/node/v2/genesis.proto\x1a\x1esentinel/plan/v2/genesis.proto\x1a"sentinel/provider/v2/genesis.proto\x1a!sentinel/session/v2/genesis.proto\x1a&sentinel/subscription/v2/genesis.proto"\xd2\x02\n\x0cGenesisState\x124\n\x08deposits\x18\x01 \x03(\x0b2\x1c.sentinel.deposit.v1.DepositB\x04\xc8\xde\x1f\x00\x12-\n\x05nodes\x18\x02 \x01(\x0b2\x1e.sentinel.node.v2.GenesisState\x122\n\x05plans\x18\x03 \x03(\x0b2\x1d.sentinel.plan.v2.GenesisPlanB\x04\xc8\xde\x1f\x00\x125\n\tproviders\x18\x04 \x01(\x0b2".sentinel.provider.v2.GenesisState\x123\n\x08sessions\x18\x05 \x01(\x0b2!.sentinel.session.v2.GenesisState\x12=\n\rsubscriptions\x18\x06 \x01(\x0b2&.sentinel.subscription.v2.GenesisStateB6Z,github.com/sentinel-official/hub/x/vpn/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.vpn.v1.genesis_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z,github.com/sentinel-official/hub/x/vpn/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _GENESISSTATE.fields_by_name['deposits']._options = None
    _GENESISSTATE.fields_by_name['deposits']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE.fields_by_name['plans']._options = None
    _GENESISSTATE.fields_by_name['plans']._serialized_options = b'\xc8\xde\x1f\x00'
    _GENESISSTATE._serialized_start = 283
    _GENESISSTATE._serialized_end = 621
