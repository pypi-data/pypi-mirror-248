
from gogoproto import gogo_pb2 as _gogo_pb2
from sentinel.types.v1 import status_pb2 as _status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class EventAllocate(_message.Message):
    __slots__ = ['address', 'granted_bytes', 'id', 'utilised_bytes']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    GRANTED_BYTES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    UTILISED_BYTES_FIELD_NUMBER: _ClassVar[int]
    address: str
    granted_bytes: str
    id: int
    utilised_bytes: str

    def __init__(self, address: _Optional[str]=..., granted_bytes: _Optional[str]=..., utilised_bytes: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventCreatePayout(_message.Message):
    __slots__ = ['address', 'id', 'node_address']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    node_address: str

    def __init__(self, address: _Optional[str]=..., node_address: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventPayForPayout(_message.Message):
    __slots__ = ['address', 'id', 'node_address', 'payment', 'staking_reward']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_FIELD_NUMBER: _ClassVar[int]
    STAKING_REWARD_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    node_address: str
    payment: str
    staking_reward: str

    def __init__(self, address: _Optional[str]=..., node_address: _Optional[str]=..., payment: _Optional[str]=..., staking_reward: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventPayForPlan(_message.Message):
    __slots__ = ['address', 'id', 'payment', 'provider_address', 'staking_reward']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STAKING_REWARD_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    payment: str
    provider_address: str
    staking_reward: str

    def __init__(self, address: _Optional[str]=..., payment: _Optional[str]=..., provider_address: _Optional[str]=..., staking_reward: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventPayForSession(_message.Message):
    __slots__ = ['address', 'node_address', 'payment', 'session_id', 'staking_reward', 'subscription_id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NODE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STAKING_REWARD_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    node_address: str
    payment: str
    session_id: int
    staking_reward: str
    subscription_id: int

    def __init__(self, address: _Optional[str]=..., node_address: _Optional[str]=..., payment: _Optional[str]=..., staking_reward: _Optional[str]=..., session_id: _Optional[int]=..., subscription_id: _Optional[int]=...) -> None:
        ...

class EventRefund(_message.Message):
    __slots__ = ['address', 'amount', 'id']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    amount: str
    id: int

    def __init__(self, address: _Optional[str]=..., amount: _Optional[str]=..., id: _Optional[int]=...) -> None:
        ...

class EventUpdateStatus(_message.Message):
    __slots__ = ['address', 'id', 'plan_id', 'status']
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    id: int
    plan_id: int
    status: _status_pb2.Status

    def __init__(self, status: _Optional[_Union[(_status_pb2.Status, str)]]=..., address: _Optional[str]=..., id: _Optional[int]=..., plan_id: _Optional[int]=...) -> None:
        ...
