"""Tests for the Lexer module (Task 2.1)."""

import pytest
from geometer.lisp.lexer import Lexer, Token, TokenType


class TestLexerBasicTokens:
    """Test basic token generation."""
    
    def test_empty_input(self):
        lexer = Lexer("")
        tokens = list(lexer.tokenize())
        assert tokens == []
    
    def test_whitespace_only(self):
        lexer = Lexer("   \n\t  ")
        tokens = list(lexer.tokenize())
        assert tokens == []
    
    def test_single_open_paren(self):
        lexer = Lexer("(")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[0].value == "("
    
    def test_single_close_paren(self):
        lexer = Lexer(")")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.RPAREN
        assert tokens[0].value == ")"
    
    def test_balanced_parentheses(self):
        lexer = Lexer("()")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 2
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.RPAREN


class TestLexerNumbers:
    """Test number tokenization."""
    
    def test_integer(self):
        lexer = Lexer("42")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 42
    
    def test_negative_integer(self):
        lexer = Lexer("-42")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == -42
    
    def test_decimal_number(self):
        lexer = Lexer("3.14")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 3.14
    
    def test_negative_decimal(self):
        lexer = Lexer("-3.14")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == -3.14
    
    def test_zero(self):
        lexer = Lexer("0")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 0
    
    def test_scientific_notation(self):
        lexer = Lexer("1e10")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == 1e10


class TestLexerStrings:
    """Test string tokenization."""
    
    def test_simple_string(self):
        lexer = Lexer('"hello"')
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello"
    
    def test_empty_string(self):
        lexer = Lexer('""')
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == ""
    
    def test_string_with_spaces(self):
        lexer = Lexer('"hello world"')
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "hello world"
    
    def test_string_with_escaped_quote(self):
        lexer = Lexer('"hello\\"world"')
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == 'hello"world'


class TestLexerSymbols:
    """Test symbol tokenization."""
    
    def test_simple_symbol(self):
        lexer = Lexer("hello")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.SYMBOL
        assert tokens[0].value == "hello"
    
    def test_symbol_with_dash(self):
        lexer = Lexer("my-variable")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.SYMBOL
        assert tokens[0].value == "my-variable"
    
    def test_symbol_with_numbers(self):
        lexer = Lexer("var123")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.SYMBOL
        assert tokens[0].value == "var123"
    
    def test_symbol_with_plus_sign(self):
        lexer = Lexer("+")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.SYMBOL
        assert tokens[0].value == "+"
    
    def test_symbol_with_angle_brackets(self):
        lexer = Lexer("<=")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.SYMBOL
        assert tokens[0].value == "<="


class TestLexerPointSyntax:
    """Test point syntax tokenization: '(<x>,<y>)'"""
    
    def test_simple_point(self):
        lexer = Lexer("'(1,2)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == (1, 2)
    
    def test_point_with_decimals(self):
        lexer = Lexer("'(3.5,4.5)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == (3.5, 4.5)
    
    def test_point_with_negative_coordinates(self):
        lexer = Lexer("'(-1,-2)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == (-1, -2)
    
    def test_point_with_space_after_comma(self):
        lexer = Lexer("'(1, 2)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == (1, 2)
    
    def test_point_zero_coordinates(self):
        lexer = Lexer("'(0,0)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.POINT
        assert tokens[0].value == (0, 0)


class TestLexerRealisticUsage:
    """Test realistic Scheme expressions."""
    
    def test_define_expression(self):
        lexer = Lexer("(define x 5)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 4
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.SYMBOL
        assert tokens[1].value == "define"
        assert tokens[2].type == TokenType.SYMBOL
        assert tokens[2].value == "x"
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == 5
    
    def test_lambda_expression(self):
        lexer = Lexer("(lambda (x) (* x 2))")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.SYMBOL
        assert tokens[1].value == "lambda"
        assert tokens[2].type == TokenType.LPAREN
    
    def test_nested_expressions(self):
        lexer = Lexer("((a b) (c d))")
        tokens = list(lexer.tokenize())
        # Should have: LPAREN LPAREN SYMBOL SYMBOL RPAREN LPAREN SYMBOL SYMBOL RPAREN RPAREN
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.LPAREN
        assert tokens[2].type == TokenType.SYMBOL
        assert tokens[2].value == "a"
    
    def test_quote_expression(self):
        lexer = Lexer("'(1 2 3)")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == TokenType.QUOTE
    
    def test_conditional_expression(self):
        lexer = Lexer("(if (> x 0) x (- x))")
        tokens = list(lexer.tokenize())
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.SYMBOL
        assert tokens[1].value == "if"
    
    def test_string_in_expression(self):
        lexer = Lexer('(print "hello world")')
        tokens = list(lexer.tokenize())
        assert tokens[2].type == TokenType.STRING
        assert tokens[2].value == "hello world"
    
    def test_mixed_point_and_expressions(self):
        lexer = Lexer("(line '(0,0) '(1,1))")
        tokens = list(lexer.tokenize())
        # Should tokenize line, quote, point, quote, point
        assert tokens[1].type == TokenType.SYMBOL
        assert tokens[2].type == TokenType.QUOTE
        assert tokens[3].type == TokenType.POINT
        assert tokens[3].value == (0, 0)


class TestLexerEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_multiple_spaces_between_tokens(self):
        lexer = Lexer("  (  define   x   5  )")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 5
        assert tokens[0].type == TokenType.LPAREN
        assert tokens[1].type == TokenType.SYMBOL
        assert tokens[1].value == "define"
    
    def test_newlines_between_tokens(self):
        lexer = Lexer("(define\nx\n5)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 4
    
    def test_tabs_between_tokens(self):
        lexer = Lexer("(define\tx\t5)")
        tokens = list(lexer.tokenize())
        assert len(tokens) == 4
    
    def test_comment_handling(self):
        lexer = Lexer("(define x 5) ; this is a comment")
        tokens = list(lexer.tokenize())
        # Comments should be skipped
        assert len(tokens) == 4
        assert tokens[-1].value == 5
    
    def test_unterminated_string(self):
        lexer = Lexer('"unterminated')
        with pytest.raises(ValueError, match="unterminated string"):
            list(lexer.tokenize())
    
    def test_invalid_point_syntax(self):
        lexer = Lexer("'(1 2 3)")  # Too many values
        with pytest.raises(ValueError, match="invalid point"):
            list(lexer.tokenize())
    
    def test_unbalanced_parentheses(self):
        lexer = Lexer("((())")
        with pytest.raises(ValueError, match="unbalanced"):
            list(lexer.tokenize())


class TestLexerTokenPositions:
    """Test that tokens track their positions correctly."""
    
    def test_position_tracking(self):
        lexer = Lexer("(define x 5)")
        tokens = list(lexer.tokenize())
        assert tokens[0].line == 1
        assert tokens[0].column == 1
        assert tokens[1].line == 1
        assert tokens[1].column == 2
    
    def test_position_after_newline(self):
        lexer = Lexer("(define\nx)")
        tokens = list(lexer.tokenize())
        # x should be on line 2
        assert tokens[2].line == 2
        assert tokens[2].column == 1
