from src.emoji_parser import EmojiParser


def main() -> None:
    parser = EmojiParser()

    with open("data/ex1.txt", "r") as file:
        codigo = file.read()

    parser.lexer.test(codigo)
    parser.parse(codigo)


if __name__ == "__main__":
    main()
