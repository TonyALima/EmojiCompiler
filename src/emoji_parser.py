import ply.lex as lex
import ply.yacc as yacc

from emoji_lex import EmojiLexer


class EmojiParser:
    # Precedência dos operadores
    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("left", "EQUAL", "NEQUAL"),
        ("left", "LT", "LTE", "GT", "GTE"),
        ("left", "PLUS", "MINUS"),
        ("left", "MULTIPLY", "DIVIDE", "MOD"),
        ("right", "NOT"),
        ("right", "UMINUS"),
    )
    # dictionary of names
    names = {}

    def __init__(self, lexer):
        self.yacc = yacc.yacc(module=self)

    def p_statement_expr(self, p):
        """statement : comando
        | type ..."""
        print(p[1])

    def p_comando(self, p):
        """comando : ASSIGN
        | IF
        | ELSE
        | WHILE
        | FOR
        | BREAK
        | CONTINUE
        | RETURN"""

    # Tipos de dados
    def p_type(self, p):
        """type : INT
        | FLOAT
        | CHAR
        | VOID"""
        p[0] = p[1]

    def p_operador(self, p):
        """operador : MULTIPLY
        | DIVIDE
        | MOD
        | PLUS
        | MINUS
        | EQUAL
        | NEQUAL
        | GT
        | LT
        | GTE
        | LTE
        | AND
        | OR
        """
        p[0] = p[1]

    def p_boolean(self, p):
        """boolean : TRUE
        | FALSE"""
        p[0] = p[1]

    def p_nome(self, p):
        """NOME"""

    def p_valor(self, p):
        pass

    def p_operation_binop(self, p):
        """
        operation : valor operador valor
        """
        if p[2] == "+":
            p[0] = p[1] + p[3]
        elif p[2] == "-":
            p[0] = p[1] - p[3]
        elif p[2] == "*":
            p[0] = p[1] * p[3]
        elif p[2] == "/":
            p[0] = p[1] / p[3]

    def p_assign(self, p):
        """assign: NOME valor"""
        if (self.names.get(p[1])):
            if (type(self.names[p[1]]) == type(p[2])):
                self.names[p[1]] = p[2]
    
    def p_declare(self, p):
        """declare: type NOME valor"""
        if ():
            self.names[p[2]]

    # Declaração de variáveis
    def p_declaration(self, p):
        """declaration : type NOME ASSIGN expression SEMICOLON
        | type NOME SEMICOLON"""
        if len(p) == 6:
            p[0] = ("assign", p[2], p[4])
        else:
            p[0] = ("declare", p[1], p[2])

    # Atribuição
    def p_assignment(self, p):
        """assignment : NOME ASSIGN expression SEMICOLON"""
        p[0] = ("assign", p[1], p[3])

    def p_parentheses(self, p):
        """parentheses: LPAREN valor RPAREN"""
        p[0] = p[2]

    # Bloco de código
    def p_bloco(self, p):
        """bloco : LBRACE comando RBRACE
        | LBRACE RBRACE"""
        if len(p) == 4:
            p[0] = [2]

    # Condicional
    def p_if_statement(self, p):
        """if_statement : IF LPAREN expression RPAREN LBRACE block RBRACE
        | IF LPAREN expression RPAREN LBRACE block RBRACE ELSE LBRACE block RBRACE"""
        if len(p) == 8:
            p[0] = ("if", p[3], p[6])
        else:
            p[0] = ("ifelse", p[3], p[6], p[10])

    # Loop while
    def p_while_statement(self, p):
        """while_statement : WHILE LPAREN expression RPAREN LBRACE block RBRACE"""
        p[0] = ("while", p[3], p[6])

    # Loop for
    def p_for_statement(self, p):
        """for_statement : FOR LPAREN declaration SEMICOLON expression SEMICOLON assignment RPAREN LBRACE block RBRACE"""
        p[0] = ("for", p[3], p[5], p[7], p[10])

    # Leitura de entrada
    def p_scanf_statement(self, p):
        """scanf_statement : SCANF LPAREN NOME RPAREN SEMICOLON"""
        p[0] = ("scanf", p[3])

    # Impressão
    def p_printf_statement(self, p):
        """printf_statement : PRINTF LPAREN expression RPAREN SEMICOLON"""
        p[0] = ("printf", p[3])

    # Interrupção de loop
    def p_break_statement(self, p):
        """break_statement : BREAK SEMICOLON"""
        p[0] = ("break",)

    # Continuação de loop
    def p_continue_statement(self, p):
        """continue_statement : CONTINUE SEMICOLON"""
        p[0] = ("continue",)

    # Retorno de valor
    def p_return_statement(self, p):
        """return_statement : RETURN expression SEMICOLON"""
        p[0] = ("return", p[2])

    # Erro de sintaxe
    def p_error(self, p):
        print(f"Erro de sintaxe em {p.value}")


def main() -> None:
    lexer = EmojiLexer()

    codigo = """
        ℹ x🟰5❣
        👨
        👉
            🖨🤜x🤛❣
        👈
        """

    # Give the lexer some input
    lexer.test(codigo)

    
    parser = EmojiParser()
    result = parser.yacc.parse(codigo, lexer=lexer.lexer)
    print(result)


if __name__ == "__main__":
    main()
