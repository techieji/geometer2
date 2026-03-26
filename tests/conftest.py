import pytest
from lexer import lex
from parser import parse
from execute import execute
from collections import ChainMap


@pytest.fixture
def empty_env():
    return ChainMap({})


def run(source: str, env=None):
    """Helper to run a source string through lexer, parser, and executor."""
    if env is None:
        env = ChainMap({})
    tokens = list(lex(source))
    tree = parse(tokens)
    return execute(tree, env)
