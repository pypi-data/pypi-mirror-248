
from ibc.core.client.v1 import client_pb2 as _client_pb2
from cosmos.base.query.v1beta1 import pagination_pb2 as _pagination_pb2
from ibc.core.channel.v1 import channel_pb2 as _channel_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import any_pb2 as _any_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
DESCRIPTOR: _descriptor.FileDescriptor

class QueryChannelClientStateRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=...) -> None:
        ...

class QueryChannelClientStateResponse(_message.Message):
    __slots__ = ['identified_client_state', 'proof', 'proof_height']
    IDENTIFIED_CLIENT_STATE_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    identified_client_state: _client_pb2.IdentifiedClientState
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, identified_client_state: _Optional[_Union[(_client_pb2.IdentifiedClientState, _Mapping)]]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryChannelConsensusStateRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id', 'revision_height', 'revision_number']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    REVISION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    revision_height: int
    revision_number: int

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., revision_number: _Optional[int]=..., revision_height: _Optional[int]=...) -> None:
        ...

class QueryChannelConsensusStateResponse(_message.Message):
    __slots__ = ['client_id', 'consensus_state', 'proof', 'proof_height']
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONSENSUS_STATE_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    consensus_state: _any_pb2.Any
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, consensus_state: _Optional[_Union[(_any_pb2.Any, _Mapping)]]=..., client_id: _Optional[str]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryChannelRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=...) -> None:
        ...

class QueryChannelResponse(_message.Message):
    __slots__ = ['channel', 'proof', 'proof_height']
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    channel: _channel_pb2.Channel
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, channel: _Optional[_Union[(_channel_pb2.Channel, _Mapping)]]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryChannelsRequest(_message.Message):
    __slots__ = ['pagination']
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    pagination: _pagination_pb2.PageRequest

    def __init__(self, pagination: _Optional[_Union[(_pagination_pb2.PageRequest, _Mapping)]]=...) -> None:
        ...

