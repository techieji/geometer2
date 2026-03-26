from lexer import lex
from parser import parse
from language import TokenType


class TestParserLiterals:
    def test_parse_number(self):
        tokens = list(lex("42"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.NUMBER
        assert tree.value.value == 42

    def test_parse_negative_number(self):
        tokens = list(lex("-5"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.NUMBER

    def test_parse_float(self):
        tokens = list(lex("3.14"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.NUMBER
        assert tree.value.value == 3.14

    def test_parse_string(self):
        tokens = list(lex('"hello"'))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.STRING
        assert tree.value.value == "hello"

    def test_parse_atom(self):
        tokens = list(lex("foo"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.ATOM
        assert tree.value.value == "foo"

    def test_parse_boolean_true(self):
        tokens = list(lex("#t"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.BOOLEAN
        assert tree.value.value is True

    def test_parse_boolean_false(self):
        tokens = list(lex("#f"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.BOOLEAN
        assert tree.value.value is False


class TestParserCompound:
    def test_simple_s_expression(self):
        tokens = list(lex("(1 2 3)"))
        tree = parse(tokens)
        assert tree.is_literal is False
        assert len(tree.value) == 3
        assert all(child.is_literal for child in tree.value)

    def test_nested_s_expression(self):
        tokens = list(lex("((1 2) (3 4))"))
        tree = parse(tokens)
        assert tree.is_literal is False
        assert len(tree.value) == 2
        # First child is (1 2)
        assert tree.value[0].value[0].value.value == 1
        # Second child is (3 4)
        assert tree.value[1].value[1].value.value == 4

    def test_nested_single_element(self):
        tokens = list(lex("((1))"))
        tree = parse(tokens)
        assert tree.is_literal is False
        assert len(tree.value) == 1
        assert tree.value[0].is_literal is False

    def test_deeply_nested(self):
        tokens = list(lex("(((1)))"))
        tree = parse(tokens)
        assert tree.is_literal is False
        inner = tree.value[0].value[0].value[0]
        assert inner.is_literal is True
        assert inner.value.value == 1


class TestParserQuote:
    def test_quote_shorthand(self):
        tokens = list(lex("'(1 2)"))
        tree = parse(tokens)
        # '(1 2) should parse as (quote (1 2))
        assert tree.is_literal is False
        # First element should be 'quote'
        first = tree.value[0]
        assert first.is_literal is True
        assert first.value.value == "quote"


class TestParserPoint:
    def test_point_literal(self):
        tokens = list(lex("'(1,2)"))
        tree = parse(tokens)
        assert tree.is_literal is True
        assert tree.value.kind == TokenType.POINT
        assert tree.value.value == (1, 2)


class TestParserMultiple:
    def test_two_expressions(self):
        tokens = list(lex("1 2"))
        tree = parse(tokens)
        # Returns the first expression
        assert tree.is_literal is True
        # Should have remaining tokens?
        # This depends on parser design


class TestParserEdgeCases:
    def test_whitespace_handling(self):
        tokens = list(lex("  (  1  2  )  "))
        tree = parse(tokens)
        assert tree.is_literal is False
        assert len(tree.value) == 2

    def test_newline_handling(self):
        tokens = list(lex("(1\n2)"))
        tree = parse(tokens)
        assert tree.is_literal is False
        assert len(tree.value) == 2
