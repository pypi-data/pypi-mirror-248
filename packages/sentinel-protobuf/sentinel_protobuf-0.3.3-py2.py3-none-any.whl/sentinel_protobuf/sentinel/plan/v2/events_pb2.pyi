
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class EventCreate(_message.Message):
    __slots__ = ['address', 'id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int

    def __init__(self, address: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventCreateSubscription(_message.Message):
    __slots__ = ['address', 'id', 'plan_id', 'provider_address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    plan_id: int
    provider_address: str

    def __init__(self, address: _Optional[str]=..., provider_address: _Optional[str]=..., id: _Optional[int]=..., plan_id: _Optional[int]=...) -> None:
        ...

class EventLinkNode(_message.Message):
    __slots__ = ['address', 'id', 'node_address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    node_address: str

    def __init__(self, address: _Optional[str]=..., node_address: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventUnlinkNode(_message.Message):
    __slots__ = ['address', 'id', 'node_address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    node_address: str

    def __init__(self, address: _Optional[str]=..., node_address: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventUpdateStatus(_message.Message):
    __slots__ = ['address', 'id', 'status']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    status: _status_pb2.Status

    def __init__(self, status: _Optional[_Union[(_status_pb2.Status, str)]]=..., address: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...
