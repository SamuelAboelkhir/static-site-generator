from textnode import TextNode, TextType


def main() -> None:
    textNode = TextNode("some text", TextType.BOLD, "https://localhost")
    print(textNode)


if __name__ == "__main__":
    main()
