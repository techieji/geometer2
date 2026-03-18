"""Evaluator module for Geometer Lisp interpreter.

This module provides evaluation of AST nodes, including special forms
and function application.
"""

from typing import Any, Callable, Dict, List, Optional, Union
from geometer.lisp.parser import ASTNode, AtomNode, ListNode, PointNode
from geometer.lisp.environment import Environment, get_global_environment
from geometer.types.point import DefinitePoint, Point


# Type alias for callable objects (built-in functions)
CallableType = Callable[..., Any]


class Function:
    """Represents a user-defined Lisp function (lambda)."""
    
    def __init__(
        self,
        params: List[str],
        body: ASTNode,
        env: Environment,
        name: Optional[str] = None
    ):
        """Initialize a function.
        
        Args:
            params: List of parameter names.
            body: The function body (AST node).
            env: The closure environment (captured at definition time).
            name: Optional function name (for debugging).
        """
        self.params = params
        self.body = body
        self.env = env
        self.name = name
    
    def __repr__(self) -> str:
        if self.name:
            return f"<Function {self.name}>"
        return f"<Function lambda ({' '.join(self.params)}) ...>"


class BuiltinFunction:
    """Represents a built-in function implemented in Python."""
    
    def __init__(self, func: CallableType, name: Optional[str] = None):
        """Initialize a built-in function.
        
        Args:
            func: The Python function to call.
            name: Optional name (for debugging).
        """
        self.func = func
        self.name = name or getattr(func, '__name__', '<builtin>')
    
    def __repr__(self) -> str:
        return f"<BuiltinFunction {self.name}>"
    
    def __call__(self, *args: Any) -> Any:
        return self.func(*args)


class EvaluatorError(Exception):
    """Base exception for evaluator errors."""
    pass


class SyntaxError(EvaluatorError):
    """Raised for malformed special forms."""
    pass


class TypeError(EvaluatorError):
    """Raised for type errors during evaluation."""
    pass


# Built-in functions registry
_builtins: Dict[str, Any] = {}


def add_builtin(name: str, func: CallableType) -> None:
    """Add a built-in function to the global environment.
    
    Args:
        name: Name of the built-in function in Lisp.
        func: Python function to call.
    """
    _builtins[name] = BuiltinFunction(func, name)


def get_builtins() -> Dict[str, Any]:
    """Get a copy of the built-in functions dictionary."""
    return _builtins.copy()


def _init_builtins() -> None:
    """Initialize built-in functions."""
    # Arithmetic
    add_builtin('+', lambda a, b: a + b)
    add_builtin('-', lambda a, b: a - b)
    add_builtin('*', lambda a, b: a * b)
    add_builtin('/', lambda a, b: a / b)
    
    # Comparison
    add_builtin('=', lambda a, b: a == b)
    add_builtin('<', lambda a, b: a < b)
    add_builtin('>', lambda a, b: a > b)
    add_builtin('<=', lambda a, b: a <= b)
    add_builtin('>=', lambda a, b: a >= b)
    
    # List operations
    add_builtin('list', lambda *args: list(args))
    add_builtin('car', lambda lst: lst[0] if lst else None)
    add_builtin('cdr', lambda lst: lst[1:] if lst else [])
    add_builtin('cons', lambda item, lst: [item] + lst)
    
    # Type predicates
    add_builtin('number?', lambda x: isinstance(x, (int, float)))
    add_builtin('string?', lambda x: isinstance(x, str))
    add_builtin('boolean?', lambda x: isinstance(x, bool))
    add_builtin('list?', lambda x: isinstance(x, list))
    add_builtin('point?', lambda x: isinstance(x, Point))
    add_builtin('function?', lambda x: isinstance(x, (Function, BuiltinFunction)))
    
    # Equality
    add_builtin('eq?', lambda a, b: a is b)
    add_builtin('equal?', lambda a, b: a == b)
    
    # Display
    add_builtin('display', lambda x: print(x) or None)
    add_builtin('newline', lambda: print())
    
    # Point constructors
    add_builtin('point', lambda x, y: DefinitePoint(x, y))
    
    # Point operations
    add_builtin('point-x', lambda p: p.x)
    add_builtin('point-y', lambda p: p.y)
    add_builtin('point+', lambda p1, p2: DefinitePoint(p1.x + p2.x, p1.y + p2.y))
    add_builtin('point-', lambda p1, p2: DefinitePoint(p1.x - p2.x, p1.y - p2.y))
    add_builtin('point*', lambda s, p: DefinitePoint(s * p.x, s * p.y))


def _convert_point_node(node: PointNode) -> DefinitePoint:
    """Convert a PointNode to a DefinitePoint.
    
    Args:
        node: The PointNode to convert.
        
    Returns:
        A DefinitePoint with the same coordinates.
    """
    return DefinitePoint(node.x, node.y)


