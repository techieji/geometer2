import re
from language import TokenType, Token, ParseTree

def lex(program):
    program = program.strip()
    i = 0
    n = len(program)

    while i < n:
        c = program[i]

        if c.isspace():
            i += 1
        elif c == ';':
            while i < n and program[i] != '\n':
                i += 1
        elif c == '"':
            j = i + 1
            while j < n and program[j] != '"':
                if program[j] == '\\':
                    j += 2
                else:
                    j += 1
            yield Token(TokenType.STRING, program[i+1:j])
            i = j + 1
        elif c == "'" and i + 1 < n and program[i+1] == '(':
            j = i + 2
            while j < n and program[j] != ')':
                j += 1
            if ',' in program[i+1:j]:
                yield Token(TokenType.POINT, program[i+1:j+1])
            else:
                yield Token(TokenType.CHARACTER, "'")
                i += 1
                continue
            i = j + 1
        elif c == '#':
            if i + 1 < n and program[i+1] in 'tf':
                yield Token(TokenType.BOOLEAN, program[i+1] == 't')
                i += 2
        elif c.isdigit() or (c == '-' and i + 1 < n and program[i+1].isdigit()):
            j = i + 1
            while j < n and (program[j].isdigit() or program[j] == '.'):
                j += 1
            yield Token(TokenType.NUMBER, float(program[i:j]) if '.' in program[i:j] else int(program[i:j]))
            i = j
        elif c in "()'`,":
            yield Token(TokenType.CHARACTER, c)
            i += 1
        else:
            j = i
            while j < n and not program[j].isspace() and program[j] not in "()\"';`,":
                j += 1
            atom = program[i:j]
            if atom in ('true', 'false'):
                yield Token(TokenType.BOOLEAN, atom == 'true')
            else:
                yield Token(TokenType.ATOM, atom)
            i = j

if __name__ == '__main__':
    try:
        while True:
            print('\n'.join(map(str, lex(input()))))
    except EOFError:
        print('Exiting')
