import pytest
from geometer.core.entities import Point, Line, Arc # Import Shape types for dependencies
from geometer.core.evaluator import parse_lisp_expression, evaluate, Environment, _standard_env, Symbol, Procedure

@pytest.fixture
def global_env():
    return _standard_env()

# --- Parsing Tests ---
def test_parse_number():
    assert parse_lisp_expression("123") == 123
    assert parse_lisp_expression("123.45") == 123.45
    assert parse_lisp_expression("-10") == -10
    assert parse_lisp_expression("+5.0") == 5.0

def test_parse_string():
    assert parse_lisp_expression('"hello"') == "hello"
    assert parse_lisp_expression('""') == ""

def test_parse_symbol():
    assert parse_lisp_expression("foo") == Symbol("foo")
    assert parse_lisp_expression("+") == Symbol("+")
    assert parse_lisp_expression("define") == Symbol("define")
    assert parse_lisp_expression("null?") == Symbol("null?")

def test_parse_point_literal():
    p = parse_lisp_expression("'(10,20)")
    assert isinstance(p, Point)
    assert p == Point(10, 20)
    assert not p.computed

    p_float = parse_lisp_expression("'(-5.5,12.3)")
    assert isinstance(p_float, Point)
    assert p_float == Point(-5.5, 12.3)
    assert not p_float.computed

def test_parse_list():
    assert parse_lisp_expression("(+ 1 2)") == [Symbol("+"), 1, 2]
    assert parse_lisp_expression("(define x 10)") == [Symbol("define"), Symbol("x"), 10]
    assert parse_lisp_expression("()") == []

def test_parse_nested_list():
    assert parse_lisp_expression("(if (> x 0) x (- x))") == \
           [Symbol("if"), [Symbol(">"), Symbol("x"), 0], Symbol("x"), [Symbol("-"), Symbol("x")]]

def test_parse_list_with_point():
    expr = parse_lisp_expression("(- '(10,20) '(5,5))")
    assert expr == [Symbol("-"), Point(10,20), Point(5,5)]

# --- Evaluation Tests ---

def test_evaluate_numbers_and_strings(global_env):
    assert evaluate("123", global_env) == 123
    assert evaluate('"hello"', global_env) == "hello"

def test_evaluate_point_literal(global_env):
    p = evaluate("'(10,20)", global_env)
    assert isinstance(p, Point)
    assert p == Point(10, 20)
    assert not p.computed

def test_evaluate_basic_arithmetic(global_env):
    assert evaluate("(+ 1 2)", global_env) == 3
    assert evaluate("(- 5 2)", global_env) == 3
    assert evaluate("(* 3 4)", global_env) == 12
    assert evaluate("(/ 10 2)", global_env) == 5.0
    assert evaluate("(+ 1 2 3)", global_env) == 6
    assert evaluate("(* 2 (+ 3 4))", global_env) == 14

def test_evaluate_point_arithmetic(global_env):
    p1 = evaluate("'(1,2)", global_env)
    p2 = evaluate("'(3,4)", global_env)
    
    p_sum = evaluate("(+ '(1,2) '(3,4))", global_env)
    assert p_sum == Point(4, 6)
    assert not p_sum.computed # Definite + Definite = Definite

    p_diff = evaluate("(- '(5,5) '(2,1))", global_env)
    assert p_diff == Point(3, 4)
    assert not p_diff.computed

    p_scaled = evaluate("(* '(2,3) 2)", global_env)
    assert p_scaled == Point(4, 6)
    assert not p_scaled.computed

    p_rscaled = evaluate("(* 3 '(2,3))", global_env)
    assert p_rscaled == Point(6, 9)
    assert not p_rscaled.computed

def test_evaluate_point_arithmetic_with_computed(global_env):
    # Setup for dependencies (simulated shapes)
    s1 = Line(Point(0,0), Point(1,1))
    s2 = Arc(Point(0,1), Point(1,0), Point(0,0))
    
    # Create a computed point manually for testing. In real usage, this would come from an intersect fn.
    global_env["_comp_p1"] = Point(1, 1, computed=True, dependencies=[s1])
    global_env["_comp_p2"] = Point(2, 2, computed=True, dependencies=[s2])
    global_env["_def_p"] = Point(10, 10)

    # Computed + Definite = Computed
    res_add = evaluate("(+ _comp_p1 _def_p)", global_env)
    assert res_add == Point(11, 11, computed=True)
    assert set(res_add.dependencies) == {s1}

    # Computed - Definite = Computed
    res_sub = evaluate("(- _comp_p1 _def_p)", global_env)
    assert res_sub == Point(-9, -9, computed=True)
    assert set(res_sub.dependencies) == {s1}

    # Computed * Scalar = Computed
    res_mul = evaluate("(* _comp_p1 5)", global_env)
    assert res_mul == Point(5, 5, computed=True)
    assert set(res_mul.dependencies) == {s1}

    # Scalar * Computed = Computed
    res_rmul = evaluate("(* 5 _comp_p1)", global_env)
    assert res_rmul == Point(5, 5, computed=True)
    assert set(res_rmul.dependencies) == {s1}

    # Computed (with deps) + Computed (with other deps)
    res_add_comp_comp = evaluate("(+ _comp_p1 _comp_p2)", global_env)
    assert res_add_comp_comp == Point(3, 3, computed=True)
    assert set(res_add_comp_comp.dependencies) == {s1, s2}

