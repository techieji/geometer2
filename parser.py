from language import Token, TokenType, ParseTree
from typing import Iterable, Iterator

def parse(tokens: Iterable[Token]) -> ParseTree:
    token_iter = iter(tokens)

    def parse_one():
        token = next(token_iter)

        if token.kind == TokenType.CHARACTER:
            if token.value == '(':
                items = []
                while True:
                    next_token = next(token_iter, None)
                    if next_token is None:
                        raise ValueError("Unclosed parenthesis")
                    if next_token.kind == TokenType.CHARACTER and next_token.value == ')':
                        break
                    token_iter = iter([next_token] + list(token_iter))
                    item = parse_one()
                    items.append(item)
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
