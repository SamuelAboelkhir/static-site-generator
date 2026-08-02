import re
from enum import Enum
from typing import override

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    text: str
    text_type: TextType
    url: str | None

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("URL is required for link text type")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("URL is required for link text type")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:  # pyright: ignore[reportUnnecessaryComparison]
            raise ValueError(
                f"Invalid text type: {text_node.text_type}"
            )  # pyright: ignore[reportUnreachable]


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes: list[TextNode] = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images: list[str] = re.findall(r"\!\[.+?\)", text)
    tuples: list[tuple[str, str]] = []
    for image in images:
        alt: list[str] = re.findall(r"\[(.*?)\]", image)
        url: list[str] = re.findall(r"\((.*?)\)", image)
        tuples.append((alt[0], url[0]))

    return tuples


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links: list[str] = re.findall(r"(?<!!)\[.+?\)", text)
    tuples: list[tuple[str, str]] = []
    for link in links:
        alt: list[str] = re.findall(r"\[(.+?)\]", link)
        url: list[str] = re.findall(r"\((.+?)\)", link)
        tuples.append((alt[0], url[0]))

    return tuples
