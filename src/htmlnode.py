from textnode import TextNode,text_to_textnodes
import re

    #tag,value,children,props
    #Should hold string representing HTML tag type
    #The text within the html tags
    #list of HTMLNode objects representing children of this node
    #Dictionary of k-v pairs representing attributes of the html flags
    #ex:{"href": "https://www.google.com"}

class HTMLNode:
    #Base model for our HTML nodes, turning into either parent or child.
    #All values default to none unless otherwise

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        #print(f"Initialized HTMLNode: tag={self.tag}, props={self.props}, children={self.children}")
                                            

    def to_html(self):
        raise NotImplementedError
    
    #Method turns Urls/Images into html compatible string, used by children.
    def props_to_html(self):
        props_list = [f'{key}="{value}"' for key,value in self.props.items()]
        return ' '.join(props_list)


    #For testing purposes, return all attributes.
    def __repr__(self):
     return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    
class LeafNode(HTMLNode):
    SELF_CLOSING_TAGS = {'img', 'br', 'hr'}

    def __init__(self, tag, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        if self.value is None and self.tag not in self.SELF_CLOSING_TAGS:
            raise ValueError("LeafNode value cannot be 'None' unless tag is self-closing")
        #print(f"Initialized LeafNode: tag={self.tag}, props={self.props}, children={self.children}")

    def to_html(self):
        if self.tag is None:
            return self.value
        props_string = self.props_to_html()
        if self.tag in self.SELF_CLOSING_TAGS:
            return f"<{self.tag} {props_string}/>" if props_string else f"<{self.tag}/>"
        else:
            return f"<{self.tag} {props_string}>{self.value}</{self.tag}>" if props_string else f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    #Must have children, designed to encapsulate multiple leaf nodes recursively.

    def __init__(self, tag, children,props=None):
        super().__init__(tag=tag,value=None,children=children,props=props)
        if not self.children:
            raise ValueError("Parentnode children cannot be 'None'")
        #print(f"Initialized ParentNode: tag={self.tag}, props={self.props}, children={self.children}")
        
    #ParentNode must have a tag, parent node is to organize blocks of text, not the text iself.
    def to_html(self):
        #print(f"Processing Node: tag={self.tag}, props={self.props}")

        children_html = "".join(child.to_html() for child in self.children)

        if self.tag is None:
            raise ValueError("ParentNode tag cannot be 'None'")

        props_string = self.props_to_html()

        if props_string:
            return f"<{self.tag} {props_string}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"

        
#Converting text_node's .text and/or url to a leafnode via it's text_type.
def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(tag="p", value=text_node.text)  # Assuming "p" (paragraph) for plain text sections

    if text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)

    if text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)

    if text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)

    if text_node.text_type == "link":
        if not text_node.url:
            raise ValueError("text_type 'link' must have a URL")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    if text_node.text_type == "image":
        if not text_node.url:
            raise ValueError("text type 'image' must have URL ")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("text_type must be of: 'text','bold','italic','code','link','image'")

    
def markdown_to_blocks(markdown):
    # Splitting markdown text into blocks based on double newline characters
    return re.split(r'\n\n+', markdown.strip())

#Takes list of blocks and populates a list of typings in same order
def block_to_block_type(block):
    block = block.strip()
    if block.startswith('#'):
        return "heading"
    elif block.startswith('```'):
        return "code_block"
    elif block.startswith('>'):
        return "quote"
    elif block.startswith('- ') or block[0].isdigit() and block[1:3] == '. ':
        return "list"
    elif block.startswith('!['):
        return "image"
    elif block.startswith('['):
        return "link"
    else:
        return "paragraph"

    
def convert_text_node(node):
    if not isinstance(node, TextNode):
        raise TypeError("Expected a TextNode instance")

    if node.text_type == "bold":
        return ParentNode(tag='b', children=[LeafNode(tag=None, value=node.text)])
    elif node.text_type == "italic":
        return ParentNode(tag='i', children=[LeafNode(tag=None, value=node.text)])
    elif node.text_type == "code":
        return ParentNode(tag='code', children=[LeafNode(tag=None, value=node.text)])
    elif node.text_type == "link":
        if not node.url:
            raise ValueError("text_type 'link' must have a URL")
        return ParentNode(tag='a', children=[LeafNode(tag=None, value=node.text)], props={"href": node.url})
    elif node.text_type == "image":
        if not node.url:
            raise ValueError("text_type 'image' must have a URL")
        return LeafNode(tag='img', value="", props={"src": node.url, "alt": node.text})
    elif node.text_type == "text":
        return LeafNode(tag=None, value=node.text)
    else:
        raise ValueError(f"Unknown text_type: {node.text_type}")


    
def convert_heading(block):
    """Convert a heading block to the corresponding heading HTML node."""
    heading_level = block.count('#', 0, block.find(' '))
    heading_text = block[heading_level:].strip()
    text_nodes = text_to_textnodes(heading_text)
    children = []

    for text_node in text_nodes:
        if text_node.text_type == "text":
            children.append(LeafNode(tag=None, value=text_node.text))
        elif text_node.text_type == "bold":
            children.append(LeafNode(tag='b', value=text_node.text))
        elif text_node.text_type == "italic":
            children.append(LeafNode(tag='i', value=text_node.text))
        elif text_node.text_type == "link":
            children.append(LeafNode(tag='a', value=text_node.text, attributes={'href': text_node.url}))
        elif text_node.text_type == "image":
            children.append(LeafNode(tag='img', value=None, attributes={'alt': text_node.text, 'src': text_node.url}))

    return ParentNode(tag=f'h{heading_level}', children=children)