def _eval_atom(node: AtomNode, env: Environment) -> Any:
    """Evaluate an atom node.
    
    Args:
        node: The AtomNode to evaluate.
        env: The current environment.
        
    Returns:
        The value of the atom (number, string, boolean) or looked-up symbol.
    """
    value = node.value
    
    # Symbols need to be looked up in the environment
    if isinstance(value, str):
        return env.lookup(value)
    
    # Numbers, strings, booleans return themselves
    return value


def _eval_list(node: ListNode, env: Environment) -> Any:
    """Evaluate a list node (function call or special form).
    
    Args:
        node: The ListNode to evaluate.
        env: The current environment.
        
    Returns:
        The result of evaluation.
        
    Raises:
        SyntaxError: For malformed expressions.
        TypeError: For invalid function calls.
    """
    if not node.elements:
        return []
    
    # Get the operator (first element)
    operator = _eval(node.elements[0], env)
    
    # Evaluate the rest as arguments
    args = node.elements[1:]
    
    # Check for special forms
    if isinstance(operator, AtomNode) and isinstance(operator.value, str):
        return _eval_special_form(operator.value, args, env)
    
    # Function application
    return _apply(operator, args, env)


def _eval_special_form(name: str, args: List[ASTNode], env: Environment) -> Any:
    """Evaluate a special form.
    
    Args:
        name: The special form name.
        args: The arguments to the special form.
        env: The current environment.
        
    Returns:
        The result of the special form.
        
    Raises:
        SyntaxError: For malformed special forms.
    """
    if name == 'quote':
        # (quote <expr>) - return expr unevaluated
        if len(args) != 1:
            raise SyntaxError("quote requires exactly one argument")
        return args[0]
    
    elif name == 'if':
        # (if <test> <consequent> <alternate>)
        if len(args) < 2 or len(args) > 3:
            raise SyntaxError("if requires 2 or 3 arguments")
        
        test_result = _eval(args[0], env)
        
        # False or nil is falsy, everything else is truthy
        if test_result:
            return _eval(args[1], env)
        elif len(args) == 3:
            return _eval(args[2], env)
        return None
    
    elif name == 'define':
        # (define <symbol> <value>) or (define (<name> <params>...) <body>...)
        if len(args) < 2:
            raise SyntaxError("define requires at least 2 arguments")
        
        if isinstance(args[0], AtomNode) and isinstance(args[0].value, str):
            # Simple variable definition: (define x 10)
            symbol = args[0].value
            value = _eval(args[1], env)
            env.define(symbol, value)
            return None
        
        elif isinstance(args[0], ListNode):
            # Function definition: (define (foo x y) body...)
            func_name_node = args[0].elements[0]
            if not isinstance(func_name_node, AtomNode):
                raise SyntaxError("function name must be a symbol")
            
            func_name = func_name_node.value
            params = []
            for p in args[0].elements[1:]:
                if not isinstance(p, AtomNode):
                    raise SyntaxError("parameter must be a symbol")
                params.append(p.value)
            
            # Function body
            if len(args) == 1:
                raise SyntaxError("function definition requires a body")
            
            # Create a list node for the body if there are multiple expressions
            if len(args) == 2:
                body = args[1]
            else:
                body = ListNode(args[1:])
            
            # Create the function object
            func = Function(params, body, env, name=func_name)
            env.define(func_name, func)
            return None
        
        else:
            raise SyntaxError("define: first argument must be a symbol or list")
    
    elif name == 'lambda':
        # (lambda (<params>...) <body>...)
        if len(args) < 2:
            raise SyntaxError("lambda requires at least 2 arguments")
        
        params_node = args[0]
        if not isinstance(params_node, ListNode):
            raise SyntaxError("lambda parameters must be a list")
        
        params = []
        for p in params_node.elements:
            if not isinstance(p, AtomNode):
                raise SyntaxError("parameter must be a symbol")
            params.append(p.value)
        
        # Function body
        if len(args) == 2:
            body = args[1]
        else:
            body = ListNode(args[1:])
        
        return Function(params, body, env)
    
    elif name == 'let':
        # (let ((<sym> <val>)...) <body>...)
        if len(args) < 2:
            raise SyntaxError("let requires at least 2 arguments")
        
        bindings_node = args[0]
        if not isinstance(bindings_node, ListNode):
            raise SyntaxError("let bindings must be a list")
        
        # Create a new environment for the let bindings
        let_env = env.extend()
        
        # Process bindings
        for binding in bindings_node.elements:
            if not isinstance(binding, ListNode) or len(binding.elements) != 2:
                raise SyntaxError("let binding must be a list of two elements")
            
            sym_node = binding.elements[0]
            if not isinstance(sym_node, AtomNode):
                raise SyntaxError("let binding variable must be a symbol")
            
            symbol = sym_node.value
            value = _eval(binding.elements[1], env)
            let_env.define(symbol, value)
        
        # Evaluate body in the new environment
        if len(args) == 2:
            return _eval(args[1], let_env)
        else:
            # Multiple expressions - evaluate each and return last
            result = None
            for expr in args[1:]:
                result = _eval(expr, let_env)
            return result
    
    elif name == 'set!':
        # (set! <symbol> <value>) - set existing variable
        if len(args) != 2:
            raise SyntaxError("set! requires exactly 2 arguments")
        
        if not isinstance(args[0], AtomNode):
            raise SyntaxError("set! variable must be a symbol")
        
        symbol = args[0].value
        value = _eval(args[1], env)
        
        if not env.set(symbol, value):
            raise NameError(f"cannot set undefined variable: {symbol}")
        return None
    
    elif name == 'begin':
        # (begin <expr>...) - evaluate expressions in sequence
        result = None
        for expr in args:
            result = _eval(expr, env)
        return result
    
    elif name == 'cond':
        # (cond (<test> <expr>...)... )
        for clause in args:
            if not isinstance(clause, ListNode):
                raise SyntaxError("cond clause must be a list")
            
            if len(clause.elements) == 0:
                raise SyntaxError("cond clause cannot be empty")
            
            test = clause.elements[0]
            
            # Check for 'else' clause
            if isinstance(test, AtomNode) and test.value == 'else':
                # Evaluate remaining expressions in the clause
                result = None
                for expr in clause.elements[1:]:
                    result = _eval(expr, env)
                return result
            
            # Evaluate test
            test_result = _eval(test, env)
            if test_result:
                # Evaluate remaining expressions in the clause
                result = None
                for expr in clause.elements[1:]:
                    result = _eval(expr, env)
                return result
        
        return None
    
    else:
        # Not a special form - treat as function call
        raise TypeError(f"unknown special form: {name}")