def test_evaluate_point_division_unsupported(global_env):
    with pytest.raises(TypeError, match="Division of Point objects is not supported"):
        evaluate("(/ '(10,20) '(2,2))", global_env)
    with pytest.raises(TypeError, match="Division of Point objects is not supported"):
        evaluate("(/ '(10,20) 2)", global_env)
    with pytest.raises(TypeError, match="Division of Point objects is not supported"):
        evaluate("(/ 2 '(10,20))", global_env) # this case will actually hit _polymorphic_op's point check first

def test_evaluate_define_and_lookup(global_env):
    evaluate("(define x 10)", global_env)
    assert global_env["x"] == 10
    assert evaluate("x", global_env) == 10

    evaluate("(define p '(1,1))", global_env)
    assert evaluate("p", global_env) == Point(1,1)

def test_evaluate_if_statement(global_env):
    assert evaluate("(if true 1 0)", global_env) == 1
    assert evaluate("(if false 1 0)", global_env) == 0
    assert evaluate("(if (> 5 3) (+ 1 1) (- 1 1))", global_env) == 2
    assert evaluate("(if (= 5 3) (+ 1 1) (- 1 1))", global_env) == 0

def test_evaluate_lambda(global_env):
    evaluate("(define double (lambda (x) (* x 2)))", global_env)
    assert isinstance(global_env["double"], Procedure)
    assert evaluate("(double 5)", global_env) == 10
    assert evaluate("(double '(1,2))", global_env) == Point(2,4)

    # Lambda with multiple arguments
    evaluate("(define add3 (lambda (x y z) (+ x y z)))", global_env)
    assert evaluate("(add3 1 2 3)", global_env) == 6

def test_evaluate_list_operations(global_env):
    assert evaluate("(list 1 2 3)", global_env) == [1, 2, 3]
    assert evaluate("(car (list 1 2 3))", global_env) == 1
    assert evaluate("(cdr (list 1 2 3))", global_env) == [2, 3]
    assert evaluate("(cons 0 (list 1 2))", global_env) == [0, 1, 2]
    assert evaluate("(car ())", global_env) is None
    assert evaluate("(cdr ())", global_env) == []
    assert evaluate("(cons 1 2)", global_env) == [1,2] # cons also works with non-list second arg

def test_evaluate_equality_and_comparison(global_env):
    assert evaluate("(= 1 1)", global_env) is True
    assert evaluate("(= 1 2)", global_env) is False
    assert evaluate("(> 5 3)", global_env) is True
    assert evaluate("(< 3 5)", global_env) is True
    assert evaluate("(= '(1,2) '(1,2))", global_env) is True
    assert evaluate("(= '(1,2) '(1,3))", global_env) is False

def test_evaluate_not_and_null(global_env):
    assert evaluate("(not true)", global_env) is False
    assert evaluate("(not false)", global_env) is True
    assert evaluate("(null? ())", global_env) is True
    assert evaluate("(null? (list 1))", global_env) is False

# --- Error Handling Tests ---
def test_evaluate_unbound_variable(global_env):
    with pytest.raises(NameError, match="unbound variable: y"):
        evaluate("y", global_env)

def test_evaluate_wrong_number_of_arguments_to_builtin(global_env):
    with pytest.raises(TypeError, match="Operator 'add' requires at least one argument"):
        evaluate("(+)", global_env)
    with pytest.raises(TypeError, match="car expects iterable argument"): # The 'car' lambda might give a different error depending on the exact implementation.
        evaluate("(car 1)", global_env)

def test_evaluate_wrong_number_of_arguments_to_special_form(global_env):
    with pytest.raises(TypeError, match="if expects 3 arguments"):
        evaluate("(if true 1)", global_env)
    with pytest.raises(TypeError, match="define expects 2 arguments"):
        evaluate("(define x)", global_env)
    with pytest.raises(TypeError, match="lambda expects 2 arguments"):
        evaluate("(lambda (x))", global_env)
