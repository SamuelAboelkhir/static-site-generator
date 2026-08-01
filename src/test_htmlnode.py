import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "hello"})
        toHTML = node.props_to_html()
        node2 = ' href="hello"'
        self.assertEqual(toHTML, node2)

    def test_noteq(self):
        node = HTMLNode(props={"bold": "olla"})
        toHTML = node.props_to_html()
        node2 = ' bold="olla"'
        self.assertEqual(toHTML, node2)

    def test_urlIsNone(self):
        node = HTMLNode(props={"anchor": "salut"})
        toHTML = node.props_to_html()
        node2 = ' anchor="salut"'
        self.assertEqual(toHTML, node2)

    def test_eq2(self):
        node = LeafNode("p", "test1", props={"bold": "hello"})
        toHTML = node.to_html()
        node2 = '<p bold="hello">test1</p>'
        self.assertEqual(toHTML, node2)

    def test_eq3(self):
        node = LeafNode("link", "test2", props={"href": "olla"})
        toHTML = node.to_html()
        node2 = '<link href="olla">test2</link>'
        self.assertEqual(toHTML, node2)

    def test_eq4(self):
        node = LeafNode("a", "test3", props={"anchor": "salut"})
        toHTML = node.to_html()
        node2 = '<a anchor="salut">test3</a>'
        self.assertEqual(toHTML, node2)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    _ = unittest.main()
