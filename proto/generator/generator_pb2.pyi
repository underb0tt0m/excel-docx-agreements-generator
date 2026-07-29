from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateRequest(_message.Message):
    __slots__ = ("archive",)
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    archive: bytes
    def __init__(self, archive: _Optional[bytes] = ...) -> None: ...

class GenerateResponse(_message.Message):
    __slots__ = ("zip_archive", "errors", "generated_count")
    ZIP_ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_COUNT_FIELD_NUMBER: _ClassVar[int]
    zip_archive: bytes
    errors: _containers.RepeatedCompositeFieldContainer[FileErrors]
    generated_count: int
    def __init__(self, zip_archive: _Optional[bytes] = ..., errors: _Optional[_Iterable[_Union[FileErrors, _Mapping]]] = ..., generated_count: _Optional[int] = ...) -> None: ...

class FileErrors(_message.Message):
    __slots__ = ("file_name", "errors")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    errors: _containers.RepeatedCompositeFieldContainer[FileError]
    def __init__(self, file_name: _Optional[str] = ..., errors: _Optional[_Iterable[_Union[FileError, _Mapping]]] = ...) -> None: ...

class FileError(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
