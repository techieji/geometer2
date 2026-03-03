from __future__ import annotations
import operator
import os
from typing import List, Optional, Tuple, Any
from lark import Lark, Transformer, v_args
from geometer.core.entities import Point, Shape

# Define Symbol as a string type for convenience
Symbol = str

class Environment:
    "An environment: a dict of {'var': val} pairs, with an outer (parent) env."
    def __init__(self, parms=(), args=(), outer=None):
        self.vars = dict(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Environment where var appears."
        if var in self.vars:
            return self
        if self.outer is None:
            raise NameError(f"unbound variable: {var}")
        return self.outer.find(var)

    def __getitem__(self, key):
        return self.find(key).vars[key]

    def __setitem__(self, key, value):
        self.vars[key] = value

class Procedure:
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return evaluate(self.body, Environment(self.parms, args, self.env))

def _polymorphic_op(op_func, args):
    """Applies an operator polymorphically to numbers or Points."""
    if not args:
        raise TypeError(f"Operator '{op_func.__name__}' requires at least one argument")
    
    # Check for division of Points, which is not supported as per README
    if op_func == operator.truediv:
        if any(isinstance(arg, Point) for arg in args):
            raise TypeError(f"Division of Point objects is not supported.")

    first_arg = args[0]

    # Handle unary minus for numbers and points
    if op_func == operator.sub and len(args) == 1:
        if isinstance(first_arg, (int, float)):
            return -first_arg
        elif isinstance(first_arg, Point):
            # Create a new Point with inverted coordinates, retaining computed status and dependencies
            return Point(-first_arg.x, -first_arg.y, computed=first_arg.computed, dependencies=first_arg.dependencies)
        else:
            raise TypeError(f"Unsupported operand type for unary '{op_func.__name__}': {type(first_arg)}")

    # For binary and n-ary operations
    res = first_arg
    for arg in args[1:]:
        if isinstance(res, Point) or isinstance(arg, Point):
            # If `res` is a Point and `arg` is a Point, use Point's dunder method
            if isinstance(res, Point) and isinstance(arg, Point):
                res = op_func(res, arg)
            # If `res` is a Point and `arg` is scalar (e.g., Point * scalar, Point + scalar)
            elif isinstance(res, Point) and isinstance(arg, (int, float)):
                if op_func in (operator.add, operator.sub, operator.mul): # Supported by Point's methods
                    res = op_func(res, arg)
                else:
                    raise TypeError(f"Unsupported operand type for '{op_func.__name__}': Point and {type(arg)}")
            # If `res` is scalar and `arg` is a Point (e.g., scalar * Point, scalar + Point)
            elif isinstance(res, (int, float)) and isinstance(arg, Point):
                if op_func in (operator.add, operator.sub, operator.mul): # Supported by Point's __r*__ methods
                    res = op_func(res, arg)
                else:
                    raise TypeError(f"Unsupported operand type for '{op_func.__name__}': {type(res)} and Point")
            else:
                raise TypeError(f"Incompatible types for '{op_func.__name__}': {type(res)} and {type(arg)}")
        else: # Both are numbers (or other non-Point types)
            res = op_func(res, arg)
    return res

def _standard_env() -> Environment:
    "An environment with a built-in set of functions and operators."
    env = Environment()
    env.vars.update({
        '+': lambda *args: _polymorphic_op(operator.add, args),
        '-': lambda *args: _polymorphic_op(operator.sub, args),
        '*': lambda *args: _polymorphic_op(operator.mul, args),
        '/': lambda *args: _polymorphic_op(operator.truediv, args),
        '=': operator.eq,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        'list': lambda *args: list(args),
        'car': lambda x: x[0] if x else None,
        'cdr': lambda x: x[1:] if x else [],
        'cons': lambda x, y: [x] + (list(y) if isinstance(y, (list, tuple)) else [y]),
        'true': True,
        'false': False,
        'null?': lambda x: x == [],
        'not': operator.not_,
    })
    return env

@v_args(inline=True) # Flatten rule matches directly into the parent's children.
class LispTransformer(Transformer):
    def NUMBER(self, n):
        return float(n) if '.' in n else int(n)

    def SYMBOL(self, s):
        return Symbol(s)

    def STRING(self, s):
        return s[1:-1] # Remove quotes

    def point_literal(self, x, y):
        return Point(float(x), float(y))

    def list_expr(self, *items):
        return list(items)

    def expression(self, expr):
        return expr # Directly return the expression (atom, list_expr, or point_literal)

    def start(self, expr):
        return expr

GRAMMAR_FILE_PATH = os.path.join(os.path.dirname(__file__), "grammar.lark")

# Ensure the grammar file exists (it will be created by a previous block)
try:
    with open(GRAMMAR_FILE_PATH, 'r'):
        pass
except FileNotFoundError:
    pass # Will be handled by the user's execution order

lisp_parser = Lark.open(
    GRAMMAR_FILE_PATH,
    parser='lalr',
    start='start',
    transformer=LispTransformer()
)

GLOBAL_ENV = _standard_env()

def parse_lisp_expression(program: str):
    """Parses a Geometer Lisp program string into an AST."""
    return lisp_parser.parse(program)

def evaluate(exp, env=GLOBAL_ENV):
    "Evaluate an expression in an environment."
    if isinstance(exp, Symbol):  # variable reference
        return env[exp]
    elif not isinstance(exp, (list, tuple)):  # constant literal (number, string, Point, etc.)
        return exp
    
    # Process S-expressions (lists/tuples)
    exp_list = list(exp) # Ensure it's a mutable list for consistent unpacking
    op, *args = exp_list

    if op == 'quote':             # (quote exp)
        return args[0]
    elif op == 'if':              # (if test conseq alt)
        if len(args) != 3:
            raise TypeError("if expects 3 arguments (test conseq alt)")
        (test, conseq, alt) = args
        return evaluate(conseq, env) if evaluate(test, env) else evaluate(alt, env)
    elif op == 'define':          # (define var exp)
        if len(args) != 2:
            raise TypeError("define expects 2 arguments (var val)")
        (symbol, val_exp) = args
        if not isinstance(symbol, Symbol):
            raise TypeError(f"first argument to define must be a symbol, got {type(symbol)}")
        env[symbol] = evaluate(val_exp, env)
    elif op == 'lambda':          # (lambda (var...) body)
        if len(args) != 2:
            raise TypeError("lambda expects 2 arguments ((parm...) body)")
        (parms, body) = args
        if not all(isinstance(p, Symbol) for p in parms):
            raise TypeError("parameters to lambda must be symbols")
        return Procedure(parms, body, env)
    else:                         # (proc exp...)
        proc = evaluate(op, env)
        vals = [evaluate(arg, env) for arg in args]
        return proc(*vals)
