"""Lexer for Geometer Lisp interpreter (Task 2.1)."""

import re
from enum import Enum, auto
from typing import List, Optional, Tuple, Union


class TokenType(Enum):
    """Token types for the lexer."""
    LPAREN = auto()
    RPAREN = auto()
    NUMBER = auto()
    STRING = auto()
    SYMBOL = auto()
    QUOTE = auto()
    POINT = auto()
    COMMENT = auto()
    EOF = auto()


class Token:
    """Represents a token in the source code."""
    
    def __init__(
        self,
        type: TokenType,
        value: Union[str, int, float, Tuple[float, float]],
        line: int = 1,
        column: int = 1
    ):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class Lexer:
    """Tokenizes Scheme source code."""
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
    
    def tokenize(self) -> List[Token]:
        """Generate tokens from the source code."""
        tokens = []
        
        while self.pos < len(self.source):
            # Skip whitespace
            self._skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.source[self.pos] == ';':
                self._skip_comment()
                continue
            
            # Get next token
            char = self.source[self.pos]
            
            # Parentheses
            if char == '(':
                tokens.append(self._create_token(TokenType.LPAREN, '('))
            elif char == ')':
                tokens.append(self._create_token(TokenType.RPAREN, ')'))
            
            # Quote
            elif char == "'":
                tokens.append(self._read_quote())
            
            # String
            elif char == '"':
                tokens.append(self._read_string())
            
            # Number
            elif char.isdigit() or (char == '-' and self._has_number_after_minus()):
                tokens.append(self._read_number())
            
            # Symbol
            elif char.isalpha() or char in '+-*/<>=_':
                tokens.append(self._read_symbol())
            
            else:
                raise ValueError(
                    f"Unexpected character '{char}' "
                    f"at line {self.line}, column {self.column}"
                )
        
        return tokens
    
    def _has_number_after_minus(self) -> bool:
        """Check if there's a digit after a minus sign."""
        if self.pos + 1 < len(self.source):
            return self.source[self.pos + 1].isdigit()
        return False
    
    def _skip_whitespace(self) -> None:
        """Skip whitespace characters."""
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char in ' \t\n\r':
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1
            else:
                break
    
    def _skip_comment(self) -> None:
        """Skip comment until end of line."""
        while self.pos < len(self.source) and self.source[self.pos] != '\n':
            self.pos += 1
    
    def _create_token(
        self,
        token_type: TokenType,
        value: Union[str, int, float, Tuple[float, float]]
    ) -> Token:
        """Create a token at the current position."""
        token = Token(token_type, value, self.line, self.column)
        
        # Advance position
        value_str = str(value)
        self.column += len(value_str)
        self.pos += len(value_str)
        
        return token
    
    def _read_quote(self) -> Token:
        """Read a quote token, checking for point syntax."""
        start_line = self.line
        start_column = self.column
        self.pos += 1  # Skip '
        
        # Check if followed by opening paren for point
        if self.pos < len(self.source) and self.source[self.pos] == '(':
            return self._read_point(start_line, start_column)
        
        # Just a quote, return it
        return Token(TokenType.QUOTE, "'", start_line, start_column)
    
    def _read_point(self, start_line: int, start_column: int) -> Token:
        """Read a point literal: '(<x>,<y>)"""
        self.pos += 1  # Skip (
        
        # Skip whitespace
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
        
        # Read x coordinate (get the value, not the token)
        x_token = self._read_number()
        x = x_token.value
        
        # Skip whitespace around comma
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
        
        # Expect comma
        if self.pos >= len(self.source) or self.source[self.pos] != ',':
            raise ValueError(f"invalid point: expected comma at line {self.line}")
        self.pos += 1  # Skip ,
        
        # Skip whitespace after comma
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
        
        # Read y coordinate (get the value, not the token)
        y_token = self._read_number()
        y = y_token.value
        
        # Skip whitespace before closing paren
        while self.pos < len(self.source) and self.source[self.pos] in ' \t':
            self.pos += 1
        
        # Expect closing paren
        if self.pos >= len(self.source) or self.source[self.pos] != ')':
            raise ValueError(f"invalid point: expected closing paren at line {self.line}")
        self.pos += 1  # Skip )
        
        # Convert to tuple
        value = (x, y)
        
        return Token(TokenType.POINT, value, start_line, start_column)
    
    def _read_number(self) -> Token:
        """Read a number from the current position."""
        start_line = self.line
        start_column = self.column
        
        # Handle negative sign
        negative = False
        if self.source[self.pos] == '-':
            negative = True
            self.pos += 1
        
        # Read digits before decimal
        int_part = ''
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            int_part += self.source[self.pos]
            self.pos += 1
        
        # Read decimal part
        has_decimal = False
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            has_decimal = True
            self.pos += 1
        
        dec_part = ''
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            dec_part += self.source[self.pos]
            self.pos += 1
        
        # Read exponent
        has_exponent = False
        if self.pos < len(self.source) and self.source[self.pos] in 'eE':
            has_exponent = True
            self.pos += 1
        
        exp_sign = ''
        if self.pos < len(self.source) and self.source[self.pos] in '+-':
            exp_sign = self.source[self.pos]
            self.pos += 1
        
        exp_part = ''
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            exp_part += self.source[self.pos]
            self.pos += 1
        
        # Build the number
        num_str = int_part
        if has_decimal:
            num_str += '.' + dec_part
        if has_exponent:
            num_str += 'e' + exp_sign + exp_part
        
        # Convert to int or float
        try:
            if has_decimal or has_exponent:
                value = float(num_str)
            else:
                value = int(num_str)
            if negative and int_part:
                value = -value
        except ValueError:
            raise ValueError(f"Invalid number: {num_str}")
        
        return Token(TokenType.NUMBER, value, start_line, start_column)
    
    def _read_string(self) -> Token:
        """Read a string literal."""
        start_line = self.line
        start_column = self.column
        self.pos += 1  # Skip opening quote
        
        result = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            
            if char == '"':
                self.pos += 1  # Skip closing quote
                return Token(TokenType.STRING, ''.join(result), start_line, start_column)
            
            if char == '\\' and self.pos + 1 < len(self.source):
                self.pos += 1
                escaped = self.source[self.pos]
                if escaped == 'n':
                    result.append('\n')
                elif escaped == 't':
                    result.append('\t')
                elif escaped == '"':
                    result.append('"')
                elif escaped == '\\':
                    result.append('\\')
                else:
                    result.append(escaped)
            else:
                result.append(char)
            
            self.pos += 1
        
        raise ValueError(f"unterminated string starting at line {start_line}")
    
    def _read_symbol(self) -> Token:
        """Read a symbol."""
        start_line = self.line
        start_column = self.column
        
        result = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isalnum() or char in '+-*/<>=_':
                result.append(char)
                self.pos += 1
            else:
                break
        
        return Token(TokenType.SYMBOL, ''.join(result), start_line, start_column)
