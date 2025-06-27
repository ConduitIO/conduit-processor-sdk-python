from schema.v1 import schema_pb2 as _schema_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSchemaRequest(_message.Message):
    __slots__ = ("subject", "type", "bytes")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    subject: str
    type: _schema_pb2.Schema.Type
    bytes: bytes
    def __init__(self, subject: _Optional[str] = ..., type: _Optional[_Union[_schema_pb2.Schema.Type, str]] = ..., bytes: _Optional[bytes] = ...) -> None: ...

class CreateSchemaResponse(_message.Message):
    __slots__ = ("schema",)
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _schema_pb2.Schema
    def __init__(self, schema: _Optional[_Union[_schema_pb2.Schema, _Mapping]] = ...) -> None: ...

class GetSchemaRequest(_message.Message):
    __slots__ = ("subject", "version")
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    subject: str
    version: int
    def __init__(self, subject: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class GetSchemaResponse(_message.Message):
    __slots__ = ("schema",)
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    schema: _schema_pb2.Schema
    def __init__(self, schema: _Optional[_Union[_schema_pb2.Schema, _Mapping]] = ...) -> None: ...
