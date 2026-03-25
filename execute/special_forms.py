from collections import ChainMap
from language import ParseTree, Token, Environment, TokenType
from execute.registry import _bind_special_form, _globals
from execute.eval import _eval, _eval_list
from execute.utils import _is_truthy
from execute import EvalResult

def _install_special_forms():
    def quote_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        return args[0].value if len(args) == 1 else [a.value for a in args]
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
        params = [p.value for p in args[0].value] if args[0].is_literal and args[0].value.kind == TokenType.CHARACTER else [p.value.value for p in args[0].value]
        body = args[1:]
        from execute.closure import _make_closure
        return _make_closure(params, body, env)
    _bind_special_form('lambda', lambda_handler)

    def let_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        bindings = args[0].value if args[0].is_literal else args[0].value
        local = {}
        for b in bindings:
            var = b.value[0].value.value
            val = _eval(b.value[1], env)
            local[var] = val
        new_env = ChainMap(local, env)
        result = None
        for expr in args[1:]:
            result = _eval(expr, new_env)
        return result
    _bind_special_form('let', let_handler)

    def set_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        name = args[0].value.value
        value = _eval(args[1], env)
        for m in env.maps:
            if name in m:
                m[name] = value
                break
        return Token(TokenType.ATOM, 'ok')
    _bind_special_form('set!', set_handler)

    def begin_handler(args: list[ParseTree], env: Environment) -> EvalResult:
        result = None
        for expr in args:
            result = _eval(expr, env)
        return result
    _bind_special_form('begin', begin_handler)
