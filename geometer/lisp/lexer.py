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
    
    # Regex patterns for tokenization
    PATTERNS = [
        (r';[^\n]*', None),  # Comments - skip
        (r'\s+', None),      # Whitespace - skip
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
        (r"'[^()'\"]+", TokenType.QUOTE),  # Quote shorthand
        (r"'(?=\()", TokenType.QUOTE),  # Quote followed by paren
        (r"'(?=[0-9+-])", TokenType.QUOTE),  # Quote followed by number
        (r'-?\d+\.?\d*(?:[eE][+-]?\d+)?', TokenType.NUMBER),
        (r'"(?:[^"\\]|\\.)*"', TokenType.STRING),
        (r"'(?P<x>-?\d+\.?\d*)\s*,\s*(?P<y>-?\d+\.?\d*)\)", TokenType.POINT),
        (r'[a-zA-Z+/<>=_][a-zA-Z0-9+/<>=_-]*', TokenType.SYMBOL),
    ]
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
    
    def tokenize(self) -> List[Token]:
        """Generate tokens from the source code."""
        tokens = []
        
        while self.pos < len(self.source):
            matched = False
            
            # Try each pattern
            for pattern, token_type in self.PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)
                
                if match:
                    text = match.group(0)
                    
                    # Skip whitespace and comments
                    if token_type is None:
                        self._advance(text)
                        matched = True
                        break
                    
                    # Process the matched token
                    value = self._process_value(text, token_type)
                    token = Token(token_type, value, self.line, self.column)
                    tokens.append(token)
                    
                    self._advance(text)
                    matched = True
                    break
            
            if not matched:
                raise ValueError(
                    f"Unexpected character '{self.source[self.pos]}' "
                    f"at line {self.line}, column {self.column}"
                )
        
        # Add EOF token
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens
    
    def _advance(self, text: str) -> None:
        """Advance position after matching text."""
        for char in text:
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        self.pos += len(text)
    
    def _process_value(
        self, 
        text: str, 
        token_type: TokenType
    ) -> Union[str, int, float, Tuple[float, float]]:
        """Process the matched text into a token value."""
        if token_type == TokenType.NUMBER:
            # Try integer first, then float
            try:
                return int(text)
            except ValueError:
                return float(text)
        
        elif token_type == TokenType.STRING:
            # Remove quotes and handle escapes
            return text[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        
        elif token_type == TokenType.POINT:
            # Parse point syntax: '(<x>,<y>)
            match = re.match(r"'(?P<x>-?\d+\.?\d*)\s*,\s*(?P<y>-?\d+\.?\d*)\)", text)
            if match:
                x = float(match.group('x'))
                y = float(match.group('y'))
                # Convert to int if whole numbers
                if x.is_integer() and y.is_integer():
                    return (int(x), y)
                return (x, y)
            raise ValueError(f"Invalid point syntax: {text}")
        
        elif token_type == TokenType.QUOTE:
            # Return the quote marker, actual quote handling done by parser
            return text
        
        else:
            return text
