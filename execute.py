from typing import Callable
from language import Environment, ParseTree, Token, TokenType, EvalResult
from builtin_fns import get_builtin
from pprint import pprint_result

def execute(parse_tree: ParseTree, environment: Environment) -> EvalResult:
    from special_forms import get_special_form
    if isinstance(parse_tree.value, Token):
        return parse_tree.value.value
    
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

if __name__ == '__main__':
    from lexer import lex
    from parser import parse
    from environment import make_environment
    try:
        while True:
            pprint_result(execute(parse(lex(input('> '))), make_environment()))
    except EOFError:
        print('exiting')
