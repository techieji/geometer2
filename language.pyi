from dataclasses import dataclass
from enum import Enum
from typing import Any
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

@dataclass
class ParseTree:
    is_literal: bool
    value: Token | list['ParseTree']
    def display(self) -> None: ...
type Environment = ChainMap
