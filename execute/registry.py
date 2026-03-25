from typing import Any, Callable
from language import Environment
from execute import EvalResult, _ApplyFunc

_globals: dict[str, Any] = {}
_special_forms: dict[str, Callable[[list, Environment], EvalResult]] = {}

def _bind_special_form(name: str, handler: Callable[[list, Environment], EvalResult]) -> None:
    _special_forms[name] = handler

def _bind_builtin(name: str, handler: _ApplyFunc) -> None:
    _globals[name] = handler
