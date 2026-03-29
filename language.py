from enum import Enum
from typing import Any, Callable
from dataclasses import dataclass
from collections import ChainMap

class TokenType(Enum):
    NUMBER = 0
    STRING = 1
    ATOM = 2
    BOOLEAN = 3
    POINT = 4
    CHARACTER = 5        # represents parentheses, quotes, unquote, quasiquotes, etc.

@dataclass
class Token:
    kind: TokenType
    value: Any

type EvalResult = list[EvalResult] | int | float | bool | str | tuple[float, float] | Callable[[list[EvalResult]], EvalResult]

@dataclass
class ParseTree:
    is_literal: bool
    value: Token | list['ParseTree']

    def display(self):       # pretty-prints the tree using box-drawing characters                                                                                                                                                                         
        def _show(node, prefix="", is_last=True):                                                                                                                                                                                                          
            connector = "└── " if is_last else "├── "                                                                                                                                                                                                      
            if node.is_literal:                                                                                                                                                                                                                            
                token = node.value                                                                                                                                                                                                                         
                if token.kind == TokenType.POINT:                                                                                                                                                                                                          
                    print(f"{prefix}{connector}POINT {token.value}")                                                                                                                                                                                       
                elif token.kind == TokenType.STRING:                                                                                                                                                                                                       
                    print(f"{prefix}{connector}STRING \"{token.value}\"")                                                                                                                                                                                  
                elif token.kind == TokenType.NUMBER:                                                                                                                                                                                                       
                    print(f"{prefix}{connector}NUMBER {token.value}")                                                                                                                                                                                      
                elif token.kind == TokenType.ATOM:                                                                                                                                                                                                         
                    print(f"{prefix}{connector}ATOM {token.value}")                                                                                                                                                                                        
                elif token.kind == TokenType.BOOLEAN:                                                                                                                                                                                                      
                    print(f"{prefix}{connector}BOOLEAN {token.value}")                                                                                                                                                                                     
                elif token.kind == TokenType.CHARACTER:                                                                                                                                                                                                    
                    print(f"{prefix}{connector}CHAR {token.value}")                                                                                                                                                                                        
            else:                                                                                                                                                                                                                                          
                print(f"{prefix}{connector}LIST")                                                                                                                                                                                                          
                children = node.value                                                                                                                                                                                                                      
                for i, child in enumerate(children):                                                                                                                                                                                                       
                    extension = "    " if is_last else "│   "                                                                                                                                                                                              
                    _show(child, prefix + extension, i == len(children) - 1)                                                                                                                                                                               
        _show(self)                                                                   

type Environment = ChainMap
