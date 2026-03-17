"""Parser module for Geometer Lisp interpreter.

This module provides S-expression parsing and AST node construction.
"""

from typing import List, Any, Union, Optional
from geometer.lisp.lexer import Lexer, Token, TokenType


class ASTNode:
    """Base class for all AST nodes."""

    def __init__(self, line: int = 1, column: int = 1):
        self.line = line
        self.column = column

    @property
    def type(self) -> str:
        raise NotImplementedError("Subclasses must implement 'type' property")


class AtomNode(ASTNode):
    """Represents an atom (symbol, number, string, boolean)."""

    def __init__(
        self,
        value: Union[str, int, float, bool],
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self._value = value

    @property
    def type(self) -> str:
        return "atom"

    @property
    def value(self) -> Union[str, int, float, bool]:
        return self._value

    @value.setter
    def value(self, val: Union[str, int, float, bool]) -> None:
        self._value = val

    def __repr__(self) -> str:
        return f"AtomNode({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AtomNode):
            return False
        return self._value == other._value


class ListNode(ASTNode):
    """Represents a list of AST nodes (S-expression)."""

    def __init__(
        self,
        elements: List[ASTNode],
        line: int = 1,
        column: int = 1
    ):
        super().__init__(line, column)
        self._elements = elements

    @property
    def type(self) -> str:
        return "list"

    @property
    def elements(self) -> List[ASTNode]:
        return self._elements

    @elements.setter
    def elements(self, val: List[ASTNode]) -> None:
        self._elements = val

    def __repr__(self) -> str:
        return f"ListNode({self._elements!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ListNode):
            return False
        return self._elements == other._elements


class PointNode(ASTNode):
    """Represents a point literal (x, y)."""

    def __init__(self, x: float, y: float, line: int = 1, column: int = 1):
        super().__init__(line, column)
        self._x = x
        self._y = y

    @property
    def type(self) -> str:
        return "point"

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, val: float) -> None:
        self._x = val

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, val: float) -> None:
        self._y = val

    def __repr__(self) -> str:
        return f"PointNode({self._x}, {self._y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointNode):
            return False
        return self._x == other._x and self._y == other._y


