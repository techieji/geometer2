from collections import ChainMap
from typing import Any
from language import ParseTree, Token, Environment, TokenType
from execute.registry import _bind_builtin
from execute.utils import _is_truthy
from execute import EvalResult, _ApplyFunc

def _install_builtins() -> None:
    def to_num(v: EvalResult) -> Any:
        if isinstance(v, Token) and v.kind == TokenType.NUMBER:
            return v.value
        return v

    def add(args: list[ParseTree], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        result = sum(nums[1:], nums[0])
        return Token(TokenType.NUMBER, result)
    _bind_builtin('+', add)

    def sub(args: list[ParseTree], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        if len(nums) == 1:
            return Token(TokenType.NUMBER, -nums[0])
        result = nums[0] - sum(nums[1:])
        return Token(TokenType.NUMBER, result)
    _bind_builtin('-', sub)

    def mul(args: list[ParseTree], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        result = 1
        for n in nums:
            result *= n
        return Token(TokenType.NUMBER, result)
    _bind_builtin('*', mul)

    def div(args: list[ParseTree], env: Environment) -> EvalResult:
        nums = [to_num(a) for a in args]
        if len(nums) == 1:
            return Token(TokenType.NUMBER, 1 / nums[0])
        result = nums[0]
        for n in nums[1:]:
            result /= n
        return Token(TokenType.NUMBER, result)
    _bind_builtin('/', div)

    def eq(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('=', eq)

    def lt(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) < to_num(args[1]))
    _bind_builtin('<', lt)

    def gt(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) > to_num(args[1]))
    _bind_builtin('>', gt)

    def lte(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) <= to_num(args[1]))
    _bind_builtin('<=', lte)

    def gte(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, to_num(args[0]) >= to_num(args[1]))
    _bind_builtin('>=', gte)

    def and_op(args: list[ParseTree], env: Environment) -> EvalResult:
        for a in args:
            if not _is_truthy(a):
                return Token(TokenType.BOOLEAN, False)
        return args[-1] if args else Token(TokenType.BOOLEAN, True)
    _bind_builtin('and', and_op)

    def or_op(args: list[ParseTree], env: Environment) -> EvalResult:
        for a in args:
            if _is_truthy(a):
                return a
        return Token(TokenType.BOOLEAN, False)
    _bind_builtin('or', or_op)

    def not_op(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, not _is_truthy(args[0]))
    _bind_builtin('not', not_op)

    def cons(args: list[ParseTree], env: Environment) -> EvalResult:
        return [args[0]] + args[1]
    _bind_builtin('cons', cons)

    def car(args: list[ParseTree], env: Environment) -> EvalResult:
        return args[0][0]
    _bind_builtin('car', car)

    def cdr(args: list[ParseTree], env: Environment) -> EvalResult:
        return args[0][1:]
    _bind_builtin('cdr', cdr)

    def list_fn(args: list[ParseTree], env: Environment) -> EvalResult:
        return args
    _bind_builtin('list', list_fn)

    def eqv(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('eqv?', eqv)

    def equal(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, args[0] == args[1])
    _bind_builtin('equal?', equal)

    def nullp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, len(args[0]) == 0 if isinstance(args[0], list) else args[0] == [])
    _bind_builtin('null?', nullp)

    def pairp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], list) and len(args[0]) > 0)
    _bind_builtin('pair?', pairp)

    def listp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], list))
    _bind_builtin('list?', listp)

    def numberp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.NUMBER)
    _bind_builtin('number?', numberp)

    def symbolp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.ATOM)
    _bind_builtin('symbol?', symbolp)

    def booleanp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.BOOLEAN)
    _bind_builtin('boolean?', booleanp)

    def stringp(args: list[ParseTree], env: Environment) -> EvalResult:
        return Token(TokenType.BOOLEAN, isinstance(args[0], Token) and args[0].kind == TokenType.STRING)
    _bind_builtin('string?', stringp)

    def display(args: list[ParseTree], env: Environment) -> EvalResult:
        print(args[0])
        return Token(TokenType.ATOM, 'ok')
    _bind_builtin('display', display)

    def newline(args: list[ParseTree], env: Environment) -> EvalResult:
        print()
        return Token(TokenType.ATOM, 'ok')
    _bind_builtin('newline', newline)
