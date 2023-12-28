
'Generated protocol buffer code.'
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from ....gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n sentinel/deposit/v1/events.proto\x12\x13sentinel.deposit.v1\x1a\x14gogoproto/gogo.proto"P\n\x08EventAdd\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\x1f\n\x05coins\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"coins""U\n\rEventSubtract\x12#\n\x07address\x18\x01 \x01(\tB\x12\xf2\xde\x1f\x0eyaml:"address"\x12\x1f\n\x05coins\x18\x02 \x01(\tB\x10\xf2\xde\x1f\x0cyaml:"coins"B:Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sentinel.deposit.v1.events_pb2', globals())
if (_descriptor._USE_C_DESCRIPTORS == False):
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'Z0github.com/sentinel-official/hub/x/deposit/types\xa8\xe2\x1e\x00\xc8\xe1\x1e\x00'
    _EVENTADD.fields_by_name['address']._options = None
    _EVENTADD.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTADD.fields_by_name['coins']._options = None
    _EVENTADD.fields_by_name['coins']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"coins"'
    _EVENTSUBTRACT.fields_by_name['address']._options = None
    _EVENTSUBTRACT.fields_by_name['address']._serialized_options = b'\xf2\xde\x1f\x0eyaml:"address"'
    _EVENTSUBTRACT.fields_by_name['coins']._options = None
    _EVENTSUBTRACT.fields_by_name['coins']._serialized_options = b'\xf2\xde\x1f\x0cyaml:"coins"'
    _EVENTADD._serialized_start = 79
    _EVENTADD._serialized_end = 159
    _EVENTSUBTRACT._serialized_start = 161
    _EVENTSUBTRACT._serialized_end = 246