def _apply(operator: Any, args: List[ASTNode], env: Environment) -> Any:
    """Apply a function to arguments.
    
    Args:
        operator: The function to apply (Function or BuiltinFunction).
        args: The arguments to evaluate and pass to the function.
        env: The current environment.
        
    Returns:
        The result of function application.
        
    Raises:
        TypeError: If the operator is not callable.
    """
    # Evaluate arguments
    evaluated_args = [_eval(arg, env) for arg in args]
    
    if isinstance(operator, Function):
        # Create new environment with bindings
        func_env = operator.env.extend()
        
        # Bind parameters to arguments
        if len(operator.params) != len(evaluated_args):
            raise TypeError(
                f"function expected {len(operator.params)} arguments, "
                f"got {len(evaluated_args)}"
            )
        
        for param, arg in zip(operator.params, evaluated_args):
            func_env.define(param, arg)
        
        # Evaluate function body in the new environment
        return _eval(operator.body, func_env)
    
    elif isinstance(operator, BuiltinFunction):
        # Call the built-in function
        return operator(*evaluated_args)
    
    else:
        raise TypeError(f"cannot apply: {operator} is not a function")


def _eval(node: ASTNode, env: Environment) -> Any:
    """Evaluate an AST node.
    
    Args:
        node: The AST node to evaluate.
        env: The current environment.
        
    Returns:
        The result of evaluation.
    """
    if isinstance(node, AtomNode):
        return _eval_atom(node, env)
    
    elif isinstance(node, ListNode):
        return _eval_list(node, env)
    
    elif isinstance(node, PointNode):
        return _convert_point_node(node)
    
    else:
        raise TypeError(f"cannot evaluate: {node}")


def eval_ast(nodes: List[ASTNode], env: Optional[Environment] = None) -> List[Any]:
    """Evaluate a list of AST nodes.
    
    Args:
        nodes: List of AST nodes to evaluate.
        env: Optional environment (uses global if not provided).
        
    Returns:
        List of evaluation results.
    """
    if env is None:
        env = get_global_environment()
    
    results = []
    for node in nodes:
        result = _eval(node, env)
        results.append(result)
    
    return results


def eval_source(source: str, env: Optional[Environment] = None) -> List[Any]:
    """Parse and evaluate a source string.
    
    This is a convenience function that combines parsing and evaluation.
    
    Args:
        source: The Lisp source code to evaluate.
        env: Optional environment (uses global if not provided).
        
    Returns:
        List of evaluation results.
    """
    from geometer.lisp.parser import Parser
    
    parser = Parser(source)
    nodes = parser.parse()
    return eval_ast(nodes, env)


# Initialize built-ins when module is loaded
_init_builtins()
