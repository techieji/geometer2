from language import Token, TokenType, Environment
from execute import EvalResult

def _is_truthy(val: EvalResult) -> bool:
    if isinstance(val, Token):
        if val.kind == TokenType.BOOLEAN:
            return val.value
        if val.kind == TokenType.NUMBER:
            return val.value != 0
        if val.kind == TokenType.ATOM:
            return val.value not in ('#f', 'false', 'nil', '()')
    if isinstance(val, list):
        return len(val) > 0
    return True

def _eval_list(nodes: list, env: Environment) -> list[EvalResult]:
    from execute.eval import _eval
    return [_eval(node, env) for node in nodes]

def pprint_result(result: EvalResult) -> None:
    def fmt(x):
        if isinstance(x, Token):
            if x.kind == TokenType.NUMBER:
                return str(x.value)
            if x.kind == TokenType.STRING:
                return f'"{x.value}"'
            if x.kind == TokenType.BOOLEAN:
                return '#t' if x.value else '#f'
            if x.kind == TokenType.ATOM:
                return str(x.value)
            if x.kind == TokenType.POINT:
                return str(x.value)
            return str(x.value)
        if isinstance(x, list):
            return '(' + ' '.join(fmt(e) for e in x) + ')'
        return str(x)
    print(fmt(result))
