import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode


class TestHTML(unittest.TestCase):

        #Test to see if leaf_node initializes correctly.
        #Creates a node named leaf, tests each leaf attribute.
    def test_leaf_node_initialization(self):
        leaf = LeafNode(tag='p', value='Hello, World!')
        self.assertEqual(leaf.tag, 'p')
        self.assertEqual(leaf.value, 'Hello, World!')
        self.assertEqual(leaf.children, [])
        self.assertEqual(leaf.props, {})

        #Test to see if error flag triggers when value = None
    def test_leaf_node_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag='p', value=None)

        #Test to see if Leafnode .node_to_html formats correctly
    def test_leaf_node_to_html(self):
        leaf = LeafNode(tag='p', value='Hello, World!')
        self.assertEqual(leaf.to_html(), '<p>Hello, World!</p>')

        #Test to see if text returns with no tag present
    def test_leaf_node_no_tag(self):
        leaf = LeafNode(tag=None, value='No Tag Text')
        self.assertEqual(leaf.to_html(), 'No Tag Text')

        #Test to see if parent views leaf correctly
    def test_parent_node_initialization(self):
        leaf = LeafNode(tag='p', value='Hello, World!')
        parent = ParentNode(tag='div', children=[leaf])
        self.assertEqual(parent.tag, 'div')
        self.assertEqual(parent.children, [leaf])
        self.assertEqual(parent.props, {})

        #Test for flag raise if parent has no children
    def test_parent_node_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag='div', children=[])

        #Test to see if parent properly encapsulates leafnodes.
    def test_parent_node_to_html(self):
        leaf1 = LeafNode(tag='b', value='Bold text')
        leaf2 = LeafNode(tag=None, value='Normal text')
        leaf3 = LeafNode(tag='i', value='italic text')
        parent = ParentNode(tag='p', children=[leaf1, leaf2, leaf3, leaf2])
        self.assertEqual(
            parent.to_html(),
            '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )


if __name__ == "__main__":
    unittest.main()