class QueryChannelsResponse(_message.Message):
    __slots__ = ['channels', 'height', 'pagination']
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[_channel_pb2.IdentifiedChannel]
    height: _client_pb2.Height
    pagination: _pagination_pb2.PageResponse

    def __init__(self, channels: _Optional[_Iterable[_Union[(_channel_pb2.IdentifiedChannel, _Mapping)]]]=..., pagination: _Optional[_Union[(_pagination_pb2.PageResponse, _Mapping)]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryConnectionChannelsRequest(_message.Message):
    __slots__ = ['connection', 'pagination']
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    connection: str
    pagination: _pagination_pb2.PageRequest

    def __init__(self, connection: _Optional[str]=..., pagination: _Optional[_Union[(_pagination_pb2.PageRequest, _Mapping)]]=...) -> None:
        ...

class QueryConnectionChannelsResponse(_message.Message):
    __slots__ = ['channels', 'height', 'pagination']
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[_channel_pb2.IdentifiedChannel]
    height: _client_pb2.Height
    pagination: _pagination_pb2.PageResponse

    def __init__(self, channels: _Optional[_Iterable[_Union[(_channel_pb2.IdentifiedChannel, _Mapping)]]]=..., pagination: _Optional[_Union[(_pagination_pb2.PageResponse, _Mapping)]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryNextSequenceReceiveRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=...) -> None:
        ...

class QueryNextSequenceReceiveResponse(_message.Message):
    __slots__ = ['next_sequence_receive', 'proof', 'proof_height']
    NEXT_SEQUENCE_RECEIVE_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    next_sequence_receive: int
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, next_sequence_receive: _Optional[int]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryPacketAcknowledgementRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id', 'sequence']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    sequence: int

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., sequence: _Optional[int]=...) -> None:
        ...

class QueryPacketAcknowledgementResponse(_message.Message):
    __slots__ = ['acknowledgement', 'proof', 'proof_height']
    ACKNOWLEDGEMENT_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    acknowledgement: bytes
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, acknowledgement: _Optional[bytes]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryPacketAcknowledgementsRequest(_message.Message):
    __slots__ = ['channel_id', 'packet_commitment_sequences', 'pagination', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PACKET_COMMITMENT_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    packet_commitment_sequences: _containers.RepeatedScalarFieldContainer[int]
    pagination: _pagination_pb2.PageRequest
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., pagination: _Optional[_Union[(_pagination_pb2.PageRequest, _Mapping)]]=..., packet_commitment_sequences: _Optional[_Iterable[int]]=...) -> None:
        ...

class QueryPacketAcknowledgementsResponse(_message.Message):
    __slots__ = ['acknowledgements', 'height', 'pagination']
    ACKNOWLEDGEMENTS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    acknowledgements: _containers.RepeatedCompositeFieldContainer[_channel_pb2.PacketState]
    height: _client_pb2.Height
    pagination: _pagination_pb2.PageResponse

    def __init__(self, acknowledgements: _Optional[_Iterable[_Union[(_channel_pb2.PacketState, _Mapping)]]]=..., pagination: _Optional[_Union[(_pagination_pb2.PageResponse, _Mapping)]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryPacketCommitmentRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id', 'sequence']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    sequence: int

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., sequence: _Optional[int]=...) -> None:
        ...

class QueryPacketCommitmentResponse(_message.Message):
    __slots__ = ['commitment', 'proof', 'proof_height']
    COMMITMENT_FIELD_NUMBER: _ClassVar[int]
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    commitment: bytes
    proof: bytes
    proof_height: _client_pb2.Height

    def __init__(self, commitment: _Optional[bytes]=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryPacketCommitmentsRequest(_message.Message):
    __slots__ = ['channel_id', 'pagination', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    pagination: _pagination_pb2.PageRequest
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., pagination: _Optional[_Union[(_pagination_pb2.PageRequest, _Mapping)]]=...) -> None:
        ...

class QueryPacketCommitmentsResponse(_message.Message):
    __slots__ = ['commitments', 'height', 'pagination']
    COMMITMENTS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    commitments: _containers.RepeatedCompositeFieldContainer[_channel_pb2.PacketState]
    height: _client_pb2.Height
    pagination: _pagination_pb2.PageResponse

    def __init__(self, commitments: _Optional[_Iterable[_Union[(_channel_pb2.PacketState, _Mapping)]]]=..., pagination: _Optional[_Union[(_pagination_pb2.PageResponse, _Mapping)]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryPacketReceiptRequest(_message.Message):
    __slots__ = ['channel_id', 'port_id', 'sequence']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    port_id: str
    sequence: int

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., sequence: _Optional[int]=...) -> None:
        ...

class QueryPacketReceiptResponse(_message.Message):
    __slots__ = ['proof', 'proof_height', 'received']
    PROOF_FIELD_NUMBER: _ClassVar[int]
    PROOF_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    proof: bytes
    proof_height: _client_pb2.Height
    received: bool

    def __init__(self, received: bool=..., proof: _Optional[bytes]=..., proof_height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryUnreceivedAcksRequest(_message.Message):
    __slots__ = ['channel_id', 'packet_ack_sequences', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PACKET_ACK_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    packet_ack_sequences: _containers.RepeatedScalarFieldContainer[int]
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., packet_ack_sequences: _Optional[_Iterable[int]]=...) -> None:
        ...

class QueryUnreceivedAcksResponse(_message.Message):
    __slots__ = ['height', 'sequences']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    height: _client_pb2.Height
    sequences: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, sequences: _Optional[_Iterable[int]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...

class QueryUnreceivedPacketsRequest(_message.Message):
    __slots__ = ['channel_id', 'packet_commitment_sequences', 'port_id']
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    PACKET_COMMITMENT_SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    PORT_ID_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    packet_commitment_sequences: _containers.RepeatedScalarFieldContainer[int]
    port_id: str

    def __init__(self, port_id: _Optional[str]=..., channel_id: _Optional[str]=..., packet_commitment_sequences: _Optional[_Iterable[int]]=...) -> None:
        ...

class QueryUnreceivedPacketsResponse(_message.Message):
    __slots__ = ['height', 'sequences']
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SEQUENCES_FIELD_NUMBER: _ClassVar[int]
    height: _client_pb2.Height
    sequences: _containers.RepeatedScalarFieldContainer[int]

    def __init__(self, sequences: _Optional[_Iterable[int]]=..., height: _Optional[_Union[(_client_pb2.Height, _Mapping)]]=...) -> None:
        ...
