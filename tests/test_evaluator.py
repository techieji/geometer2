"""Tests for the Lisp evaluator module.

This module tests the evaluator's ability to handle:
- Atom evaluation (literals and symbol lookup)
- Special forms (quote, if, define, lambda, let, set!, begin, cond)
- Function application (built-ins and user-defined)
- Point operations
- Realistic usage scenarios
- Error handling
"""

import pytest
from geometer.lisp.lexer import Lexer
from geometer.lisp.parser import Parser
from geometer.lisp.environment import Environment, reset_global_environment
from geometer.lisp.evaluator import (
    eval_ast, eval_source, Function, BuiltinFunction, SyntaxError, TypeError
)
from geometer.types.point import DefinitePoint, Point


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def fresh_environment():
    """Reset the global environment before each test."""
    reset_global_environment()
    yield


def evaluate(source: str, env: Environment = None) -> any:
    """Helper function to parse and evaluate a source string.
    
    Args:
        source: The Lisp source code to evaluate.
        env: Optional environment to use.
        
    Returns:
        The result of evaluation.
    """
    parser = Parser(source)
    nodes = parser.parse()
    if env is not None:
        return eval_ast(nodes, env)
    return eval_source(source)


# ============================================================================
# Category 1: Atom Evaluation
# ============================================================================

class TestAtomEvaluation:
    """Test evaluation of atom nodes (literals and symbols)."""
    
    def test_integer_literal(self):
        result = evaluate("42")
        assert result == [42]
    
    def test_float_literal(self):
        result = evaluate("3.14")
        assert result == [3.14]
    
    def test_string_literal(self):
        result = evaluate('"hello"')
        assert result == ["hello"]
    
    def test_boolean_true(self):
        result = evaluate("#t")
        assert result == [True]
    
    def test_boolean_false(self):
        result = evaluate("#f")
        assert result == [False]
    
    def test_symbol_lookup(self):
        evaluate("(define x 10)")
        result = evaluate("x")
        assert result == [10]
    
    def test_undefined_symbol(self):
        with pytest.raises(NameError):
            evaluate("undefined_var")


# ============================================================================
# Category 2: Special Forms
# ============================================================================

class TestQuoteSpecialForm:
    """Test the quote special form."""
    
    def test_basic_quote(self):
        result = evaluate("(quote foo)")
        assert isinstance(result[0], type(evaluate("foo")[0].__class__))
        # The symbol should not be looked up
        assert repr(result[0]) == "foo"
    
    def test_quote_list(self):
        result = evaluate("(quote (1 2 3))")
        # Returns a ListNode
        assert len(result) == 1
    
    def test_quote_shorthand(self):
        result1 = evaluate("(quote foo)")
        result2 = evaluate("'foo")
        assert repr(result1[0]) == repr(result2[0])


class TestIfSpecialForm:
    """Test the if special form."""
    
    def test_true_branch(self):
        result = evaluate("(if #t 1 2)")
        assert result == [1]
    
    def test_false_branch(self):
        result = evaluate("(if #f 1 2)")
        assert result == [2]
    
    def test_no_alternate(self):
        result = evaluate("(if #t 1)")
        assert result == [1]
    
    def test_nil_is_falsy(self):
        result = evaluate("(if nil 1 2)")
        assert result == [2]
    
    def test_nested_condition(self):
        result = evaluate("(if (> 3 2) \"yes\" \"no\")")
        assert result == ["yes"]
    
    def test_zero_is_falsy(self):
        result = evaluate("(if 0 \"truthy\" \"falsy\")")
        # In Lisp, 0 is truthy typically, but nil is falsy
        # Our implementation treats anything not False/None as truthy
        assert result == ["truthy"]


