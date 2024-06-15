import unittest

from textnode import TextNode, split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


    def test_no_img_test(self):
        node = TextNode("This is a test with no images.", TextNode.text_type_text)
        result = split_nodes_image([node])
        expected = [TextNode("This is a test with no images.", TextNode.text_type_text)]
        self.assertEqual(result,expected)

    def test_split_single_image(self):
        node = TextNode("This is text with an ![image](https://example.com/image.png).", TextNode.text_type_text)
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextNode.text_type_text),
            TextNode("image", TextNode.text_type_image, "https://example.com/image.png"),
            TextNode(".", TextNode.text_type_text)]
        self.assertEqual(result, expected)
    

    def test_split_nodes_image_multiple_images(self):
        node = TextNode("Text with ![first image](https://example.com/first.png) and ![second image](https://example.com/second.png).", TextNode.text_type_text)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextNode.text_type_text),
            TextNode("first image", TextNode.text_type_image, "https://example.com/first.png"),
            TextNode(" and ", TextNode.text_type_text),
            TextNode("second image", TextNode.text_type_image, "https://example.com/second.png"),
            TextNode(".", TextNode.text_type_text)
            ]
        self.assertEqual(result,expected)


if __name__ == "__main__":
    unittest.main()


#Default test example, make more methods if you'd like to run different tests in the future.