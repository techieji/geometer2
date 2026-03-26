from collections import ChainMap
from typing import Any, Callable, Protocol, cast
from language import ParseTree, Token, Environment, TokenType

type EvalResult = Token | Callable[list['EvalResult'], 'EvalResult'] | list['EvalResult']

class _ApplyFunc(Protocol):
    def __call__(self, args: list[EvalResult], env: Environment) -> EvalResult: ...

_globals: dict[str, Any] = {}
_special_forms: dict[str, Callable[[list[ParseTree], Environment], EvalResult]] = {}

def _eval(node: ParseTree, env: Environment) -> EvalResult:
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
    if not first.is_literal:
        func = _eval(first, env)
        return _apply(func, elements[1:], env)
    name = first.value.value
    if name in _special_forms:
        return _special_forms[name](elements[1:], env)
    if name in _globals:
        func = _globals[name]
        return _apply(func, elements[1:], env)
    if name in env:
        func = env[name]
        return _apply(func, elements[1:], env)

    raise ValueError(f"Unknown form: {name}")

def _apply(func: _ApplyFunc, args: list[ParseTree], env: Environment) -> EvalResult:
    evaled = _eval_list(args, env)
    if callable(func):
        return func(evaled, env)
    raise TypeError(f"{func} is not callable")

def _eval_list(nodes: list[ParseTree], env: Environment) -> list[EvalResult]:
    return [_eval(node, env) for node in nodes]

def _bind_special_form(name: str, handler: Callable[[list[ParseTree], Environment], EvalResult]) -> None:
    _special_forms[name] = handler

def _bind_builtin(name: str, handler: _ApplyFunc) -> None:
    _globals[name] = handler

def _make_closure(params: list[str], body: list[ParseTree], env: Environment) -> _ApplyFunc:
    def closure(args: list[EvalResult], inner_env: Environment) -> EvalResult:
        local = dict(zip(params, args))
        new_env = ChainMap(local, env)
        result = None
        for expr in body:
            result = _eval(expr, new_env)
        return result
    return closure

def _make_native_closure(params: list[str], body: list[ParseTree], env: Environment) -> _ApplyFunc:
    def native(args: list[EvalResult], inner_env: Environment) -> EvalResult:
        local = dict(zip(params, args))
        new_env = ChainMap(local, inner_env)
        result = None
        for expr in body:
            result = _eval(expr, new_env)
        return result
    return native

def _install_special_forms():
    def quote_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        return to_python(args[0]) if len(args) == 1 else [to_python(a) for a in args]
    _bind_special_form('quote', quote_handler)
    _bind_special_form("'", lambda args, env: args[0].value if args else [])

    def if_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        cond = _eval(args[0], env)
        if _is_truthy(cond):
            return _eval(args[1], env)
        return _eval(args[2], env) if len(args) > 2 else Token(TokenType.ATOM, '#f')
    _bind_special_form('if', if_handler)

    def define_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        name = args[0].value.value
        value = _eval(args[1], env)
        env.maps[0][name] = value
        return Token(TokenType.ATOM, 'ok')
    _bind_special_form('define', define_handler)

    def lambda_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        params = [cast(ParseTree, p.value).value for p in cast(list[ParseTree], args[0].value)]
        body = args[1:]
        return _make_closure(params, body, env)
    _bind_special_form('lambda', lambda_handler)

    def let_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        bindings = cast(list[ParseTree], args[0].value)
        local = {}
        for b in bindings:
            var = cast(Token, cast(list[ParseTree], b.value)[0].value).value
            val = _eval(cast(list[ParseTree], b.value)[1], env)
            local[var] = val
        new_env = ChainMap(local, env)
        result = []
        for expr in args[1:]:
            result = _eval(expr, new_env)
        return result
    _bind_special_form('let', let_handler)

    def set_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        name = cast(Token, args[0].value).value
        value = _eval(args[1], env)
        for m in env.maps:
            if name in m:
                m[name] = value
                break
        return Token(TokenType.ATOM, 'ok')
    _bind_special_form('set!', set_handler)

    def begin_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        result = []
        for expr in args:
            result = _eval(expr, env)
        return result
    _bind_special_form('begin', begin_handler)

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

