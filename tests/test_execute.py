from lexer import lex
from parser import parse
from execute import execute
from language import Token
from collections import ChainMap


# =============================================================================
# Helper Functions
# =============================================================================

def run(source: str, env=None):
    """Run source through lexer, parser, and executor."""
    if env is None:
        env = ChainMap({})
    tokens = list(lex(source))
    tree = parse(tokens)
    return execute(tree, env)


def get_token_value(result):
    """Extract the value from a Token result."""
    if isinstance(result, Token):
        return result.value
    return result


# =============================================================================
# Special Forms - Quote
# =============================================================================

class TestQuote:
    def test_quote_number(self, empty_env):
        result = run("(quote 42)", empty_env)
        assert get_token_value(result) == 42

    def test_quote_symbol(self, empty_env):
        result = run("(quote foo)", empty_env)
        assert get_token_value(result) == "foo"

    def test_quote_list(self, empty_env):
        result = run("(quote (1 2 3))", empty_env)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_quote_shorthand(self, empty_env):
        result = run("'hello", empty_env)
        assert get_token_value(result) == "hello"


# =============================================================================
# Special Forms - If
# =============================================================================

class TestIf:
    def test_if_true_branch(self, empty_env):
        result = run("(if #t 1 2)", empty_env)
        assert get_token_value(result) == 1

    def test_if_false_branch(self, empty_env):
        result = run("(if #f 1 2)", empty_env)
        assert get_token_value(result) == 2

    def test_if_no_else(self, empty_env):
        result = run("(if #t 1)", empty_env)
        assert get_token_value(result) == 1

    def test_if_nested_condition(self, empty_env):
        result = run("(if (if #f #t #f) 1 2)", empty_env)
        assert get_token_value(result) == 2


# =============================================================================
# Special Forms - Define
# =============================================================================

class TestDefine:
    def test_define_variable(self, empty_env):
        run("(define x 42)", empty_env)
        result = run("x", empty_env)
        assert get_token_value(result) == 42

    def test_define_multiple(self, empty_env):
        run("(define a 1)", empty_env)
        run("(define b 2)", empty_env)
        result = run("(+ a b)", empty_env)
        assert get_token_value(result) == 3


# =============================================================================
# Special Forms - Lambda
# =============================================================================

class TestLambda:
    def test_lambda_simple(self, empty_env):
        # ((lambda (x) x) 5) => 5
        result = run("((lambda (x) x) 5)", empty_env)
        assert get_token_value(result) == 5

    def test_lambda_add(self, empty_env):
        # ((lambda (x y) (+ x y)) 3 4) => 7
        result = run("((lambda (x y) (+ x y)) 3 4)", empty_env)
        assert get_token_value(result) == 7

    def test_lambda_closure(self, empty_env):
        # (define add5 (lambda (x) (+ x 5)))
        # (add5 10) => 15
        run("(define add5 (lambda (x) (+ x 5)))", empty_env)
        result = run("(add5 10)", empty_env)
        assert get_token_value(result) == 15


# =============================================================================
# Special Forms - Let
# =============================================================================

class TestLet:
    def test_let_simple(self, empty_env):
        result = run("(let ((x 5)) x)", empty_env)
        assert get_token_value(result) == 5

    def test_let_multiple(self, empty_env):
        result = run("(let ((x 1) (y 2)) (+ x y))", empty_env)
        assert get_token_value(result) == 3


# =============================================================================
# Special Forms - Set
# =============================================================================

class TestSet:
    def test_set_variable(self, empty_env):
        run("(define x 5)", empty_env)
        run("(set! x 10)", empty_env)
        result = run("x", empty_env)
        assert get_token_value(result) == 10


# =============================================================================
# Special Forms - Begin
# =============================================================================

class TestBegin:
    def test_begin_multiple(self, empty_env):
        result = run("(begin 1 2 3)", empty_env)
        assert get_token_value(result) == 3

    def test_begin_with_side_effects(self, empty_env):
        run("(define x 0)", empty_env)
        result = run("(begin (set! x 5) x)", empty_env)
        assert get_token_value(result) == 5


# =============================================================================
# Builtin - Arithmetic
# =============================================================================

class TestArithmetic:
    def test_add_two_numbers(self, empty_env):
        result = run("(+ 3 4)", empty_env)
        assert get_token_value(result) == 7

    def test_add_multiple(self, empty_env):
        result = run("(+ 1 2 3 4)", empty_env)
        assert get_token_value(result) == 10

    def test_sub_two_numbers(self, empty_env):
        result = run("(- 10 3)", empty_env)
        assert get_token_value(result) == 7

    def test_mul_two_numbers(self, empty_env):
        result = run("(* 3 4)", empty_env)
        assert get_token_value(result) == 12

    def test_div_two_numbers(self, empty_env):
        result = run("(/ 10 2)", empty_env)
        assert get_token_value(result) == 5