class Parser:
    """Parser for S-expressions.

    Transforms a sequence of tokens into an Abstract Syntax Tree (AST).
    """

    def __init__(self, source: str):
        self.source = source
        self.lexer = Lexer(source)
        self.tokens: List[Token] = []
        self.pos: int = 0

    def parse(self) -> List[ASTNode]:
        """Parse the source code and return a list of AST nodes.

        Returns:
            List of AST nodes representing the parsed S-expressions.

        Raises:
            SyntaxError: If there are parsing errors.
        """
        self.tokens = self.lexer.tokenize()
        self.pos = 0

        results: List[ASTNode] = []

        while self.pos < len(self.tokens):
            node = self._parse_expr()
            if node is not None:
                results.append(node)

        return results

    def _current_token(self) -> Optional[Token]:
        """Get the current token without advancing."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _peek_token(self, offset: int = 1) -> Optional[Token]:
        """Peek at a token ahead by offset positions."""
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    def _advance(self) -> Optional[Token]:
        """Advance to the next token and return the previous current token."""
        token = self._current_token()
        self.pos += 1
        return token

    def _expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type and advance past it.

        Raises:
            SyntaxError: If the current token is not the expected type.
        """
        token = self._current_token()
        if token is None:
            raise SyntaxError(f"Expected {token_type}, got end of input")

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type} "
                f"at line {token.line}, column {token.column}"
            )

        return self._advance()

    def _parse_expr(self) -> Optional[ASTNode]:
        """Parse a single expression.

        Returns:
            An AST node, or None if end of input.
        """
        token = self._current_token()

        if token is None:
            return None

        # Handle opening parenthesis - parse a list
        if token.type == TokenType.LPAREN:
            return self._parse_list()

        # Handle quote
        if token.type == TokenType.QUOTE:
            return self._parse_quote()

        # Handle atoms: symbols, numbers, strings
        if token.type in (TokenType.SYMBOL, TokenType.NUMBER, TokenType.STRING):
            self._advance()
            return self._make_atom(token)

        # Handle boolean
        if token.type == TokenType.BOOLEAN:
            self._advance()
            return AtomNode(token.value, token.line, token.column)

        # Unexpected token
        raise SyntaxError(
            f"Unexpected token {token.type} "
            f"at line {token.line}, column {token.column}"
        )

    def _parse_list(self) -> ListNode:
        """Parse a list expression (S-expression in parentheses)."""
        token = self._advance()  # consume LPAREN
        line = token.line if token else 1
        column = token.column if token else 1

        elements: List[ASTNode] = []

        while self._current_token() is not None:
            token = self._current_token()

            # End of list
            if token.type == TokenType.RPAREN:
                self._advance()  # consume RPAREN
                return ListNode(elements, line, column)

            # Check for point syntax: (x, y)
            if token.type == TokenType.LPAREN:
                # Check if this is a point by looking ahead
                if self._is_point_syntax():
                    point_node = self._parse_point()
                    if point_node:
                        elements.append(point_node)
                        continue

                # Not a point, parse as regular list
                elements.append(self._parse_expr())
                continue

            # Parse quoted expression inside list
            if token.type == TokenType.QUOTE:
                elements.append(self._parse_quote())
                continue

            # Parse the expression
            node = self._parse_expr()
            if node is not None:
                elements.append(node)

        # Unbalanced parentheses
        raise SyntaxError(
            f"Unbalanced parentheses: missing ')' "
            f"at line {line}, column {column}"
        )

    def _is_point_syntax(self) -> bool:
        """Check if the current position starts a point syntax.

        Point syntax is: (number, number)
        """
        # Current token should be LPAREN, we've already checked that
        # Look ahead: LPAREN -> NUMBER -> COMMA -> NUMBER -> RPAREN
        if self._current_token() and self._current_token().type == TokenType.LPAREN:
            # Need at least 5 tokens ahead: ( num , num )
            if self._peek_token(1) and self._peek_token(1).type == TokenType.NUMBER:
                if self._peek_token(2) and self._peek_token(2).type == TokenType.COMMA:
                    if self._peek_token(3) and self._peek_token(3).type == TokenType.NUMBER:
                        # Check for RPAREN or end of tokens
                        peek4 = self._peek_token(4)
                        if peek4 and peek4.type == TokenType.RPAREN:
                            return True
                        elif peek4 is None:
                            # End of input after the number
                            return True
        return False

    def _parse_point(self) -> PointNode:
        """Parse a point literal: (x, y)"""
        token = self._advance()  # consume LPAREN
        line = token.line if token else 1
        column = token.column if token else 1

        # Parse x coordinate
        x_token = self._current_token()
        if x_token is None or x_token.type != TokenType.NUMBER:
            raise SyntaxError(
                f"Expected number for x coordinate, got {x_token.type if x_token else 'end of input'}"
            )
        x = x_token.value
        self._advance()

        # Expect comma
        comma = self._current_token()
        if comma is None or comma.type != TokenType.COMMA:
            raise SyntaxError(
                f"Expected comma in point syntax, got {comma.type if comma else 'end of input'}"
            )
        self._advance()

        # Parse y coordinate
        y_token = self._current_token()
        if y_token is None or y_token.type != TokenType.NUMBER:
            raise SyntaxError(
                f"Expected number for y coordinate, got {y_token.type if y_token else 'end of input'}"
            )
        y = y_token.value
        self._advance()

        # Expect closing parenthesis
        rparen = self._current_token()
        if rparen is None or rparen.type != TokenType.RPAREN:
            raise SyntaxError(
                f"Expected ')' in point syntax, got {rparen.type if rparen else 'end of input'}"
            )
        self._advance()

        return PointNode(x, y, line, column)

    def _parse_quote(self) -> ListNode:
        """Parse a quoted expression: 'expr"""
        quote_token = self._advance()  # consume QUOTE
        line = quote_token.line if quote_token else 1
        column = quote_token.column if quote_token else 1

        # Parse the quoted expression
        expr = self._parse_expr()

        if expr is None:
            # Quote with nothing after it
            expr = ListNode([], line, column + 1)

        # Build (quote expr)
        return ListNode(
            [AtomNode("quote", line, column), expr],
            line,
            column
        )

    def _make_atom(self, token: Token) -> AtomNode:
        """Convert a token to an appropriate AtomNode."""
        if token.type == TokenType.NUMBER:
            # Convert to int or float
            value = token.value
            if isinstance(value, float) or (isinstance(value, str) and '.' in value):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    pass
            else:
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    pass
            return AtomNode(value, token.line, token.column)
        elif token.type == TokenType.STRING:
            return AtomNode(token.value, token.line, token.column)
        else:
            # Symbol
            return AtomNode(token.value, token.line, token.column)
