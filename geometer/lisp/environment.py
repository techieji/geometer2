"""Environment module for Geometer Lisp interpreter.

This module provides the Environment class for managing variable bindings
and scopes in the Lisp interpreter.
"""

from typing import Any, Dict, Optional, List


class Environment:
    """Manages variable bindings and scopes.
    
    Supports nested scopes through parent environment references.
    """
    
    def __init__(
        self,
        parent: Optional['Environment'] = None,
        bindings: Optional[Dict[str, Any]] = None
    ):
        """Initialize an environment.
        
        Args:
            parent: Optional parent environment for nested scopes.
            bindings: Optional initial bindings dict.
        """
        self._parent = parent
        self._bindings: Dict[str, Any] = bindings.copy() if bindings else {}
    
    @property
    def parent(self) -> Optional['Environment']:
        """Get the parent environment."""
        return self._parent
    
    def define(self, symbol: str, value: Any) -> None:
        """Define a new variable in the current scope.
        
        Args:
            symbol: Variable name.
            value: Value to bind.
            
        Raises:
            ValueError: If the symbol is already defined in the current scope.
        """
        if symbol in self._bindings:
            raise ValueError(f"Variable '{symbol}' is already defined in this scope")
        self._bindings[symbol] = value
    
    def define_global(self, symbol: str, value: Any) -> None:
        """Define a variable in the global (root) scope.
        
        Args:
            symbol: Variable name.
            value: Value to bind.
        """
        if self._parent is None:
            # This is the global scope
            self._bindings[symbol] = value
        else:
            # Traverse to root
            env = self
            while env._parent is not None:
                env = env._parent
            env._bindings[symbol] = value
    
    def lookup(self, symbol: str) -> Any:
        """Look up a variable in the current or parent scopes.
        
        Args:
            symbol: Variable name to look up.
            
        Returns:
            The bound value.
            
        Raises:
            NameError: If the symbol is not found in any scope.
        """
        if symbol in self._bindings:
            return self._bindings[symbol]
        
        if self._parent is not None:
            return self._parent.lookup(symbol)
        
        raise NameError(f"Undefined variable: '{symbol}'")
    
    def set(self, symbol: str, value: Any) -> bool:
        """Set an existing variable in the current or parent scopes.
        
        Args:
            symbol: Variable name.
            value: New value.
            
        Returns:
            True if the variable was found and set, False otherwise.
        """
        if symbol in self._bindings:
            self._bindings[symbol] = value
            return True
        
        if self._parent is not None:
            return self._parent.set(symbol, value)
        
        return False
    
    def set_local(self, symbol: str, value: Any) -> bool:
        """Set a variable in the current scope only (does not affect parents).
        
        Args:
            symbol: Variable name.
            value: New value.
            
        Returns:
            True if the variable was found in current scope, False otherwise.
        """
        if symbol in self._bindings:
            self._bindings[symbol] = value
            return True
        return False
    
    def is_defined(self, symbol: str) -> bool:
        """Check if a variable is defined in any scope.
        
        Args:
            symbol: Variable name.
            
        Returns:
            True if defined, False otherwise.
        """
        if symbol in self._bindings:
            return True
        if self._parent is not None:
            return self._parent.is_defined(symbol)
        return False
    
    def is_defined_local(self, symbol: str) -> bool:
        """Check if a variable is defined in the current scope only.
        
        Args:
            symbol: Variable name.
            
        Returns:
            True if defined in current scope, False otherwise.
        """
        return symbol in self._bindings
    
    def extend(self) -> 'Environment':
        """Create a new environment that extends this one.
        
        Returns:
            New child environment with this as parent.
        """
        return Environment(parent=self)
    
    def get_local_bindings(self) -> Dict[str, Any]:
        """Get all bindings in the current scope.
        
        Returns:
            Copy of the current scope's bindings.
        """
        return self._bindings.copy()
    
    def __repr__(self) -> str:
        return f"Environment({self._bindings}, parent={self._parent is not None})"


# Global environment singleton
_global_env: Optional[Environment] = None


def get_global_environment() -> Environment:
    """Get the global environment, creating it if necessary.
    
    Returns:
        The global Environment instance.
    """
    global _global_env
    if _global_env is None:
        _global_env = Environment()
    return _global_env


def reset_global_environment() -> Environment:
    """Reset the global environment to a fresh state.
    
    Returns:
        New empty global Environment.
    """
    global _global_env
    _global_env = Environment()
    return _global_env


def create_child_environment(parent: Optional[Environment] = None) -> Environment:
    """Create a child environment.
    
    Args:
        parent: Parent environment (defaults to global if not provided).
        
    Returns:
        New child Environment.
    """
    if parent is None:
        parent = get_global_environment()
    return parent.extend()