def _install_builtins():
    def to_num(v):
        if isinstance(v, Token) and v.kind == TokenType.NUMBER:
            return v.value
        return v

    def add(args: list[EvalResult], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        result = sum(nums[1:], nums[0])
        return Token(TokenType.NUMBER, result)
    _bind_builtin('+', add)

    def sub(args: list[EvalResult], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        if len(nums) == 1:
            return Token(TokenType.NUMBER, -nums[0])
        result = nums[0] - sum(nums[1:])
        return Token(TokenType.NUMBER, result)
    _bind_builtin('-', sub)

    def mul(args: list[EvalResult], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        result = 1
        for n in nums:
            result *= n
        return Token(TokenType.NUMBER, result)
    _bind_builtin('*', mul)

    def div(args: list[EvalResult], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        if len(nums) == 1:
            return Token(TokenType.NUMBER, 1 / nums[0])
        result = nums[0]
        for n in nums[1:]:
            result /= n
        return Token(TokenType.NUMBER, result)
    _bind_builtin('/', div)

    def eq(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('=', eq)

    def lt(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) < to_num(args[1]))
    _bind_builtin('<', lt)

    def gt(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) > to_num(args[1]))
    _bind_builtin('>', gt)

    def lte(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) <= to_num(args[1]))
    _bind_builtin('<=', lte)

    def gte(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) >= to_num(args[1]))
    _bind_builtin('>=', gte)

    def and_op(args: list[EvalResult], env: Environment) -> EvalResult:
        for a in args:
            if not _is_truthy(a):
                return Token(TokenType.BOOLEAN, False)
        return args[-1] if args else Token(TokenType.BOOLEAN, True)
    _bind_builtin('and', and_op)

    def or_op(args: list[EvalResult], env: Environment) -> EvalResult:
        for a in args:
            if _is_truthy(a):
                return a
        return Token(TokenType.BOOLEAN, False)
    _bind_builtin('or', or_op)

    def not_op(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, not _is_truthy(args[0]))
    _bind_builtin('not', not_op)

    def cons(args: list[EvalResult], env: Environment) -> EvalResult:
        return [to_python(args[0])] + cast(list[EvalResult], args[1])
    _bind_builtin('cons', cons)

    def car(args: list[EvalResult], env: Environment) -> EvalResult:
        return cast(list[EvalResult], args[0])[0]
    _bind_builtin('car', car)

    def cdr(args: list[EvalResult], env: Environment) -> EvalResult:
        return cast(list[EvalResult], args[0])[1:]
    _bind_builtin('cdr', cdr)

    def list_fn(args: list[EvalResult], env: Environment) -> EvalResult:
        return args
    _bind_builtin('list', list_fn)

    def eqv(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('eqv?', eqv)

    def equal(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('equal?', equal)

    def nullp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, len(args[0]) == 0 if isinstance(args[0], list) else args[0] == [])
    _bind_builtin('null?', nullp)

    def pairp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], list) and len(args[0]) > 0)
    _bind_builtin('pair?', pairp)

    def listp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], list))
    _bind_builtin('list?', listp)

    def numberp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.NUMBER)
    _bind_builtin('number?', numberp)

    def symbolp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.ATOM)
    _bind_builtin('symbol?', symbolp)

    def booleanp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.BOOLEAN)
    _bind_builtin('boolean?', booleanp)

    def stringp(args: list[EvalResult], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.STRING)
    _bind_builtin('string?', stringp)

    def display(args: list[EvalResult], env: Environment) -> EvalResult:
        print(args[0])
        return Token(TokenType.ATOM, 'ok')
    _bind_builtin('display', display)

    def newline(args: list[EvalResult], env: Environment) -> EvalResult:
        print()
        return Token(TokenType.ATOM, 'ok')
    _bind_builtin('newline', newline)

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

def to_python(result: Any) -> list | int | float | str | bool | tuple:
    if isinstance(result, Token):
        return result.value
    elif isinstance(result, ParseTree):
        return to_python(result.value)
    elif isinstance(result, list):
        return [to_python(item) for item in result]
    else:
        return result

_install_special_forms()
_install_builtins()

def execute(parse_tree: ParseTree, environment: Environment) -> EvalResult:
    return _eval(parse_tree, environment)

if __name__ == '__main__':
    from lexer import lex
    from parser import parse
    env = ChainMap({})
    try:
        while True:
            pprint_result(execute(parse(lex(input())), env))
    except EOFError:
        print('Exiting')
