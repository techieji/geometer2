from enum import Enum
from typing import Any, Iterable

class TokenType(Enum):
    NUMBER = 0
    STRING = 1
    ATOM = 2
    BOOLEAN = 3
    POINT = 4
    CHARACTER = 5        # represents parentheses, quotes, unquote, quasiquotes, etc.

class Token:
    kind: TokenType
    value: Any

class ParseTree:
    is_literal: bool
    value: Token | list[ParseTree]
    # value is of type Token if is_literal is true; otherwise, it is a list of ParseTrees.

type Environment = ChainMap

def make_global_environment() -> Environment: ...

def lex(program: str) -> Iterable[Token]: ...
def parse(tokens: Iterable[Token]) -> ParseTree: ...
def execute(parse_tree: ParseTree, environment: Environment) -> Token: ...      # Returns a literal
