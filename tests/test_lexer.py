from lexer import lex
from language import TokenType


class TestLexerEmpty:
    def test_empty_string(self):
        tokens = list(lex(""))
        assert tokens == []

    def test_whitespace_only(self):
        tokens = list(lex("   \n\t  "))
        assert tokens == []


class TestLexerNumbers:
    def test_positive_integer(self):
        tokens = list(lex("42"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.NUMBER
        assert tokens[0].value == 42

    def test_negative_integer(self):
        tokens = list(lex("-5"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.NUMBER
        assert tokens[0].value == -5

    def test_float(self):
        tokens = list(lex("3.14"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.NUMBER
        assert tokens[0].value == 3.14


class TestLexerStrings:
    def test_simple_string(self):
        tokens = list(lex('"hello"'))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.STRING
        assert tokens[0].value == "hello"

    def test_empty_string(self):
        tokens = list(lex('""'))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.STRING
        assert tokens[0].value == ""


class TestLexerAtoms:
    def test_simple_atom(self):
        tokens = list(lex("foo"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.ATOM
        assert tokens[0].value == "foo"

    def test_atom_with_dash(self):
        tokens = list(lex("my-func"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.ATOM
        assert tokens[0].value == "my-func"

    def test_plus_atom(self):
        tokens = list(lex("+"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.ATOM
        assert tokens[0].value == "+"


class TestLexerBooleans:
    def test_true(self):
        tokens = list(lex("#t"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.BOOLEAN
        assert tokens[0].value is True

    def test_false(self):
        tokens = list(lex("#f"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.BOOLEAN
        assert tokens[0].value is False


class TestLexerPoints:
    def test_point(self):
        tokens = list(lex("'(1,2)"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.POINT
        assert tokens[0].value == (1, 2)

    def test_negative_point(self):
        tokens = list(lex("'(-3,4)"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.POINT
        assert tokens[0].value == (-3, 4)


class TestLexerParentheses:
    def test_open_paren(self):
        tokens = list(lex("("))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.CHARACTER
        assert tokens[0].value == "("

    def test_close_paren(self):
        tokens = list(lex(")"))
        assert len(tokens) == 1
        assert tokens[0].kind == TokenType.CHARACTER
        assert tokens[0].value == ")"

    def test_balanced_paren(self):
        tokens = list(lex("(()())"))
        assert len(tokens) == 6


class TestLexerWhitespace:
    def test_spaces_between_tokens(self):
        tokens = list(lex("1 2 3"))
        assert len(tokens) == 3
        assert all(t.kind == TokenType.NUMBER for t in tokens)

    def test_newlines_between_tokens(self):
        tokens = list(lex("1\n2\n3"))
        assert len(tokens) == 3

    def test_tabs_between_tokens(self):
        tokens = list(lex("1\t2"))
        assert len(tokens) == 2


class TestLexerIntegration:
    def test_simple_expression(self):
        tokens = list(lex("(+ 1 2)"))
        # Should have: (, +, 1, 2, )
        assert len(tokens) == 5
        assert tokens[0].value == "("
        assert tokens[1].value == "+"

    def test_nested_expression(self):
        tokens = list(lex("(+ (* 2 3) (- 5 1))"))
        # More complex nested expression
        assert tokens[0].value == "("

    def test_multiple_expressions(self):
        tokens = list(lex("(1) (2)"))
        # Two separate s-expressions
        assert len(tokens) == 6  # (, 1, ), (, 2, )
