from language import Token, TokenType, ParseTree
from typing import Iterable, List

def parse(tokens: Iterable[Token]) -> ParseTree:
    token_list = list(tokens)
    pos = 0
    n = len(token_list)

    def parse_one() -> ParseTree:
        nonlocal pos
        if pos >= n:
            raise ValueError("Unexpected end of input")

        token = token_list[pos]
        pos += 1

        if token.kind == TokenType.CHARACTER:
            if token.value == '(':
                items = []
                while pos < n:
                    next_token = token_list[pos]
                    if next_token.kind == TokenType.CHARACTER and next_token.value == ')':
                        pos += 1
                        break
                    items.append(parse_one())
                else:
                    raise ValueError("Unclosed parenthesis")
                return ParseTree(is_literal=False, value=items)
            elif token.value == "'":
                quoted = parse_one()
                return ParseTree(
                    is_literal=False,
                    value=[
                        ParseTree(is_literal=True, value=Token(TokenType.ATOM, "quote")),
                        quoted
                    ]
                )
            elif token.value == "`":
                quasiquoted = parse_one()
                return ParseTree(
                    is_literal=False,
                    value=[
                        ParseTree(is_literal=True, value=Token(TokenType.ATOM, "quasiquote")),
                        quasiquoted
                    ]
                )
            elif token.value == ",":
                unquoted = parse_one()
                return ParseTree(
                    is_literal=False,
                    value=[
                        ParseTree(is_literal=True, value=Token(TokenType.ATOM, "unquote")),
                        unquoted
                    ]
                )

        return ParseTree(is_literal=True, value=token)

    try:
        return parse_one()
    except StopIteration:
        return ParseTree(is_literal=False, value=[])
