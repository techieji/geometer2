from language import Environment as Environment, ParseTree
from typing import Callable

type EvalResult = list['EvalResult'] | int | float | bool | str | Callable[list['EvalResult'], 'EvalResult']

def pprint_result(result: EvalResult) -> None: ...
def execute(parse_tree: ParseTree, environment: Environment) -> EvalResult: ...
