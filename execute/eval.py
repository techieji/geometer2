from typing import Any
from language import ParseTree, Token, Environment, TokenType
from execute.registry import _globals, _special_forms, _apply_func
from execute.utils import _is_truthy, _eval_list

def _eval(node: ParseTree, env: Environment) -> EvalResult:
    from execute import EvalResult
    if node.is_literal:
        if node.value.kind == TokenType.ATOM:
            name = node.value.value
            if name in env:
                return env[name]
            raise NameError(f"undefined: {name}")
        return node.value
    elements = node.value if isinstance(node.value, list) else [node.value]
    if not elements:
        return Token(TokenType.ATOM, '()')
    first = elements[0]
    if not first.is_literal or first.value.kind != TokenType.ATOM:
        func = _eval(first, env)
        return _apply(func, elements[1:], env)
    name = first.value.value
    if name in _special_forms:
        return _special_forms[name](elements[1:], env)
    if name in _globals:
        func = _globals[name]
        return _apply(func, elements[1:], env)
    raise ValueError(f"Unknown form: {name}")

def _apply(func: _ApplyFunc, args: list[ParseTree], env: Environment) -> EvalResult:
    from execute import EvalResult
    evaled = _eval_list(args, env)
    if callable(func):
        return func(evaled, env)
    raise TypeError(f"{func} is not callable")
