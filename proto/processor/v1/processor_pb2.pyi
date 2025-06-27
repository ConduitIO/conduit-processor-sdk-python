from config.v1 import parameter_pb2 as _parameter_pb2
from opencdc.v1 import opencdc_pb2 as _opencdc_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandRequest(_message.Message):
    __slots__ = ("specify", "configure", "open", "process", "teardown")
    SPECIFY_FIELD_NUMBER: _ClassVar[int]
    CONFIGURE_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FIELD_NUMBER: _ClassVar[int]
    TEARDOWN_FIELD_NUMBER: _ClassVar[int]
    specify: Specify.Request
    configure: Configure.Request
    open: Open.Request
    process: Process.Request
    teardown: Teardown.Request
    def __init__(self, specify: _Optional[_Union[Specify.Request, _Mapping]] = ..., configure: _Optional[_Union[Configure.Request, _Mapping]] = ..., open: _Optional[_Union[Open.Request, _Mapping]] = ..., process: _Optional[_Union[Process.Request, _Mapping]] = ..., teardown: _Optional[_Union[Teardown.Request, _Mapping]] = ...) -> None: ...

class CommandResponse(_message.Message):
    __slots__ = ("error", "specify", "configure", "open", "process", "teardown")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SPECIFY_FIELD_NUMBER: _ClassVar[int]
    CONFIGURE_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FIELD_NUMBER: _ClassVar[int]
    TEARDOWN_FIELD_NUMBER: _ClassVar[int]
    error: Error
    specify: Specify.Response
    configure: Configure.Response
    open: Open.Response
    process: Process.Response
    teardown: Teardown.Response
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., specify: _Optional[_Union[Specify.Response, _Mapping]] = ..., configure: _Optional[_Union[Configure.Response, _Mapping]] = ..., open: _Optional[_Union[Open.Response, _Mapping]] = ..., process: _Optional[_Union[Process.Response, _Mapping]] = ..., teardown: _Optional[_Union[Teardown.Response, _Mapping]] = ...) -> None: ...

class Specify(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Response(_message.Message):
        __slots__ = ("name", "summary", "description", "version", "author", "parameters")
        class ParametersEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: _parameter_pb2.Parameter
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_parameter_pb2.Parameter, _Mapping]] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        SUMMARY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        AUTHOR_FIELD_NUMBER: _ClassVar[int]
        PARAMETERS_FIELD_NUMBER: _ClassVar[int]
        name: str
        summary: str
        description: str
        version: str
        author: str
        parameters: _containers.MessageMap[str, _parameter_pb2.Parameter]
        def __init__(self, name: _Optional[str] = ..., summary: _Optional[str] = ..., description: _Optional[str] = ..., version: _Optional[str] = ..., author: _Optional[str] = ..., parameters: _Optional[_Mapping[str, _parameter_pb2.Parameter]] = ...) -> None: ...
    def __init__(self) -> None: ...

class Configure(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("parameters",)
        class ParametersEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        PARAMETERS_FIELD_NUMBER: _ClassVar[int]
        parameters: _containers.ScalarMap[str, str]
        def __init__(self, parameters: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    def __init__(self) -> None: ...

class Open(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Response(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    def __init__(self) -> None: ...

class Process(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ("records",)
        RECORDS_FIELD_NUMBER: _ClassVar[int]
        records: _containers.RepeatedCompositeFieldContainer[_opencdc_pb2.Record]
        def __init__(self, records: _Optional[_Iterable[_Union[_opencdc_pb2.Record, _Mapping]]] = ...) -> None: ...
    class Response(_message.Message):
        __slots__ = ("records",)
        RECORDS_FIELD_NUMBER: _ClassVar[int]
        records: _containers.RepeatedCompositeFieldContainer[Process.ProcessedRecord]
        def __init__(self, records: _Optional[_Iterable[_Union[Process.ProcessedRecord, _Mapping]]] = ...) -> None: ...
    class ProcessedRecord(_message.Message):
        __slots__ = ("single_record", "filter_record", "error_record", "multi_record")
        SINGLE_RECORD_FIELD_NUMBER: _ClassVar[int]
        FILTER_RECORD_FIELD_NUMBER: _ClassVar[int]
        ERROR_RECORD_FIELD_NUMBER: _ClassVar[int]
        MULTI_RECORD_FIELD_NUMBER: _ClassVar[int]
        single_record: _opencdc_pb2.Record
        filter_record: Process.FilterRecord
        error_record: Process.ErrorRecord
        multi_record: Process.MultiRecord
        def __init__(self, single_record: _Optional[_Union[_opencdc_pb2.Record, _Mapping]] = ..., filter_record: _Optional[_Union[Process.FilterRecord, _Mapping]] = ..., error_record: _Optional[_Union[Process.ErrorRecord, _Mapping]] = ..., multi_record: _Optional[_Union[Process.MultiRecord, _Mapping]] = ...) -> None: ...
    class FilterRecord(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class ErrorRecord(_message.Message):
        __slots__ = ("error",)
        ERROR_FIELD_NUMBER: _ClassVar[int]
        error: Error
        def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...
    class MultiRecord(_message.Message):
        __slots__ = ("records",)
        RECORDS_FIELD_NUMBER: _ClassVar[int]
        records: _containers.RepeatedCompositeFieldContainer[_opencdc_pb2.Record]
        def __init__(self, records: _Optional[_Iterable[_Union[_opencdc_pb2.Record, _Mapping]]] = ...) -> None: ...
    def __init__(self) -> None: ...

class Teardown(_message.Message):
    __slots__ = ()
    class Request(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class Response(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    def __init__(self) -> None: ...

class Error(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
