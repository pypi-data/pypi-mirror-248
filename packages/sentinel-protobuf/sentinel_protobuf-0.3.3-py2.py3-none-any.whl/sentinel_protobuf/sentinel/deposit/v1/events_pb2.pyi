
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional
DESCRIPTOR: _descriptor.FileDescriptor

class EventAdd(_message.Message):
    __slots__ = ['address', 'coins']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    address: str
    coins: str

    def __init__(self, address: _Optional[str]=..., coins: _Optional[str]=...) -> None:
        ...

class EventSubtract(_message.Message):
    __slots__ = ['address', 'coins']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    address: str
    coins: str

    def __init__(self, address: _Optional[str]=..., coins: _Optional[str]=...) -> None:
        ...
