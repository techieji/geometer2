from language import Token, TokenType, ParseTree


class TestToken:
    def test_create_number_token(self):
        token = Token(TokenType.NUMBER, 42)
        assert token.kind == TokenType.NUMBER
        assert token.value == 42

    def test_create_string_token(self):
        token = Token(TokenType.STRING, "hello")
        assert token.kind == TokenType.STRING
        assert token.value == "hello"

    def test_create_atom_token(self):
        token = Token(TokenType.ATOM, "foo")
        assert token.kind == TokenType.ATOM
        assert token.value == "foo"

    def test_create_boolean_true(self):
        token = Token(TokenType.BOOLEAN, True)
        assert token.kind == TokenType.BOOLEAN
        assert token.value is True

    def test_create_boolean_false(self):
        token = Token(TokenType.BOOLEAN, False)
        assert token.kind == TokenType.BOOLEAN
        assert token.value is False

    def test_create_point_token(self):
        token = Token(TokenType.POINT, (1, 2))
        assert token.kind == TokenType.POINT
        assert token.value == (1, 2)

    def test_create_character_token(self):
        token = Token(TokenType.CHARACTER, 'a')
        assert token.kind == TokenType.CHARACTER
        assert token.value == 'a'

    def test_token_equality_same(self):
        t1 = Token(TokenType.NUMBER, 42)
        t2 = Token(TokenType.NUMBER, 42)
        assert t1 == t2

    def test_token_equality_different_value(self):
        t1 = Token(TokenType.NUMBER, 42)
        t2 = Token(TokenType.NUMBER, 43)
        assert t1 != t2

    def test_token_equality_different_type(self):
        t1 = Token(TokenType.NUMBER, 42)
        t2 = Token(TokenType.STRING, "42")
        assert t1 != t2


class TestParseTree:
    def test_create_literal_number(self):
        token = Token(TokenType.NUMBER, 42)
        tree = ParseTree(is_literal=True, value=token)
        assert tree.is_literal is True
        assert tree.value == token

    def test_create_literal_string(self):
        token = Token(TokenType.STRING, "hello")
        tree = ParseTree(is_literal=True, value=token)
        assert tree.is_literal is True
        assert tree.value == token

    def test_create_compound(self):
        child1 = ParseTree(is_literal=True, value=Token(TokenType.NUMBER, 1))
        child2 = ParseTree(is_literal=True, value=Token(TokenType.NUMBER, 2))
        tree = ParseTree(is_literal=False, value=[child1, child2])
        assert tree.is_literal is False
        assert len(tree.value) == 2

    def test_display_literal(self, capsys):
        token = Token(TokenType.NUMBER, 42)
        tree = ParseTree(is_literal=True, value=token)
        tree.display()
        captured = capsys.readouterr()
        assert "NUMBER" in captured.out

    def test_display_compound(self, capsys):
        child = ParseTree(is_literal=True, value=Token(TokenType.NUMBER, 1))
        tree = ParseTree(is_literal=False, value=[child])
        tree.display()
        captured = capsys.readouterr()
        assert "NUMBER" in captured.out
