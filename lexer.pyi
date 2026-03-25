from language import ParseTree as ParseTree, Token
from typing import Iterable

def lex(program: str) -> Iterable[Token]: ...
