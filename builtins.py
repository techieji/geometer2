from typing import Callable
from language import Environment, Token, TokenType

type EvalResult = list[EvalResult] | int | float | bool | str | Callable[[list[EvalResult]], EvalResult]

def _to_token(val: EvalResult) -> Token:
    if isinstance(val, (int, float)):
        return Token(TokenType.NUMBER, val)
    if isinstance(val, bool):
        return Token(TokenType.BOOLEAN, val)
    if isinstance(val, str):
        return Token(TokenType.STRING, val)
    if isinstance(val, list):
        return Token(TokenType.NUMBER, val)
    return Token(TokenType.ATOM, val)

def _add(args: list[EvalResult], env: Environment) -> EvalResult:
    if isinstance(args[0], Token) and args[0].kind == TokenType.POINT:
        p1, p2 = args[0].value, args[1].value
        return (p1[0] + p2[0], p1[1] + p2[1])
    result = sum(a for a in args if isinstance(a, (int, float)))
    return result

def _sub(args: list[EvalResult], env: Environment) -> EvalResult:
    if isinstance(args[0], Token) and args[0].kind == TokenType.POINT:
        p1, p2 = args[0].value, args[1].value
        return (p1[0] - p2[0], p1[1] - p2[1])
    return args[0] - args[1]

def _mul(args: list[EvalResult], env: Environment) -> EvalResult:
    if isinstance(args[1], Token) and args[1].kind == TokenType.POINT:
        s, p = args[0], args[1].value
        return (s * p[0], s * p[1])
    return args[0] * args[1]

def _div(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] / args[1]

def _eq(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] == args[1]

def _lt(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] < args[1]

def _gt(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] > args[1]

def _car(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0][0]

def _cdr(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0][1:]

def _cons(args: list[EvalResult], env: Environment) -> EvalResult:
    return [args[0]] + args[1]

def _list(args: list[EvalResult], env: Environment) -> EvalResult:
    return args

def _eqp(args: list[EvalResult], env: Environment) -> EvalResult:
    return args[0] is args[1]

def _not(args: list[EvalResult], env: Environment) -> EvalResult:
    return not args[0]

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
