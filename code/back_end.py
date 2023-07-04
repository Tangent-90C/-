from ply import lex, yacc
import regex
import sympy as sp


class algebra():
    def __init__(self, Debug=False):
        self.Debug = Debug
        # All tokens must be named in advance.
        self.tokens = ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'LPAREN', 'RPAREN', 'COMMA',
                       'VARIABLE', 'NUMBER', 'SPECIAL_NUMBER', 'FUNC', 'diy_FUNC', 'diy_FUNC_recursion')

        # Ignored characters
        self.t_ignore = ' \t'

        # Token matching rules are written as regexs
        self.t_PLUS = r'\+'
        self.t_MINUS = r'-'
        self.t_TIMES = r'(?<!\*)\*(?!\*)'
        self.t_DIVIDE = r'/'
        self.t_POWER = r'(?<!\*)\*\*(?!\*)|\^'
        self.t_LPAREN = r'\(|（'
        self.t_RPAREN = r'\)|）'
        self.t_COMMA = r',|，'

        # 优先级
        self.precedence = (
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE'),
            ('right', 'POWER'),
            ('nonassoc', 'UMINUS')
        )

        # 用于记录所有的变量名，方便后面的带入数字
        self.length_all_var = set()
        # 用于记录自定义的函数
        self.diy_func_dict = {}
        self.diy_FUNC_recursion_dict = {}

        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

    def __call__(self, s):
        s = self._filtter(s)
        ops = self.parser.parse(s, lexer=self.lexer)
        return ops

    def define_new_func(self, func_name, func, var_list):
        # func sympy的表达式
        # var_list 是个列表，里面是变量名
        # 找出var_list中不存在的变量
        var_list_exist = [i for i in var_list if i not in self.length_all_var]
        self.diy_func_dict[func_name] = (self(func), var_list)
        # 清理
        for i in var_list_exist:
            if i in self.length_all_var:
                self.length_all_var.remove(i)

    def define_new_套娃_func(self, func_name, var_list, express_list, domain_list):
        self.diy_FUNC_recursion_dict[func_name] = (func, var_list)
        var_list_exist = [i for i in var_list if i not in self.length_all_var]
        self.diy_func_dict[func_name] = (self(func), var_list)
        # 清理
        for i in var_list_exist:
            if i in self.length_all_var:
                self.length_all_var.remove(i)


    def return_all_var(self):
        return self.length_all_var

    def return_all_func(self):
        return self.diy_func_dict

    def clear_var(self):
        # 清空变量
        self.length_all_var = set()

    def clear_diy_func(self):
        # 清空自定义函数
        self.diy_func_dict = {}

    def t_FUNC(self, t):
        r'sin|cos|tan|cot|sec|csc|ln|log|sqrt|floor|abs'
        if t.value == 'abs':
            t.value = sp.Abs
        else:
            t.value = getattr(sp, t.value)
        return t

    def t_SPECIAL_NUMBER(self, t):
        r'pi|e'
        if t.value == 'pi':
            t.value = sp.pi
        elif t.value == 'e':
            t.value = sp.E
        elif t.value == 'i':
            t.value = sp.I
        return t

    def t_NUMBER(self, t):
        r'([1-9]\d*\.?\d*)|(0\.\d*[1-9])'
        t.value = sp.Rational(t.value)
        return t

    # t_VARIABLE必须在最底下，否则会盖住其他的匹配规则。
    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'

        if t.value in self.diy_func_dict.keys():
            # 这是一个自定义的函数，不是变量
            t.type = 'diy_FUNC'
            t.value = self.diy_func_dict[t.value]
            return t
        else:
            # 这是一个变量
            t.value = sp.Symbol(t.value)
            return t

    # Error handler for illegal characters
    def t_error(self, t):
        print(f'Illegal character {t.value[0]!r}')
        t.lexer.skip(1)

    def p_expr_all(self, p):
        """expr : NUMBER
                | SPECIAL_NUMBER"""
        p[0] = p[1]
        print(f'{p[1]} 转为了expr') if self.Debug else None

    def p_expr_var(self, p):
        'expr : VARIABLE'
        self.length_all_var.add(p[1].name)
        p[0] = p[1]
        print(f'变量 {p[0]} 从VARIABLE转化为expr') if self.Debug else None

    def p_expr2uminus(self, p):
        'expr : MINUS expr %prec UMINUS'
        p[0] = - p[2]

    # 函数调用处理，或括号处理
    def p_factor_func_no_paren(self, p):
        """expr : LPAREN expr RPAREN
                | FUNC LPAREN expr RPAREN
                | FUNC LPAREN expr COMMA expr RPAREN"""
        if len(p) == 4:
            print(f'将括号内的：{p[2]} 提取出来') if self.Debug else None
            p[0] = p[2]
        elif len(p) == 5:
            p[0] = p[1](p[3])
            print(f'函数调用：{p[1]} {p[2]} {p[3]} {p[4]}，得到{p[0]}') if self.Debug else None
        elif len(p) == 7:
            p[0] = p[1](p[3], p[5])
            print(f'函数调用：{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}, 得到{p[0]}') if self.Debug else None

    # diy函数调用处理，或括号处理
    def p_factor_diy_func_no_paren(self, p):
        """expr : diy_FUNC LPAREN expr RPAREN
                | diy_FUNC LPAREN expr COMMA expr RPAREN"""
        if len(p) == 5:
            p[0] = p[1][0].subs({f'{p[1][1][0]}': p[3]})
            print(f'函数调用：{p[1]} {p[2]} {p[3]} {p[4]}，得到{p[0]}') if self.Debug else None
        elif len(p) == 7:
            p[0] = p[1][0].subs({f'{p[1][1][0]}': p[3], f'{p[1][1][1]}': p[5]})
            print(f'函数调用：{p[1]} {p[2]} {p[3]} {p[4]} {p[5]} {p[6]}, 得到{p[0]}') if self.Debug else None

    # 乘方是优先度第1高的
    def p_term_power(self, p):
        """expr : expr POWER expr"""
        p[0] = p[1] ** p[3]
        print(f'乘方：{p[1]} {p[2]} {p[3]}，得到{p[0]}') if self.Debug else None

    # 乘法和除法是优先度第3高的
    def p_term_times(self, p):
        """expr : expr TIMES expr
                | expr DIVIDE expr"""
        if p[2] == '*':
            p[0] = p[1] * p[3]
            print(f'乘法：{p[1]} {p[2]} {p[3]}，得到{p[0]}') if self.Debug else None
        elif p[2] == '/':
            p[0] = p[1] / p[3]
            print(f'除法：{p[1]} {p[2]} {p[3]}，得到{p[0]}') if self.Debug else None

    # 加法和减法是优先度第4高的
    def p_expression_plus(self, p):
        """expr : expr PLUS expr
                | expr MINUS expr"""
        if p[2] == '+':
            p[0] = p[1] + p[3]
            print(f'加法：{p[1]} {p[2]} {p[3]}，得到{p[0]}') if self.Debug else None
        elif p[2] == '-':
            p[0] = p[1] - p[3]
            print(f'减法：{p[1]} {p[2]} {p[3]}，得到{p[0]}') if self.Debug else None

    def p_error(self, p):
        print("Syntax error in input!，{}".format(p))

    def _filtter(self, s):
        if regex.findall('[𝐀-𝚣]', s):
            buffer = ''
            for i in s:
                if regex.match('[𝐀-𝚣]', i):
                    ch = chr((ord(i) - ord('𝐀')) % 26 + ord('a'))
                    buffer = buffer + ch
                else:
                    buffer = buffer + i
            s = buffer

        s = s.replace('∗', '*')
        s = s.replace('−', '-')
        s = s.replace(r'∕', r'/')
        s = s.replace(r'∖', '\\')
        s = s.replace(r'∘', '*')
        s = s.replace(r'∙', '*')

        s = regex.sub(r'(?<=[0-9]+)\s*(?=[a-z\(])', '*', s)  # 补全数字与字母之间的乘号
        s = regex.sub(r'(?<=[a-z\)]+)\s+(?=[a-z])', '*', s)  # 补全字母与空格后函数之间的乘号
        s = regex.sub(r'\)\s*\(', ')*(', s)  # 补全括号之间的乘号
        s = regex.sub(r'(^\+)|((?<=\()\+)', '', s)  # 去掉开头的加号

        return s





if __name__ == '__main__':
    agb = algebra()
    question = '5 + 6 + x + 9 + sin(5 * x - y)'
    print(agb(question))
    question = 'a*sin(b*x+c^log(2,sin(a)))+abs(3+x)*cos(cos(b)+(b-4*ac))/(2*floor(x))-log(a,x)'
    print(agb(question))
    question = '𝑎 sin(𝑏 ∗ 𝑥 + 𝑐^2) + abs(3 + x) ∗ sec(𝑏 + (b − 4𝑎𝑐))/(2 ∗ 𝑓𝑙𝑜𝑜𝑟(𝑥)) − log(𝑎, 𝑥) ∗ ln(𝑥)'
    print(agb(question))
    question = 'log(log(log(𝑎, 𝑥), 𝑚), 𝑛) + sin(cos(sin(cos(x) + a ∗ b/(c ∗ d)) + b) + c)'
    print(agb(question))
