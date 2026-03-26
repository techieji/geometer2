from collections import ChainMap
from typing import Any
from language import Environment

def make_environment() -> Environment:
    return ChainMap({})

def extend_environment(env: Environment, bindings: dict[str, Any]) -> Environment:
    return ChainMap(bindings, env)
