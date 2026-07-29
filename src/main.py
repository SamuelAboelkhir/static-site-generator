from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main() -> None:
    textNode = TextNode("some text", TextType.BOLD, "https://localhost")
    print(textNode)

    htmlNode = HTMLNode("anchor", "hello", None, {"anchor": "hello"})
    print(htmlNode.props_to_html())


if __name__ == "__main__":
    main()