class TestDefineSpecialForm:
    """Test the define special form."""
    
    def test_variable_define(self):
        result = evaluate("(define x 5)")
        assert result == [None]
        # Verify binding exists
        assert evaluate("x") == [5]
    
    def test_redefine_error(self):
        evaluate("(define x 1)")
        with pytest.raises(ValueError):
            evaluate("(define x 2)")
    
    def test_function_define(self):
        evaluate("(define (add a b) (+ a b))")
        result = evaluate("(add 3 4)")
        assert result == [7]
    
    def test_define_multiple_args(self):
        evaluate("(define (mul a b c) (* a b c))")
        result = evaluate("(mul 2 3 4)")
        assert result == [24]


class TestLambdaSpecialForm:
    """Test the lambda special form."""
    
    def test_lambda_creation(self):
        result = evaluate("(lambda (x y) (+ x y))")
        assert isinstance(result[0], Function)
    
    def test_lambda_application(self):
        result = evaluate("((lambda (x) (* x 2)) 5)")
        assert result == [10]
    
    def test_closure_capture(self):
        evaluate("(define f (let ((x 10)) (lambda () x)))")
        result = evaluate("(f)")
        assert result == [10]
    
    def test_lambda_with_multiple_params(self):
        result = evaluate("((lambda (a b c) (+ a b c)) 1 2 3)")
        assert result == [6]


class TestLetSpecialForm:
    """Test the let special form."""
    
    def test_simple_let(self):
        result = evaluate("(let ((x 5)) x)")
        assert result == [5]
    
    def test_multiple_bindings(self):
        result = evaluate("(let ((x 3) (y 4)) (+ x y))")
        assert result == [7]
    
    def test_let_body(self):
        result = evaluate("(let ((x 1)) (+ x 10))")
        assert result == [11]
    
    def test_let_nested(self):
        result = evaluate("(let ((x 5)) (let ((y 10)) (+ x y)))")
        assert result == [15]


class TestSetSpecialForm:
    """Test the set! special form."""
    
    def test_set_existing(self):
        evaluate("(define x 5)")
        evaluate("(set! x 10)")
        result = evaluate("x")
        assert result == [10]
    
    def test_set_undefined(self):
        with pytest.raises(NameError):
            evaluate("(set! undefined 1)")


class TestBeginSpecialForm:
    """Test the begin special form."""
    
    def test_sequential_eval(self):
        result = evaluate("(begin 1 2 3)")
        assert result == [3]
    
    def test_side_effects(self):
        result = evaluate("(begin (define x 1) (set! x 2) x)")
        assert result == [2]


class TestCondSpecialForm:
    """Test the cond special form."""
    
    def test_first_true(self):
        result = evaluate("(cond (#t 1) (#t 2))")
        assert result == [1]
    
    def test_else_clause(self):
        result = evaluate("(cond (#f 1) (else 2))")
        assert result == [2]
    
    def test_no_match(self):
        result = evaluate("(cond (#f 1))")
        assert result == [None]
    
    def test_cond_multiple_exprs(self):
        result = evaluate("(cond (#t 1 2 3))")
        assert result == [3]


# ============================================================================
# Category 3: Function Application
# ============================================================================

class TestBuiltinArithmetic:
    """Test built-in arithmetic functions."""
    
    def test_addition(self):
        result = evaluate("(+ 3 4)")
        assert result == [7]
    
    def test_subtraction(self):
        result = evaluate("(- 10 3)")
        assert result == [7]
    
    def test_multiplication(self):
        result = evaluate("(* 6 7)")
        assert result == [42]
    
    def test_division(self):
        result = evaluate("(/ 20 4)")
        assert result == [5.0]
    
    def test_chained_ops(self):
        result = evaluate("(+ (* 2 3) (/ 10 2))")
        assert result == [11.0]


class TestBuiltinComparison:
    """Test built-in comparison functions."""
    
    def test_equality(self):
        result = evaluate("(= 5 5)")
        assert result == [True]
    
    def test_less_than(self):
        result = evaluate("(< 3 5)")
        assert result == [True]
    
    def test_greater_than(self):
        result = evaluate("(> 5 3)")
        assert result == [True]
    
    def test_less_equal(self):
        result = evaluate("(<= 3 3)")
        assert result == [True]
    
    def test_greater_equal(self):
        result = evaluate("(>= 5 3)")
        assert result == [True]


