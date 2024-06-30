import sys

from src.emoji_parser import EmojiParser
from src.gcc_translate import Translator


def main():
    parser = EmojiParser()
    translator = Translator()

    codigo: str = ""
    output: str = "output"

    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as file:
            codigo = file.read()
        if len(sys.argv) == 3:
            output = sys.argv[2]
    else:
        print("Usage python main.py <file.emo> [<output_name>]")

    print("/" + 10 * "-" + "Analise Lexica" + 10 * "-" + "/\n")
    parser.lexer.test(codigo)
    print("/" + 10 * "-" + "Analise Sintatica" + 10 * "-" + "/\n")
    r = parser.parse(codigo, True)
    print("/" + 10 * "-" + "Tradução" + 10 * "-" + "/\n")
    translator.translate(codigo, name=output, execute=True)


if __name__ == "__main__":
    main()
