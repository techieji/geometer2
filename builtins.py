from typing import Callable, Any
from language import Environment, Token, TokenType

type EvalResult = list[EvalResult] | int | float | bool | str | Callable[[list[EvalResult]], EvalResult]

def _is_token(val: EvalResult) -> bool:
    return isinstance(val, Token)

def _to_number(val: EvalResult) -> int | float:
    if isinstance(val, Token) and val.kind == TokenType.NUMBER:
        return val.value
    return val  # type: ignore

def _to_bool(val: EvalResult) -> bool:
    if isinstance(val, Token) and val.kind == TokenType.BOOLEAN:
        return val.value
    return bool(val)

def _add(args: list[EvalResult], env: Environment) -> EvalResult:
    if _is_token(args[0]) and args[0].kind == TokenType.POINT:  # type: ignore
        p1: tuple[float, float] = args[0].value  # type: ignore
        p2: tuple[float, float] = args[1].value  # type: ignore
        return (p1[0] + p2[0], p1[1] + p2[1])
    result: int | float = 0
    for a in args:
        if isinstance(a, (int, float)):
            result += a
    return result

def _sub(args: list[EvalResult], env: Environment) -> EvalResult:
    if _is_token(args[0]) and args[0].kind == TokenType.POINT:  # type: ignore
        p1: tuple[float, float] = args[0].value  # type: ignore
        p2: tuple[float, float] = args[1].value  # type: ignore
        return (p1[0] - p2[0], p1[1] - p2[1])
    a = _to_number(args[0])
    b = _to_number(args[1])
    return a - b  # type: ignore

def _mul(args: list[EvalResult], env: Environment) -> EvalResult:
    if len(args) > 1 and _is_token(args[1]) and args[1].kind == TokenType.POINT:  # type: ignore
        s: int | float = _to_number(args[0])
        p: tuple[float, float] = args[1].value  # type: ignore
        return (s * p[0], s * p[1])
    a = _to_number(args[0])
    b = _to_number(args[1])
    return a * b  # type: ignore

def _div(args: list[EvalResult], env: Environment) -> EvalResult:
    a = _to_number(args[0])
    b = _to_number(args[1])
    return a / b  # type: ignore

def _eq(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] == args[1]

def _lt(args: list[EvalResult], env: Environment) -> EvalResult:
    a = _to_number(args[0])
    b = _to_number(args[1])
    return a < b  # type: ignore

def _gt(args: list[EvalResult], env: Environment) -> EvalResult:
    a = _to_number(args[0])
    b = _to_number(args[1])
    return a > b  # type: ignore

def _car(args: list[EvalResult], env: Environment) -> EvalResult:
    lst = args[0]
    if isinstance(lst, list):
        return lst[0]
    return None

def _cdr(args: list[EvalResult], env: Environment) -> EvalResult:
    lst = args[0]
    if isinstance(lst, list):
        return lst[1:]
    return []

def _cons(args: list[EvalResult], env: Environment) -> EvalResult:
    return [args[0]] + args[1]  # type: ignore

def _list(args: list[EvalResult], env: Environment) -> EvalResult:
    return args

def _eqp(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] is args[1]

def _not(args: list[EvalResult], env: Environment) -> EvalResult:
    return not _to_bool(args[0])

BUILTINS: dict[str, Callable[[list[EvalResult], Environment], EvalResult]] = {
    "+": _add,
    "-": _sub,
    "*": _mul,
    "/": _div,
    "=": _eq,
    "<": _lt,
    ">": _gt,
    "car": _car,
    "cdr": _cdr,
    "cons": _cons,
    "list": _list,
    "eq?": _eqp,
    "not": _not,
}

def get_builtin(name: str) -> Callable[[list[EvalResult], Environment], EvalResult] | None:
    return BUILTINS.get(name)
