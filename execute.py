from typing import Callable
from language import Environment, ParseTree, Token, TokenType
from builtins import get_builtin
from special_forms import get_special_form
from pprint import pprint_result

type EvalResult = list[EvalResult] | int | float | bool | str | Callable[[list[EvalResult]], 'EvalResult']

def execute(parse_tree: ParseTree, environment: Environment) -> EvalResult:
    if parse_tree.is_literal:
        return parse_tree.value
    
    expr: list[ParseTree] = parse_tree.value
    first = execute(expr[0], environment)
    
    if isinstance(first, Token) and first.kind == TokenType.ATOM:
        special = get_special_form(first.value)
        if special:
            return special(expr, environment)
        
        args = [execute(arg, environment) for arg in expr[1:]]
        builtin = get_builtin(first.value)
        if builtin:
            return builtin(args, environment)
    
    raise ValueError(f"Cannot evaluate {parse_tree}")
