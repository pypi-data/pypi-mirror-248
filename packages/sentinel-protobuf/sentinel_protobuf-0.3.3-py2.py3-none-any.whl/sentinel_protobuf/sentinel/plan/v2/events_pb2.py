
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ....sentinel.types.v1 import status_pb2 as sentinel_dot_types_dot_v1_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsentinel/plan/v2/events.proto\x12\x10sentinel.plan.v2\x1a\x14gogoproto/gogo.proto\x1a\x1esentinel/types/v1/status.proto"S\n\x0bEventCreate\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\x1f\n\x02id\x18\x02 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id""\x97\x01\n\x11EventUpdateStatus\x12<\n\x06status\x18\x01 \x01(\x0e2\x19.sentinel.types.v1.StatusB\x11\xf2\xde\x1f\ryaml:"status"\x12#\n\x07address\x18\x02 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\x1f\n\x02id\x18\x03 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id""\x84\x01\n\rEventLinkNode\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12-\n\x0cnode_address\x18\x02 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address"\x12\x1f\n\x02id\x18\x03 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id""\x86\x01\n\x0fEventUnlinkNode\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12-\n\x0cnode_address\x18\x02 \x01(\tB\x17\xf2\xde\x1f\x13yaml:"node_address"\x12\x1f\n\x02id\x18\x03 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id""\xc5\x01\n\x17EventCreateSubscription\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x125\n\x10provider_address\x18\x02 \x01(\tB\x1b\xf2\xde\x1f\x17yaml:"provider_address"\x12\x1f\n\x02id\x18\x03 \x01(\x04B\x13\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"\x12-\n\x07plan_id\x18\x04 \x01(\x04B\x1c\xe2\xde\x1f\x06PlanID\xf2\xde\x1f\x0eyaml:"plan_id"B7Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.plan.v2.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z-github.com/sentinel-official/hub/x/plan/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTCREATE.fields_by_name['address']._options = None
    _EVENTCREATE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTCREATE.fields_by_name['id']._options = None
    _EVENTCREATE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUPDATESTATUS.fields_by_name['status']._options = None
    _EVENTUPDATESTATUS.fields_by_name['status']._serialized_options = b'\xf2\xde\x1f\ryaml:"status"'
    _EVENTUPDATESTATUS.fields_by_name['address']._options = None
    _EVENTUPDATESTATUS.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUPDATESTATUS.fields_by_name['id']._options = None
    _EVENTUPDATESTATUS.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTLINKNODE.fields_by_name['address']._options = None
    _EVENTLINKNODE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTLINKNODE.fields_by_name['node_address']._options = None
    _EVENTLINKNODE.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTLINKNODE.fields_by_name['id']._options = None
    _EVENTLINKNODE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTUNLINKNODE.fields_by_name['address']._options = None
    _EVENTUNLINKNODE.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTUNLINKNODE.fields_by_name['node_address']._options = None
    _EVENTUNLINKNODE.fields_by_name['node_address']._serialized_options = b'\xf2\xde\x1f\x13yaml:"node_address"'
    _EVENTUNLINKNODE.fields_by_name['id']._options = None
    _EVENTUNLINKNODE.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['address']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['provider_address']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['provider_address']._serialized_options = b'\xf2\xde\x1f\x17yaml:"provider_address"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['id']._serialized_options = b'\xe2\xde\x1f\x02ID\xf2\xde\x1f\tyaml:"id"'
    _EVENTCREATESUBSCRIPTION.fields_by_name['plan_id']._options = None
    _EVENTCREATESUBSCRIPTION.fields_by_name['plan_id']._serialized_options = b'\xe2\xde\x1f\x06PlanID\xf2\xde\x1f\x0eyaml:"plan_id"'
    _EVENTCREATE._serialized_start = 105
    _EVENTCREATE._serialized_end = 188
    _EVENTUPDATESTATUS._serialized_start = 191
    _EVENTUPDATESTATUS._serialized_end = 342
    _EVENTLINKNODE._serialized_start = 345
    _EVENTLINKNODE._serialized_end = 477
    _EVENTUNLINKNODE._serialized_start = 480
    _EVENTUNLINKNODE._serialized_end = 614
    _EVENTCREATESUBSCRIPTION._serialized_start = 617
    _EVENTCREATESUBSCRIPTION._serialized_end = 814
