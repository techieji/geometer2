from typing import Callable
from language import Environment, ParseTree, Token
from execute import execute

type EvalResult = list[EvalResult] | int | float | bool | str | Callable[[list[EvalResult]], EvalResult]

def _quote(expr: list[ParseTree], env: Environment) -> EvalResult:
    if len(expr) < 2:
        return []
    val = expr[1].value
    if isinstance(val, Token):
        return val
    return val

def _if(expr: list[ParseTree], env: Environment) -> EvalResult:
    cond = execute(expr[1], env)
    if cond:
        return execute(expr[2], env)
    if len(expr) > 3:
        return execute(expr[3], env)
    return None

def _define(expr: list[ParseTree], env: Environment) -> EvalResult:
    name = expr[1].value
    if isinstance(name, Token):
        name = name.value
    value = execute(expr[2], env)
    env[name] = value
    return None

def _set(expr: list[ParseTree], env: Environment) -> EvalResult:
    name = expr[1].value
    if isinstance(name, Token):
        name = name.value
    value = execute(expr[2], env)
    env[name] = value
    return None

def _lambda(expr: list[ParseTree], env: Environment) -> EvalResult:
    params = [p.value for p in expr[1].value] if isinstance(expr[1].value, list) else []
    body = expr[2]
    return (params, body, env)

def _begin(expr: list[ParseTree], env: Environment) -> EvalResult:
    result: EvalResult = None
    for e in expr[1:]:
        result = execute(e, env)
    return result

SPECIAL_FORMS: dict[str, Callable[[list[ParseTree], Environment], EvalResult]] = {
    "quote": _quote,
    "if": _if,
    "define": _define,
    "set!": _set,
    "lambda": _lambda,
    "begin": _begin,
}

def get_special_form(name: str) -> Callable[[list[ParseTree], Environment], EvalResult] | None:
    return SPECIAL_FORMS.get(name)
