from collections import ChainMap
from language import ParseTree, Environment
from execute.eval import _eval
from execute import EvalResult, _ApplyFunc

def _make_closure(params: list[str], body: list[ParseTree], env: Environment) -> _ApplyFunc:
    def closure(args: list[EvalResult], inner_env: Environment) -> EvalResult:
        local = dict(zip(params, args))
        new_env = ChainMap(local, env)
        result = None
        for expr in body:
            result = _eval(expr, new_env)
        return result
    return closure
