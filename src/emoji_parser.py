import ply.lex as lex
import ply.yacc as yacc

from emoji_lex import EmojiLexer


class EmojiParser:
    tokens = EmojiLexer.tokens

    # Precedência dos operadores
    precedence = (
        ("left", "OR"),
        ("left", "AND"),
        ("left", "EQUAL", "NEQUAL"),
        ("left", "LT", "LTE", "GT", "GTE"),
        ("left", "PLUS", "MINUS"),
        ("left", "MULTIPLY", "DIV", "MOD"),
        ("right", "NOT"),
    )
    # dictionary of names
    names = {}

    def __init__(self):
        self.lexer = EmojiLexer(debug=True)
        self.parser = yacc.yacc(module=self, debug=True)
        self.comandos = []

    def parse(self, data):
        result = self.parser.parse(data, lexer=self.lexer.lexer)
        print(result)

    def p_program(self, p):
        """program : INT MAIN LPAREN RPAREN bloco"""
        print("Programa identificado")
        p[0] = p[5]

    def p_comando(self, p):
        """comando : declaration
        | if_statement
        | while_statement
        | for_statement
        | break_statement
        | continue_statement
        | return_statement"""
        print("Comando identificado: ", p[1])
        p[0] = p[1]

    def p_type(self, p):
        """type : INT
        | FLOAT
        | CHAR
        | VOID
        | BOOL"""
        print("Tipo identificado: ", p[1])
        p[0] = p[1]

    def p_operador(self, p):
        """operador : MULTIPLY
        | DIV
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

    def p_valor(self, p):
        """valor : NUMBER
        | CHARACTER
        | boolean
        | operation
        | parentheses"""
        p[0] = p[1]

    def p_operation(self, p):
        """
        operation : valor operador valor
        """

    def p_assignment(self, p):
        """assignment : NOME valor"""
        if self.names.get(p[1]):
            if type(self.names[p[1]]) == type(p[2]):
                self.names[p[1]] = p[2]

    def p_declare(self, p):
        """declare : type NOME valor"""
        self.names[p[2]]

    # Declaração de variáveis
    def p_declaration(self, p):
        """declaration : type NOME ASSIGN valor SEMICOLON
        | type NOME SEMICOLON"""
        if len(p) == 6:
            p[0] = ("assignment", p[2], p[4])
        elif len(p) == 7:
            p[0] = ("declare", p[1], p[2])

    def p_parentheses(self, p):
        """parentheses : LPAREN valor RPAREN"""
        p[0] = p[2]

    # Bloco de código
    def p_bloco(self, p):
        """bloco : LBRACE comando RBRACE
        | LBRACE RBRACE"""
        if len(p) == 4:
            p[0] = [2]

    # Condicional
    def p_if_statement(self, p):
        """if_statement : IF LPAREN valor RPAREN LBRACE bloco RBRACE"""
        p[0] = ("if", p[3], p[6])

    # Loop while
    def p_while_statement(self, p):
        """while_statement : WHILE LPAREN valor RPAREN LBRACE bloco RBRACE"""
        p[0] = ("while", p[3], p[6])

    def p_for_statement(self, p):
        """for_statement : FOR LPAREN assignment_or_declaration_or_value SEMICOLON assignment_or_value SEMICOLON assignment_or_value RPAREN comando"""
        p[0] = ("for", p[3], p[5], p[7], p[9])

    def p_assignment_or_declaration_or_value(self, p):
        """assignment_or_declaration_or_value : assignment
        | declaration
        | valor"""
        p[0] = p[1]

    def p_assignment_or_value(self, p):
        """assignment_or_value : assignment
        | valor"""
        p[0] = p[1]

    # Leitura de entrada
    def p_scanf_statement(self, p):
        """scanf_statement : SCANF LPAREN NOME RPAREN SEMICOLON"""
        p[0] = ("scanf", p[3])

    # Impressão
    def p_printf_statement(self, p):
        """printf_statement : PRINTF LPAREN valor RPAREN SEMICOLON"""
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
        """return_statement : RETURN valor SEMICOLON"""
        p[0] = ("return", p[2])

    # Erro de sintaxe
    def p_error(self, p):
        print(f"Erro de sintaxe em {p.value}")


def main() -> None:
    parser = EmojiParser()

    codigo = "ℹ️👨🤜🤛👉☁x🟰5💥1❣👈"

    # Give the lexer some input
    parser.parse(codigo)


if __name__ == "__main__":
    main()
