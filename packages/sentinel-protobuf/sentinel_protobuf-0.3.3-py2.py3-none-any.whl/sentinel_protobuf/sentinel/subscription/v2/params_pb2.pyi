
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class Params(_message.Message):
    __slots__ = ['status_change_delay']
    STATUS_CHANGE_DELAY_FIELD_NUMBER: _ClassVar[int]
    status_change_delay: _duration_pb2.Duration

    def __init__(self, status_change_delay: _Optional[_Union[(_duration_pb2.Duration, _Mapping)]]=...) -> None:
        ...
