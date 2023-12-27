from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Word(_message.Message):
    __slots__ = ("f1", "f2")
    F1_FIELD_NUMBER: _ClassVar[int]
    F2_FIELD_NUMBER: _ClassVar[int]
    f1: str
    f2: str
    def __init__(self, f1: _Optional[str] = ..., f2: _Optional[str] = ...) -> None: ...
