import ply.lex as lex


class EmojiLexer:
    # Lista de tokens
    tokens = (
        "NOME",
        "INT",
        "FLOAT",
        "CHAR",
        "VOID",
        "BOOL",
        "ASSIGN",
        "SCANF",
        "PRINTF",
        "IF",
        "ELSE",
        "WHILE",
        "FOR",
        "EQUAL",
        "NEQUAL",
        "GT",
        "LT",
        "GTE",
        "LTE",
        "AND",
        "OR",
        "NOT",
        "PLUS",
        "MINUS",
        "MULTIPLY",
        "DIV",
        "MOD",
        "LBRACE",
        "RBRACE",
        "LPAREN",
        "RPAREN",
        "LBRACKET",
        "RBRACKET",
        "COMMA",
        "SEMICOLON",
        "DOT",
        "SQUOTE",
        "TRUE",
        "FALSE",
        "BREAK",
        "CONTINUE",
        "RETURN",
        "MAIN",
        "NUMBER",
        "CHARACTER",
    )

    # Expressões regulares para tokens simples
    t_CHAR = r"🔤"
    t_INT = r"ℹ️"
    t_FLOAT = r"☁"
    t_VOID = r"🥚"
    t_BOOL = r"🐃"
    t_ASSIGN = r"🟰"
    t_SCANF = r"🔍"
    t_PRINTF = r"🖨"
    t_IF = r"🤔"
    t_ELSE = r"🙄"
    t_WHILE = r"🧄"
    t_FOR = r"🍀"
    t_EQUAL = r"🟰🟰"
    t_NEQUAL = r"❗🟰"
    t_GT = r"🙌"
    t_LT = r"🤏"
    t_GTE = r"🙌🟰"
    t_LTE = r"🤏🟰"
    t_AND = r"🤝"
    t_OR = r"🖖"
    t_NOT = r"❗"
    t_PLUS = r"➕"
    t_MINUS = r"➖"
    t_MULTIPLY = r"✖"
    t_DIV = r"➗"
    t_MOD = r"💩"
    t_LBRACE = r"👉"
    t_RBRACE = r"👈"
    t_LPAREN = r"🤜"
    t_RPAREN = r"🤛"
    t_LBRACKET = r"👇"
    t_RBRACKET = r"👆"
    t_COMMA = r"❤"
    t_SEMICOLON = r"❣"
    t_DOT = r"💥"
    t_SQUOTE = r"🙏"
    t_TRUE = r"👍"
    t_FALSE = r"👎"
    t_BREAK = r"❌"
    t_CONTINUE = r"✅"
    t_RETURN = r"🔄"
    t_MAIN = r"👨"
    t_NOME = r"[a-z]+([0-9]||[a-z])*"

    # Regra para ignorar espaços e tabulações
    t_ignore = " \t"

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_NUMBER(self, t: lex.LexToken):
        r"[0-9]+(💥[0-9]+)?"
        t.value = float(t.value.replace("💥", ".")) if "💥" in t.value else int(t.value)
        return t

    def t_CHARACTER(self, t: lex.LexToken):
        r"🙏([^🙏])*🙏"
        t.value = t.value[1:-1]  # Remova as aspas simples
        return t

    # Função para contagem de linhas
    def t_newline(self, t: lex.LexToken):
        r"\n+"
        t.lexer.lineno += len(t.value)

    # Regra para capturar erros
    def t_error(self, t: lex.LexToken):
        print(f"Caracter inválido '{t.value[0]}'")
        t.lexer.skip(1)

    # Test it output
    def test(self, data: str) -> None:
        self.lexer.input(data)
        for tok in self.lexer:
            print(tok.type, tok.value, tok.lineno, tok.lexpos)
        print()


if __name__ == "__main__":
    l = EmojiLexer()

    data: str = [
        """
        ℹ x🟰5❣
        👨
        👉
            🖨🤜x🤛❣
        👈
        """,
        "ℹ👨🤜🤛👉 🔤x🟰5💥1❣ 👈",
        "ℹ👨🤜🤛👉 🔤x🟰🙏a🙏❣ 👈",
        "☁ pi 🟰 3💥141592654❣",
        "🐃 b 🟰 👍",
        "🔤 a 🟰 🙏_🙏",
        """🍀 🤜 ℹ️i🟰0 ❣ i 🤏 10 ❣ i 🟰 i ➕ 1 🤛 
            👉
                
            👈""",
    ]

    for code in data:
        l.test(code)
