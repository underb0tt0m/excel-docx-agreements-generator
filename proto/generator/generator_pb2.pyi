from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

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
    errors: _containers.RepeatedScalarFieldContainer[str]
    generated_count: int
    def __init__(self, zip_archive: _Optional[bytes] = ..., errors: _Optional[_Iterable[str]] = ..., generated_count: _Optional[int] = ...) -> None: ...
