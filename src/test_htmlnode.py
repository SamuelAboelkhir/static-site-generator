import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