def convert_paragraph(block):
    """Convert a paragraph block to a paragraph HTML node."""
    text_nodes = text_to_textnodes(block.strip())
    children = []

    for text_node in text_nodes:
        if text_node.text_type == "text":
            children.append(LeafNode(tag=None, value=text_node.text))
        elif text_node.text_type == "bold":
            children.append(LeafNode(tag='strong', value=text_node.text))
        elif text_node.text_type == "italic":
            children.append(LeafNode(tag='em', value=text_node.text))
        elif text_node.text_type == "link":
             children.append(LeafNode(tag='a', value=text_node.text, props={'href': text_node.url}))
        elif text_node.text_type == "image":
            children.append(LeafNode(tag='img', value=None, props={'alt': text_node.text, 'src': text_node.url}))

    return ParentNode(tag='p', children=children)



def convert_code_block(block):
    # Remove the triple backticks and any surrounding whitespace
    code_content = block.strip('`').strip()
    # Create the inner code node
    code_node = LeafNode(tag='code', value=code_content)
    # Create the outer pre node that contains the code node
    pre_node = ParentNode(tag='pre', children=[code_node])
    return pre_node


def convert_quote(block):
    """Convert a quote block to a blockquote HTML node."""
    lines = block.strip().split('\n')
    quoted_text = []

    for line in lines:
        # Remove the leading '>'
        if line.strip().startswith('>'):
            quoted_text.append(line.lstrip('> ').strip())
    
    # Combine all the quoted lines into a single string
    combined_text = ' '.join(quoted_text)
    text_nodes = text_to_textnodes(combined_text)
    children = []

    for text_node in text_nodes:
        if text_node.text_type == "text":
            children.append(LeafNode(tag=None, value=text_node.text))
        elif text_node.text_type == "bold":
            children.append(LeafNode(tag='strong', value=text_node.text))
        elif text_node.text_type == "italic":
            children.append(LeafNode(tag='em', value=text_node.text))
        elif text_node.text_type == "link":
            children.append(LeafNode(tag='a', value=text_node.text, attributes={'href': text_node.url}))
        elif text_node.text_type == "image":
            children.append(LeafNode(tag='img', value=None, attributes={'alt': text_node.text, 'src': text_node.url}))

    return ParentNode(tag='blockquote', children=children)


def convert_list(block):
    items = block.strip().split('\n')
    if not items:
        raise ValueError("List should contain at least one item.")
    
    is_ordered = items[0].strip().startswith('1.')
    tag = 'ol' if is_ordered else 'ul'
    children = []

    for item in items:
        item_text = item.lstrip('- 1234567890.').strip()  # Adjust stripping for ordered and unordered lists
        text_nodes = text_to_textnodes(item_text)
        li_children = []

        for text_node in text_nodes:
            if text_node.text_type == "text":
                li_children.append(LeafNode(tag=None, value=text_node.text))
            elif text_node.text_type == "bold":
                li_children.append(LeafNode(tag='strong', value=text_node.text))
            elif text_node.text_type == "italic":
                li_children.append(LeafNode(tag='em', value=text_node.text))
            elif text_node.text_type == "link":
                li_children.append(LeafNode(tag='a', value=text_node.text, attributes={'href': text_node.url}))
            elif text_node.text_type == "image":
                li_children.append(LeafNode(tag='img', value=None, attributes={'alt': text_node.text, 'src': text_node.url}))
        
        li_node = ParentNode(tag='li', children=li_children)
        children.append(li_node)

    return ParentNode(tag=tag, children=children)




def convert_image(markdown_image):
    import re
    # Example markdown image: ![Alt text](/path/to/image)
    match = re.match(r"!\[(.*?)\]\((.*?)\)", markdown_image)
    if not match:
        raise ValueError("Invalid markdown image format")

    alt_text, src = match.groups()
    #print(f"Parsing image: alt_text='{alt_text}', src='{src}'")  # Diagnostic print
    return LeafNode(tag='img', value=None, props={'src': src, 'alt': alt_text})



def convert_link(markdown_link):
    import re
    # Example markdown link: [Example Text](http://example.com)
    match = re.match(r"\[(.*?)\]\((.*?)\)", markdown_link)
    if not match:
        raise ValueError("Invalid markdown link format")

    text, href = match.groups()
    #print(f"Parsing link: text='{text}', href='{href}'")  # Diagnostic print
    return LeafNode(tag='a', value=text, props={'href': href})





def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            html_blocks.append(convert_heading(block))
        elif block_type == "paragraph":
            html_blocks.append(convert_paragraph(block))
        elif block_type == "code_block":
            html_blocks.append(convert_code_block(block))
        elif block_type == "quote":
            html_blocks.append(convert_quote(block))
        elif block_type == "list":
            html_blocks.append(convert_list(block))
        elif block_type == "image":
            html_blocks.append(convert_image(block))
        elif block_type == "link":
            html_blocks.append(convert_link(block))
        else:
            raise ValueError(f"Unsupported block type: {block_type}")

    html_node = ParentNode(tag='div', children=html_blocks)
    #print(f"Generated HTML Node: {html_node.to_html()[:100]}...")  # Show first 100 chars only
    return html_node


#=======================================================================================================











