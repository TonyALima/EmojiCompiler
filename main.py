from src.emoji_parser import EmojiParser
from src.translate import traduzir_estrutura


def print_hierarchical_dict(d, level=0):
    indent = "    " * level
    if isinstance(d, dict):
        for key, value in d.items():
            print(f"{indent}{key}:")
            if isinstance(value, (dict, list)):
                print_hierarchical_dict(value, level + 1)
            else:
                print(f"{indent}    {value}")
    elif isinstance(d, list):
        for item in d:
            print_hierarchical_dict(item, level)
    else:
        print(f"{indent}{d}")


def main() -> None:
    parser = EmojiParser()

    with open("data/EhDois.emo", "r") as file:
        codigo = file.read()

    parser.lexer.test(codigo)
    r = parser.parse(codigo)

    print_hierarchical_dict(r, 0)

    print("/" + 10 * "-" + "Código python" + 10 * "-" + "/")
    codigo_python = traduzir_estrutura(r)

    print(codigo_python)


if __name__ == "__main__":
    main()
