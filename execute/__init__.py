from collections import ChainMap
from typing import Any, Callable, Protocol
from language import ParseTree, Token, Environment, TokenType, make_global_environment

type EvalResult = Token | list['EvalResult']

class _ApplyFunc(Protocol):
    def __call__(self, args: list[EvalResult], env: Environment) -> EvalResult: ...

from execute.eval import _eval, _apply, _eval_list
from execute.special_forms import _install_special_forms
from execute.builtins import _install_builtins
from execute.utils import _is_truthy, pprint_result
from execute.closure import _make_closure

def _install() -> None:
    _install_special_forms()
    _install_builtins()

_install()

def execute(parse_tree: ParseTree, environment: Environment) -> EvalResult:
    return _eval(parse_tree, environment)
