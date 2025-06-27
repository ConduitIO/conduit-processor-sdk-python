from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Schema(_message.Message):
    __slots__ = ("subject", "version", "id", "type", "bytes")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[Schema.Type]
        TYPE_AVRO: _ClassVar[Schema.Type]
    TYPE_UNSPECIFIED: Schema.Type
    TYPE_AVRO: Schema.Type
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    subject: str
    version: int
    id: int
    type: Schema.Type
    bytes: bytes
    def __init__(self, subject: _Optional[str] = ..., version: _Optional[int] = ..., id: _Optional[int] = ..., type: _Optional[_Union[Schema.Type, str]] = ..., bytes: _Optional[bytes] = ...) -> None: ...
