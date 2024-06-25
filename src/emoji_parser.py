import ply.lex as lex
import ply.yacc as yacc
from ply.yacc import Production

from src.emoji_lex import EmojiLexer


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
    variables: dict = {}

    types: dict = {
        "ℹ️": int,
        "☁": float,
        "🐃": bool,
        "🥚": None,
    }

    operations: dict = {
        "🟰": "=",
        "➕": "+",
        "➖": "-",
        "✖": "*",
        "➗": "/",
        "❗": "!",
        "🤏": "<",
        "🤏🟰": "<=",
        "🙌": ">",
        "🙌🟰": ">=",
        "🟰🟰": "==",
        "💩": "%",
    }

    def __init__(self):
        self.lexer = EmojiLexer()
        self.parser = yacc.yacc(module=self, debug=True)
        self.current_type_declaration = None
        self.commands = []

    def parse(self, data):
        print("/" + 10 * "-" + "Analise Sintatica" + 10 * "-" + "/")

        return self.parser.parse(data, lexer=self.lexer.lexer)

    def p_program(self, p: Production) -> None:
        """program : INT MAIN LPAREN RPAREN bloco"""
        p[0] = {"MAIN": p[5]}

    def p_sinal(self, p: Production) -> None:
        """sinal : NOT PLUS
        | NOT MINUS
        | NOT
        | PLUS
        | MINUS"""
        p[0] = p[1]

    def p_comando(self, p: Production) -> None:
        """comando : declaration
        | assignment
        | if_statement
        | while_statement
        | for_statement
        | bloco
        | break_statement
        | continue_statement
        | return_statement
        | printf_statement
        | scanf_statement"""
        p[0] = p[1]

    def p_comandos(self, p: Production) -> None:
        """comandos : comando comandos
        | comando"""
        if len(p) == 3:
            p[0] = [{"COMANDO": p[1]}] + p[2]
        elif len(p) == 2:
            p[0] = [{"COMANDO": p[1]}]

    def p_bloco(self, p: Production) -> None:
        """bloco : LBRACE comandos RBRACE
        | LBRACE RBRACE"""
        if len(p) == 4:
            p[0] = {"BLOCO": p[2]}
        else:
            p[0] = {"BLOCO": []}

    def p_parentheses(self, p: Production) -> None:
        """parentheses : LPAREN valor RPAREN"""
        p[0] = p[2]

    def p_type(self, p: Production) -> None:
        """type : INT
        | FLOAT
        | CHAR
        | VOID
        | BOOL"""
        t: type = self.types.get(p[1], None)
        self.current_type_declaration = t
        p[0] = t

    def p_operador(self, p: Production) -> None:
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
        p[0] = self.operations.get(p[1])

    def p_boolean(self, p: Production) -> None:
        """boolean : TRUE
        | FALSE"""
        p[0] = p[1]

    def p_valor(self, p: Production) -> None:
        """valor : NUMBER
        | NOME
        | CHARACTER
        | boolean
        | operation
        | parentheses"""
        p[0] = p[1]

    def p_operation(self, p: Production) -> None:
        """
        operation : valor operador valor
        """
        p[0] = {"OPERAÇÃO": {"valor1": p[1], "op": p[2], "valor2": p[3]}}

    def p_assignment(self, p: Production) -> None:
        """assignment : NOME ASSIGN valor"""
        p[0] = {"ATRIBUIÇÃO": {"nome": p[1], "valor": p[3]}}

    def p_declaration_list(self, p: Production) -> None:
        """declaration_list : NOME
        | NOME declaration_list
        | NOME ASSIGN valor
        | NOME ASSIGN valor COMMA declaration_list"""
        l = len(p)
        tn: type = self.current_type_declaration.__name__
        if l == 2:
            p[0] = [
                {
                    "nome": p[1],
                    "type": tn,
                    "valor": self.current_type_declaration(),
                }
            ]
        elif l == 3:
            p[0] = [
                {
                    "nome": p[1],
                    "type": tn,
                    "valor": self.current_type_declaration(),
                }
            ] + p[2]
        elif l == 4:
            p[0] = [
                {
                    "nome": p[1],
                    "type": tn,
                    "valor": p[3],
                }
            ]
        else:
            p[0] = [
                {
                    "nome": p[1],
                    "type": tn,
                    "valor": p[3],
                }
            ] + p[5]

    def p_declaration(self, p: Production) -> None:
        """declaration : type declaration_list SEMICOLON"""
        p[0] = {"DECLARAÇÃO": [p[2]]}

    def p_if_statement(self, p: Production) -> None:
        """if_statement : IF LPAREN valor RPAREN bloco"""
        p[0] = {"if": {"valor": p[3], "bloco": p[5]}}

    def p_while_statement(self, p: Production) -> None:
        """while_statement : WHILE LPAREN valor RPAREN bloco"""
        p[0] = {"while": {"valor": p[3], "bloco": p[6]}}

    def p_for_statement(self, p: Production) -> None:
        """for_statement : FOR LPAREN for_init SEMICOLON for_condition SEMICOLON for_update RPAREN comando"""
        p[0] = {
            "for": {"init": p[3], "condition": p[5], "update": p[7], "comando": p[9]}
        }

    def p_for_init(self, p: Production) -> None:
        """for_init : assignment
        | declaration
        | valor
        | empty
        | assignment for_comma
        | valor for_comma
        | declaration for_comma
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]

    def p_for_comma(self, p: Production) -> None:
        """for_comma : COMMA assignment
        | COMMA valor SEMICOLON
        | COMMA assignment for_comma"""
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = (p[2], p[3])

    def p_for_condition(self, p: Production) -> None:
        """for_condition : assignment
        | valor
        | valor for_comma
        | assignment for_comma
        | empty"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]

    def p_for_update(self, p: Production) -> None:
        """for_update : assignment
        | valor
        | valor for_comma
        | assignment for_comma
        | empty"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[2]

    # Leitura de entrada
    def p_scanf_statement(self, p: Production) -> None:
        """scanf_statement : SCANF LPAREN NOME RPAREN SEMICOLON"""
        p[0] = {"scanf": {"nome": p[3]}}

    # Impressão
    def p_printf_statement(self, p: Production) -> None:
        """printf_statement : PRINTF LPAREN valor RPAREN SEMICOLON"""
        p[0] = {"printf": {"valor": p[3]}}

    # Interrupção de loop
    def p_break_statement(self, p: Production) -> None:
        """break_statement : BREAK SEMICOLON"""
        p[0] = p[1]

    # Continuação de loop
    def p_continue_statement(self, p: Production) -> None:
        """continue_statement : CONTINUE SEMICOLON"""
        p[0] = p[1]

    # Retorno de valor
    def p_return_statement(self, p: Production) -> None:
        """return_statement : RETURN valor SEMICOLON"""
        p[0] = {"return": {"valor": p[2]}}

    def p_empty(self, p: Production) -> None:
        "empty :"
        pass

    def p_error(self, p: Production) -> None:
        print(f"Erro de sintaxe em {p.value}")
