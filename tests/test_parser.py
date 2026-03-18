"""Tests for the Parser module (task 2.2)."""

import pytest
from geometer.lisp.parser import Parser, ASTNode, AtomNode, ListNode, PointNode


class TestParserBasicParsing:
    """Test basic S-expression parsing."""

    def test_empty_input(self):
        """Parse empty string."""
        parser = Parser("")
        ast = parser.parse()
        assert ast == []

    def test_whitespace_only(self):
        """Parse whitespace-only string."""
        parser = Parser("   \n\t  ")
        ast = parser.parse()
        assert ast == []

    def test_single_atom(self):
        """Parse a single atom."""
        parser = Parser("hello")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], AtomNode)
        assert ast[0].value == "hello"

    def test_single_number(self):
        """Parse a single number."""
        parser = Parser("42")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], AtomNode)
        assert ast[0].value == 42

    def test_single_float(self):
        """Parse a single float."""
        parser = Parser("3.14")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], AtomNode)
        assert ast[0].value == 3.14

    def test_single_string(self):
        """Parse a single string."""
        parser = Parser('"hello world"')
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], AtomNode)
        assert ast[0].value == "hello world"


class TestParserLists:
    """Test list parsing."""

    def test_empty_list(self):
        """Parse empty list."""
        parser = Parser("()")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements == []

    def test_simple_list(self):
        """Parse simple list."""
        parser = Parser("(a b c)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert len(ast[0].elements) == 3
        assert ast[0].elements[0].value == "a"
        assert ast[0].elements[1].value == "b"
        assert ast[0].elements[2].value == "c"

    def test_nested_list(self):
        """Parse nested list."""
        parser = Parser("(a (b c) d)")
        ast = parser.parse()
        assert len(ast) == 1
        outer = ast[0]
        assert isinstance(outer, ListNode)
        assert outer.elements[0].value == "a"
        assert isinstance(outer.elements[1], ListNode)
        assert outer.elements[1].elements[0].value == "b"
        assert outer.elements[1].elements[1].value == "c"
        assert outer.elements[2].value == "d"

    def test_deeply_nested_list(self):
        """Parse deeply nested list."""
        parser = Parser("(((a)))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert isinstance(ast[0].elements[0], ListNode)
        assert isinstance(ast[0].elements[0].elements[0], AtomNode)
        assert ast[0].elements[0].elements[0].value == "a"

    def test_multiple_lists(self):
        """Parse multiple lists."""
        parser = Parser("(a b) (c d)")
        ast = parser.parse()
        assert len(ast) == 2
        assert ast[0].elements[0].value == "a"
        assert ast[1].elements[0].value == "c"


class TestParserPointSyntax:
    """Test point literal parsing."""

    def test_simple_point(self):
        """Parse simple point."""
        parser = Parser("(10, 20)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], PointNode)
        assert ast[0].x == 10
        assert ast[0].y == 20

    def test_point_with_decimals(self):
        """Parse point with decimal coordinates."""
        parser = Parser("(3.5, 7.2)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], PointNode)
        assert ast[0].x == 3.5
        assert ast[0].y == 7.2

    def test_point_with_negative_coordinates(self):
        """Parse point with negative coordinates."""
        parser = Parser("(-5, -10)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], PointNode)
        assert ast[0].x == -5
        assert ast[0].y == -10

    def test_point_zero_coordinates(self):
        """Parse point with zero coordinates."""
        parser = Parser("(0, 0)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], PointNode)
        assert ast[0].x == 0
        assert ast[0].y == 0

    def test_point_in_list(self):
        """Parse point inside a list."""
        parser = Parser("(line (0, 0) (10, 10))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        # Second element should be a point
        assert isinstance(ast[0].elements[1], PointNode)
        assert ast[0].elements[1].x == 0
        assert ast[0].elements[1].y == 0
        # Third element should be a point
        assert isinstance(ast[0].elements[2], PointNode)
        assert ast[0].elements[2].x == 10
        assert ast[0].elements[2].y == 10


class TestParserQuotedExpressions:
    """Test quoted expression parsing."""

    def test_quote_syntax(self):
        """Parse quote syntax."""
        parser = Parser("'hello")
        ast = parser.parse()
        assert len(ast) == 1
        # Quote should create a list with 'quote' and the atom
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "quote"
        assert ast[0].elements[1].value == "hello"

    def test_quote_list(self):
        """Parse quoted list."""
        parser = Parser("'(a b c)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "quote"
        assert isinstance(ast[0].elements[1], ListNode)
        assert ast[0].elements[1].elements[0].value == "a"
        assert ast[0].elements[1].elements[1].value == "b"
        assert ast[0].elements[1].elements[2].value == "c"

    def test_quote_point(self):
        """Parse quoted point."""
        parser = Parser("'(10 20)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "quote"
        assert isinstance(ast[0].elements[1], PointNode)

    def test_double_quote(self):
        """Parse double quote."""
        parser = Parser("''hello")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        # Should be (quote (quote hello))
        assert ast[0].elements[0].value == "quote"
        inner = ast[0].elements[1]
        assert isinstance(inner, ListNode)
        assert inner.elements[0].value == "quote"
        assert inner.elements[1].value == "hello"


class TestParserRealisticUsage:
    """Test realistic Scheme expressions."""

    def test_define_expression(self):
        """Parse define expression."""
        parser = Parser("(define x 10)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "define"
        assert ast[0].elements[1].value == "x"
        assert ast[0].elements[2].value == 10

    def test_lambda_expression(self):
        """Parse lambda expression."""
        parser = Parser("(lambda (x) (* x x))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "lambda"
        assert ast[0].elements[1].elements[0].value == "x"
        assert ast[0].elements[2].elements[0].value == "*"

    def test_nested_expressions(self):
        """Parse nested expressions."""
        parser = Parser("(if (> x 0) (point 1 2) (point 3 4))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "if"

    def test_conditional_expression(self):
        """Parse conditional expression."""
        parser = Parser("(if #t 1 2)")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "if"
        assert ast[0].elements[1].value == "#t"

    def test_string_in_expression(self):
        """Parse string inside expression."""
        parser = Parser('(text "Hello World" (10, 20))')
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[1].value == "Hello World"

    def test_mixed_point_and_expressions(self):
        """Parse mixed points and expressions."""
        parser = Parser("(line (0, 0) (+ 1 2))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert isinstance(ast[0].elements[1], PointNode)
        assert isinstance(ast[0].elements[2], ListNode)

    def test_let_expression(self):
        """Parse let expression."""
        parser = Parser("(let ((x 1) (y 2)) (+ x y))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert ast[0].elements[0].value == "let"

    def test_multiple_expressions(self):
        """Parse multiple expressions on one line."""
        parser = Parser("(define a 1) (define b 2)")
        ast = parser.parse()
        assert len(ast) == 2
        assert ast[0].elements[1].value == "a"
        assert ast[1].elements[1].value == "b"


class TestParserEdgeCases:
    """Test edge cases and error conditions."""

    def test_extra_whitespace(self):
        """Parse with extra whitespace."""
        parser = Parser("   (a b c)   ")
        ast = parser.parse()
        assert len(ast) == 1

    def test_newlines_between_tokens(self):
        """Parse with newlines between tokens."""
        parser = Parser("(a\n b\n c)")
        ast = parser.parse()
        assert len(ast) == 1
        assert len(ast[0].elements) == 3

    def test_tabs_between_tokens(self):
        """Parse with tabs between tokens."""
        parser = Parser("(a\tb\tc)")
        ast = parser.parse()
        assert len(ast) == 1

    def test_comment_handling(self):
        """Parse with comments (should ignore)."""
        parser = Parser("(a b c) ; this is a comment")
        ast = parser.parse()
        assert len(ast) == 1

    def test_unbalanced_parentheses(self):
        """Parse unbalanced parentheses should raise error."""
        parser = Parser("(a b c")
        with pytest.raises(SyntaxError):
            parser.parse()

    def test_unbalanced_parentheses_extra_close(self):
        """Parse extra closing parenthesis should raise error."""
        parser = Parser("(a b c))")
        with pytest.raises(SyntaxError):
            parser.parse()

    def test_invalid_point_syntax_missing_y(self):
        """Parse invalid point syntax (missing y)."""
        parser = Parser("(10,)")
        with pytest.raises(SyntaxError):
            parser.parse()

    def test_invalid_point_syntax_missing_both(self):
        """Parse invalid point syntax (missing both)."""
        parser = Parser("(,)")
        with pytest.raises(SyntaxError):
            parser.parse()

    def test_point_without_parens(self):
        """Parse point-like syntax without parens should be symbol."""
        parser = Parser("10,20")
        ast = parser.parse()
        # Should be parsed as a symbol, not a point
        assert len(ast) == 1
        assert ast[0].value == "10,20"

    def test_empty_nested_list(self):
        """Parse empty nested list."""
        parser = Parser("((()))")
        ast = parser.parse()
        assert len(ast) == 1
        assert isinstance(ast[0], ListNode)
        assert len(ast[0].elements) == 1
        assert isinstance(ast[0].elements[0], ListNode)
        assert ast[0].elements[0].elements == []


class TestParserTokenPositions:
    """Test that parser tracks positions correctly."""

    def test_position_tracking(self):
        """Parser should track line/column positions."""
        parser = Parser("(a b)")
        ast = parser.parse()
        # AST nodes should have line/column info
        assert ast[0].line == 1
        assert ast[0].column == 1

    def test_position_after_newline(self):
        """Position should be correct after newline."""
        parser = Parser("\n(a b)")
        ast = parser.parse()
        assert ast[0].line == 2
        assert ast[0].column == 1


class TestParserASTNode:
    """Test ASTNode functionality."""

    def test_atom_node_creation(self):
        """Create AtomNode with various types."""
        node = AtomNode("test")
        assert node.type == "atom"
        assert node.value == "test"

    def test_list_node_creation(self):
        """Create ListNode."""
        node = ListNode([AtomNode("a"), AtomNode("b")])
        assert node.type == "list"
        assert len(node.elements) == 2

    def test_point_node_creation(self):
        """Create PointNode."""
        node = PointNode(5, 10)
        assert node.type == "point"
        assert node.x == 5
        assert node.y == 10

    def test_ast_node_repr(self):
        """Test ASTNode string representation."""
        node = AtomNode("hello")
        assert "hello" in repr(node)
