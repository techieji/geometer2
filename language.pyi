from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from collections import ChainMap

class TokenType(Enum):
    NUMBER = 0
    STRING = 1
    ATOM = 2
    BOOLEAN = 3
    POINT = 4
    CHARACTER = 5

@dataclass
class Token:
    kind: TokenType
    value: Any

type EvalResult = list[EvalResult] | int | float | bool | str | tuple[float, float] | Callable[[list[EvalResult]], EvalResult]

@dataclass
class ParseTree:
    is_literal: bool
    value: Token | list['ParseTree']
    def display(self) -> None: ...
    def to_python(self) -> EvalResult: ...

type Environment = ChainMap
