from cn.luoyanze.word import word_pb2 as _word_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Hello(_message.Message):
    __slots__ = ("f1", "f2", "f3")
    F1_FIELD_NUMBER: _ClassVar[int]
    F2_FIELD_NUMBER: _ClassVar[int]
    F3_FIELD_NUMBER: _ClassVar[int]
    f1: str
    f2: str
    f3: _word_pb2.Word
    def __init__(self, f1: _Optional[str] = ..., f2: _Optional[str] = ..., f3: _Optional[_Union[_word_pb2.Word, _Mapping]] = ...) -> None: ...

class Foo(_message.Message):
    __slots__ = ("f1", "f2", "f3")
    F1_FIELD_NUMBER: _ClassVar[int]
    F2_FIELD_NUMBER: _ClassVar[int]
    F3_FIELD_NUMBER: _ClassVar[int]
    f1: str
    f2: str
    f3: _word_pb2.Word
    def __init__(self, f1: _Optional[str] = ..., f2: _Optional[str] = ..., f3: _Optional[_Union[_word_pb2.Word, _Mapping]] = ...) -> None: ...