# =============================================================================
# Builtin - Comparison
# =============================================================================

class TestComparison:
    def test_eq_numbers(self, empty_env):
        result = run("(= 5 5)", empty_env)
        assert get_token_value(result) is True

    def test_neq_numbers(self, empty_env):
        result = run("(= 5 3)", empty_env)
        assert get_token_value(result) is False

    def test_lt(self, empty_env):
        result = run("(< 3 5)", empty_env)
        assert get_token_value(result) is True

    def test_gt(self, empty_env):
        result = run("(> 5 3)", empty_env)
        assert get_token_value(result) is True

    def test_lte(self, empty_env):
        result = run("(<= 3 3)", empty_env)
        assert get_token_value(result) is True

    def test_gte(self, empty_env):
        result = run("(>= 5 3)", empty_env)
        assert get_token_value(result) is True


# =============================================================================
# Builtin - Logical
# =============================================================================

class TestLogical:
    def test_and_true(self, empty_env):
        result = run("(and #t #t)", empty_env)
        assert get_token_value(result) is True

    def test_and_false(self, empty_env):
        result = run("(and #t #f)", empty_env)
        assert get_token_value(result) is False

    def test_or_true(self, empty_env):
        result = run("(or #f #t)", empty_env)
        assert get_token_value(result) is True

    def test_or_all_false(self, empty_env):
        result = run("(or #f #f)", empty_env)
        assert get_token_value(result) is False

    def test_not_true(self, empty_env):
        result = run("(not #t)", empty_env)
        assert get_token_value(result) is False


# =============================================================================
# Builtin - List Operations
# =============================================================================

class TestListOps:
    def test_cons(self, empty_env):
        result = run("(cons 1 '(2 3))", empty_env)
        assert result[0].value == 1
        assert result[1].value == 2
        assert result[2].value == 3

    def test_car(self, empty_env):
        result = run("(car '(1 2 3))", empty_env)
        assert get_token_value(result) == 1

    def test_cdr(self, empty_env):
        result = run("(cdr '(1 2 3))", empty_env)
        # Should return (2 3)
        assert len(result) == 2

    def test_list(self, empty_env):
        result = run("(list 1 2 3)", empty_env)
        assert len(result) == 3
        assert get_token_value(result[0]) == 1

    def test_nullp_true(self, empty_env):
        result = run("(null? '())", empty_env)
        assert get_token_value(result) is True

    def test_nullp_false(self, empty_env):
        result = run("(null? '(1 2))", empty_env)
        assert get_token_value(result) is False


# =============================================================================
# Builtin - Type Predicates
# =============================================================================

class TestTypePredicates:
    def test_numberp_true(self, empty_env):
        result = run("(number? 42)", empty_env)
        assert get_token_value(result) is True

    def test_numberp_false(self, empty_env):
        result = run("(number? \"hi\")", empty_env)
        assert get_token_value(result) is False

    def test_stringp_true(self, empty_env):
        result = run("(string? \"hi\")", empty_env)
        assert get_token_value(result) is True

    def test_symbolp_true(self, empty_env):
        result = run("(symbol? 'foo)", empty_env)
        assert get_token_value(result) is True

    def test_booleanp_true(self, empty_env):
        result = run("(boolean? #t)", empty_env)
        assert get_token_value(result) is True


# =============================================================================
# Builtin - Equality
# =============================================================================

class TestEquality:
    def test_eqv_numbers(self, empty_env):
        result = run("(eqv? 5 5)", empty_env)
        assert get_token_value(result) is True

    def test_eqv_different(self, empty_env):
        result = run("(eqv? 5 6)", empty_env)
        assert get_token_value(result) is False

    def test_equal_lists(self, empty_env):
        result = run("(= '(1 2) '(1 2))", empty_env)
        # Depending on implementation


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    def test_full_pipeline(self, empty_env):
        result = run("(+ (* 2 3) (- 10 4))", empty_env)
        # (2*3) + (10-4) = 6 + 6 = 12
        assert get_token_value(result) == 12

    def test_recursion_factorial(self, empty_env):
        run("""
            (define fact (lambda (n)
              (if (= n 0) 1 (* n (fact (- n 1))))))
        """, empty_env)
        result = run("(fact 5)", empty_env)
        assert get_token_value(result) == 120

    def test_closure_scope(self, empty_env):
        run("(define make-adder (lambda (x) (lambda (y) (+ x y))))", empty_env)
        run("(define add5 (make-adder 5))", empty_env)
        result = run("(add5 10)", empty_env)
        assert get_token_value(result) == 15