class TestBuiltinListOperations:
    """Test built-in list operations."""
    
    def test_list_creation(self):
        result = evaluate("(list 1 2 3)")
        assert result == [[1, 2, 3]]
    
    def test_car(self):
        result = evaluate("(car (quote (1 2 3)))")
        assert result == [1]
    
    def test_cdr(self):
        result = evaluate("(cdr (quote (1 2 3)))")
        assert result == [[2, 3]]
    
    def test_cons(self):
        result = evaluate("(cons 0 (quote (1 2)))")
        assert result == [[0, 1, 2]]


class TestBuiltinTypePredicates:
    """Test built-in type predicate functions."""
    
    def test_number_check(self):
        result = evaluate("(number? 42)")
        assert result == [True]
    
    def test_string_check(self):
        result = evaluate("(string? \"hi\")")
        assert result == [True]
    
    def test_function_check(self):
        result = evaluate("(function? (lambda (x) x))")
        assert result == [True]
    
    def test_number_check_false(self):
        result = evaluate("(number? \"hi\")")
        assert result == [False]


# ============================================================================
# Category 4: Point Operations
# ============================================================================

class TestPointOperations:
    """Test point constructor and operations."""
    
    def test_point_constructor(self):
        result = evaluate("(point 3 4)")
        assert isinstance(result[0], DefinitePoint)
        assert result[0].x == 3
        assert result[0].y == 4
    
    def test_point_x_accessor(self):
        result = evaluate("(point-x (point 3 4))")
        assert result == [3]
    
    def test_point_y_accessor(self):
        result = evaluate("(point-y (point 3 4))")
        assert result == [4]
    
    def test_point_addition(self):
        result = evaluate("(point+ (point 1 2) (point 3 4))")
        assert isinstance(result[0], DefinitePoint)
        assert result[0].x == 4
        assert result[0].y == 6
    
    def test_point_subtraction(self):
        result = evaluate("(point- (point 5 4) (point 2 1))")
        assert isinstance(result[0], DefinitePoint)
        assert result[0].x == 3
        assert result[0].y == 3
    
    def test_scalar_multiplication(self):
        result = evaluate("(point* 2 (point 3 4))")
        assert isinstance(result[0], DefinitePoint)
        assert result[0].x == 6
        assert result[0].y == 8
    
    def test_point_predicate(self):
        result = evaluate("(point? (point 1 2))")
        assert result == [True]
    
    def test_point_predicate_false(self):
        result = evaluate("(point? 42)")
        assert result == [False]


# ============================================================================
# Category 5: Point Literal Syntax
# ============================================================================

class TestPointLiteralSyntax:
    """Test point literal syntax (x, y)."""
    
    def test_point_literal_in_list(self):
        result = evaluate("(list (quote (1, 2)))")
        # The point should be converted to DefinitePoint
        assert isinstance(result[0][0], DefinitePoint)
    
    def test_point_literal_evaluation(self):
        result = evaluate("(point-x (quote (5, 3)))")
        assert result == [5]


# ============================================================================
# Category 6: Realistic Usage (Integration)
# ============================================================================

class TestRealisticUsage:
    """Test realistic usage scenarios."""
    
    def test_define_and_use_variable(self):
        result = evaluate("(define pi 3.14) (* 2 pi)")
        assert result == [None, 6.28]
    
    def test_conditional_point_selection(self):
        result = evaluate('(if (> 5 3) (point 10 10) (point 0 0))')
        assert isinstance(result[0], DefinitePoint)
        assert result[0].x == 10
        assert result[0].y == 10
    
    def test_let_for_temp_point(self):
        result = evaluate("(let ((p (point 5 5))) (point-x p))")
        assert result == [5]
    
    def test_nested_lambda_application(self):
        result = evaluate("((lambda (f) (f 10)) (lambda (x) (* x x)))")
        assert result == [100]
    
    def test_factorial_function(self):
        evaluate("(define (fact n) (if (= n 0) 1 (* n (fact (- n 1)))))")
        result = evaluate("(fact 5)")
        assert result == [120]
    
    def test_fibonacci_function(self):
        evaluate("(define (fib n) (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))")
        result = evaluate("(fib 10)")
        assert result == [55]
    
    def test_composed_functions(self):
        evaluate("(define (square x) (* x x))")
        evaluate("(define (double x) (+ x x))")
        result = evaluate("(square (double 3))")
        assert result == [36]
    
    def test_higher_order_function(self):
        evaluate("(define (apply-twice f x) (f (f x)))")
        result = evaluate("((apply-twice (lambda (x) (+ x 1)) 0))")
        assert result == [2]


