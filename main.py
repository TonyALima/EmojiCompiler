from src.emoji_parser import EmojiParser


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

    with open("data/ex1.txt", "r") as file:
        codigo = file.read()

    parser.lexer.test(codigo)
    r = parser.parse(codigo)
    print(r)
    print_hierarchical_dict(r, 0)


if __name__ == "__main__":
    main()
