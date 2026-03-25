from collections import ChainMap
from execute import execute, pprint_result

if __name__ == '__main__':
    from lexer import lex
    from parser import parse
    env = ChainMap({})
    try:
        while True:
            pprint_result(execute(parse(lex(input())), env))
    except EOFError:
        print('Exiting')
