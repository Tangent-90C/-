from ply import lex, yacc
import regex
import sympy as sp


class Domain():
    def __init__(self, debug=False):
        self.debug = debug
        self.tokens = (
        'opencurly', 'open_bracket', 'open_paren', 'close_paren', 'close_bracket', 'close_curly', 'comma', 'and', 'or', 'not', 'all', 'integer', 'p_integers', 'natural_number' ,'NUMBER')

        # Ignored characters
        self.t_ignore = ' \t'

        # Token matching rules are written as regexs
        self.t_opencurly = r'\{'
        self.t_open_bracket = r'\['
        self.t_open_paren = r'\('
        self.t_close_paren = r'\)'
        self.t_close_bracket = r'\]'
        self.t_close_curly = r'\}'
        self.t_and = r'\&'
        self.t_or = r'\|'
        self.t_not = r'\~'
        self.t_comma = r','
        self.t_all = r'U'
        self.t_integer = r'Z'
        self.t_p_integers = r'N'
        self.t_natural_number = r'N0'

        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)


    def __call__(self, s):
        the_set = self.parser.parse(s, lexer=self.lexer, debug=self.debug)
        return the_set

    def t_NUMBER(self, t):
        r'(\-?[1-9]\d*\.?\d*)|(\-?0\.\d*[1-9])'
        t.value = sp.Rational(t.value)
        return t

    def t_error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        print('定义域解析器出错')
        t.lexer.skip(1)


    def p_expr_NUMBER(self, p):
        """expr : NUMBER"""
        p[0] = p[1]

    def p_leftbrack_change(self, p):
        """leftbracket : open_bracket
                        | open_paren
                        | opencurly"""
        p[0] = p[1]

    def p_rightbrack_change(self, p):
        """rightbracket : close_paren
                        | close_bracket
                        | close_curly"""
        p[0] = p[1]

    def p_MUL_first(self, p):
        """MUL : expr"""
        p[0] = [p[1]]

    def p_MUL_sec(self, p):
        """MUL : MUL comma expr"""
        p[0] = p[1] + [p[3]]


    def p_expr(self, p):
        """expr : leftbracket MUL rightbracket
                | leftbracket rightbracket"""
        if len(p) == 3:
            # 空集
            p[0] = sp.EmptySet()
        elif len(p) == 4:
            if p[1] in ['(', '['] and p[3] in [')', ']']:
                if len(p[2]) == 2:
                    p[0] = sp.Interval(p[2][0], p[2][1], True if p[1] == '(' else False, True if p[3] == ')' else False)
                else:
                    raise Exception('Syntax error in input!')
            elif p[1] in ['{', '}'] and p[3] in ['{', '}']:
                p[0] = sp.FiniteSet(*p[2])
            else:
                raise Exception('Syntax error in input!')

    def p_expr_and(self, p):
        """expr : expr and expr"""
        p[0] = p[1] & p[3]

    def p_expr_or(self, p):
        """expr : expr or expr"""
        p[0] = p[1] | p[3]

    def p_expr_not(self, p):
        """expr : not expr"""
        p[0] = sp.sets.UniversalSet - p[2]



    def p_error(self, p):
        print("Syntax error in input!，{}".format(p))