class TestDisplayBuiltin:
    """Test display and newline built-ins."""
    
    def test_display(self):
        # Should not raise, returns None
        result = evaluate("(display \"hello\")")
        assert result == [None]
    
    def test_newline(self):
        result = evaluate("(newline)")
        assert result == [None]


# ============================================================================
# Category 7: Error Handling
# ============================================================================

class TestErrorHandling:
    """Test error handling for invalid inputs."""
    
    def test_wrong_arg_count(self):
        with pytest.raises(TypeError):
            evaluate("(+ 1)")
    
    def test_not_a_function(self):
        with pytest.raises(TypeError):
            evaluate("(1 2)")
    
    def test_invalid_special_form(self):
        with pytest.raises(TypeError):
            evaluate("(unknown 1 2)")
    
    def test_invalid_if_args(self):
        with pytest.raises(SyntaxError):
            evaluate("(if)")
    
    def test_lambda_no_body(self):
        with pytest.raises(SyntaxError):
            evaluate("(lambda (x))")
    
    def test_define_no_value(self):
        with pytest.raises(SyntaxError):
            evaluate("(define x)")
    
    def test_quote_wrong_args(self):
        with pytest.raises(SyntaxError):
            evaluate("(quote 1 2)")


# ============================================================================
# Additional Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_list(self):
        result = evaluate("()")
        assert result == [[]]
    
    def test_nested_lists(self):
        result = evaluate("(quote ((1 2) (3 4)))")
        assert len(result[0].elements) == 2
    
    def test_deeply_nested_evaluation(self):
        # Test evaluation depth
        result = evaluate("((((lambda (x) x) (lambda (y) y)) 42))")
        assert result == [42]
    
    def test_let_with_no_bindings(self):
        result = evaluate("(let () 42)")
        assert result == [42]
    
    def test_begin_with_single_expr(self):
        result = evaluate("(begin 42)")
        assert result == [42]
    
    def test_cond_with_multiple_results(self):
        result = evaluate("(cond (#f 1) (#t 10 20 30))")
        assert result == [30]


# ============================================================================
# Environment Tests
# ============================================================================

class TestEnvironmentInteraction:
    """Test evaluator's interaction with environments."""
    
    def test_child_environment(self):
        env = Environment()
        env.define("x", 100)
        child = env.extend()
        child.define("y", 200)
        
        # Can access parent from child
        assert child.lookup("x") == 100
        # Can access own bindings
        assert child.lookup("y") == 200
        
        # Parent cannot access child's bindings
        with pytest.raises(NameError):
            env.lookup("y")
    
    def test_set_in_environment(self):
        env = Environment()
        env.define("x", 1)
        env.set("x", 2)
        assert env.lookup("x") == 2
    
    def test_is_defined(self):
        env = Environment()
        env.define("x", 1)
        assert env.is_defined("x")
        assert not env.is_defined("y")


# ============================================================================
# Function Object Tests
# ============================================================================

class TestFunctionObjects:
    """Test Function and BuiltinFunction classes."""
    
    def test_function_repr(self):
        result = evaluate("(lambda (x) x)")
        func = result[0]
        assert "Function" in repr(func)
    
    def test_function_with_name(self):
        evaluate("(define (my-func x) x)")
        result = evaluate("my-func")
        assert "my-func" in repr(result[0])
    
    def test_builtin_repr(self):
        result = evaluate("+")
        assert "BuiltinFunction" in repr(result[0])
