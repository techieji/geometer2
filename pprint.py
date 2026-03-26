from typing import Callable
from language import Token, TokenType

type EvalResult = list[EvalResult] | int | float | bool | str | Callable[[list[EvalResult]], EvalResult]

def pprint_result(result: EvalResult) -> None:
    if isinstance(result, list):
        parts = []
        for item in result:
            if isinstance(item, Token):
                parts.append(_token_str(item))
            else:
                parts.append(str(item))
        print("(" + " ".join(parts) + ")")
    elif isinstance(result, Token):
        print(_token_str(result))
    elif isinstance(result, bool):
        print("#t" if result else "#f")
    else:
        print(result)

def _token_str(t: Token) -> str:
    if t.kind == TokenType.NUMBER:
        return str(t.value)
    if t.kind == TokenType.STRING:
        return f'"{t.value}"'
    if t.kind == TokenType.BOOLEAN:
        return "#t" if t.value else "#f"
    if t.kind == TokenType.POINT:
        x, y = t.value
        return f"'({x},{y})"
    return str(t.value)
