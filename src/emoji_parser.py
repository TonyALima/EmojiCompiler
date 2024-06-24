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
    }

    def __init__(self):
        self.lexer = EmojiLexer()
        self.parser = yacc.yacc(module=self, debug=True)
        self.current_type_declaration = None
        self.commands = []

    def parse(self, data):
        print("/" + 10 * "-" + "Analise Sintatica" + 10 * "-" + "/")
        print(self.variables)

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
        | break_statement
        | continue_statement
        | return_statement"""
        p[0] = p[1]

    def p_comandos(self, p: Production) -> None:
        """comandos : comando comandos
        | comando"""
        if len(p) == 3:
            p[0] = [{"COMANDO": p[1]}] + p[2]
            self.commands.append([p[1]] + [p[2]])
        elif len(p) == 2:
            p[0] = [{"COMANDO": p[1]}]
            self.commands.append(p[1])

    def p_bloco(self, p: Production) -> None:
        """bloco : LBRACE comandos RBRACE
        | LBRACE RBRACE"""
        if len(p) == 4:
            self.commands.append({"bloco": p[2]})
        else:
            self.commands.append({"bloco": []})
        p[0] = {"BLOCO": p[2]}

    def p_parentheses(self, p: Production) -> None:
        """parentheses : LPAREN valor RPAREN"""
        p[0] = p[2]

    def p_type(self, p: Production) -> None:
        """type : INT
        | FLOAT
        | CHAR
        | VOID
        | BOOL"""
        t = self.types.get(p[1], None)
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
        self.commands.append(
            [{"operation": {"valor1": p[1], "op": p[2], "valor2": p[3]}}]
        )

    def assignment(self, nome: str, val=None) -> None:
        if self.variables.get(nome):
            if type(self.variables[nome]) == type(val):
                self.variables[nome] = val

    def p_assignment(self, p: Production) -> None:
        """assignment : NOME ASSIGN valor SEMICOLON"""
        p[0] = {"ATRIBUIÇÃO": {"nome": p[1], "valor": p[3]}}
        self.commands.append([{"assignment": {"nome": p[1], "valor": p[3]}}])
        self.assignment(p[1], p[3])

    def declare(self, tipo, nome: str, val=None) -> None:
        try:
            self.variables[nome] = self.current_type_declaration(val)
        except Exception as e:
            print(e)

    def p_declaration_list(self, p: Production) -> None:
        """declaration_list : NOME
        | NOME declaration_list
        | NOME ASSIGN valor
        | NOME ASSIGN valor COMMA declaration_list"""
        l = len(p)
        if l == 2:
            self.declare(
                self.current_type_declaration, p[1], self.current_type_declaration()
            )
            p[0] = [
                {
                    "nome": p[1],
                    "type": self.current_type_declaration,
                    "valor": self.current_type_declaration(),
                }
            ]
            self.commands.append(
                [
                    {
                        "declaration": {
                            "nome": p[1],
                            "type": self.current_type_declaration,
                            "valor": self.current_type_declaration(),
                        }
                    }
                ]
            )
        elif l == 3:
            self.declare(
                self.current_type_declaration, p[1], self.current_type_declaration()
            )
            p[0] = [
                {
                    "nome": p[1],
                    "type": self.current_type_declaration,
                    "valor": self.current_type_declaration(),
                }
            ] + p[2]
            self.commands.append(
                [
                    {
                        "declaration": {
                            "nome": p[1],
                            "type": self.current_type_declaration,
                            "valor": self.current_type_declaration(),
                        }
                    }
                ]
            )
        elif l == 4:
            self.declare(self.current_type_declaration, p[1], p[3])
            p[0] = [
                {
                    "nome": p[1],
                    "type": self.current_type_declaration,
                    "valor": p[3],
                }
            ]
            self.commands.append(
                [
                    {
                        "declaration": {
                            "nome": p[1],
                            "type": self.current_type_declaration,
                            "valor": p[3],
                        }
                    }
                ]
            )
        else:
            self.declare(self.current_type_declaration, p[1], p[3])
            p[0] = [
                {
                    "nome": p[1],
                    "type": self.current_type_declaration,
                    "valor": p[3],
                }
            ] + p[5]
            self.commands.append(
                [
                    {
                        "declaration": {
                            "nome": p[1],
                            "type": self.current_type_declaration,
                            "valor": p[3],
                        }
                    }
                ]
            )

    def p_declaration(self, p: Production) -> None:
        """declaration : type declaration_list SEMICOLON"""
        p[0] = {"DECLARAÇÃO": [p[2]]}

    def p_if_statement(self, p: Production) -> None:
        """if_statement : IF LPAREN valor RPAREN LBRACE bloco RBRACE"""
        print("Condicional identificado")
        p[0] = [{"if_statement": {"valor": p[3], "bloco": p[6]}}]

    def p_while_statement(self, p: Production) -> None:
        """while_statement : WHILE LPAREN valor RPAREN LBRACE bloco RBRACE"""
        print("Loop while identificado")
        p[0] = ("while", p[3], p[6])

    def p_for_statement(self, p: Production) -> None:
        """for_statement : FOR LPAREN for_init SEMICOLON for_condition SEMICOLON for_update RPAREN comando"""
        print("Loop for identificado")
        p[0] = ("for", p[3], p[5], p[7], p[9])

    def p_for_init(self, p: Production) -> None:
        """for_init : assignment
        | declaration
        | valor
        | empty
        | assignment for_comma
        | valor for_comma
        | declaration for_comma
        """
        print("Inicialização de loop identificada")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])

    def p_for_comma(self, p: Production) -> None:
        """for_comma : COMMA assignment
        | COMMA valor
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
            p[0] = (p[1], p[2])

    def p_for_update(self, p: Production) -> None:
        """for_update : assignment
        | valor
        | valor for_comma
        | assignment for_comma
        | empty"""
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])

    # Leitura de entrada
    def p_scanf_statement(self, p: Production) -> None:
        """scanf_statement : SCANF LPAREN NOME RPAREN SEMICOLON"""
        p[0] = ("scanf", p[3])

    # Impressão
    def p_printf_statement(self, p: Production) -> None:
        """printf_statement : PRINTF LPAREN valor RPAREN SEMICOLON"""
        p[0] = ("printf", p[3])

    # Interrupção de loop
    def p_break_statement(self, p: Production) -> None:
        """break_statement : BREAK SEMICOLON"""
        print("Break identificado")
        p[0] = ("break",)

    # Continuação de loop
    def p_continue_statement(self, p: Production) -> None:
        """continue_statement : CONTINUE SEMICOLON"""
        print("Continue identificado")
        p[0] = ("continue",)

    # Retorno de valor
    def p_return_statement(self, p: Production) -> None:
        """return_statement : RETURN valor SEMICOLON"""
        print("Return identificado")
        p[0] = ("return", p[2])

    def p_empty(self, p: Production) -> None:
        "empty :"
        pass

    def p_error(self, p: Production) -> None:
        print(f"Erro de sintaxe em {p.value}")
