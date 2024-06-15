import re



class TextNode:

    text_type_text = "text"
    text_type_image = "image"
    text_type_link = "link"

    

    #Creates a textnode with text and a text_type, optionally a url/image depending on text type.
    def __init__(self,text,text_type,url=None):
        valid_text_types = {"text", "bold", "italic", "code", "link", "image"}
        if text_type not in valid_text_types:
            raise ValueError("text_type must be one of: 'text','bold','italic','code','link','image'")

        if text_type in {"link","image"} and not url:
            raise ValueError("URL must be provided for text_type 'link' or 'image'")
                
    
        self.text = text  
        self.text_type = text_type
        self.url = url
    
        
        
            
    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"
    


#This delimiter will return a new list of nodes from strings of text, based on the list of delimiters.
#If delimiters are found within other delimiters, only outter delimiter will apply, but it will remove the inner delimiters to keep it clean.

def split_nodes_delimiter(nodes):
    result_nodes = []

    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'\*(.*?)\*')

    for node in nodes:
        if node.text_type == "text":
            text = node.text

            while True:
                bold_match = bold_pattern.search(text)
                italic_match = italic_pattern.search(text)

                if not bold_match and not italic_match:
                    result_nodes.append(TextNode(text, "text"))
                    break

                # Determine the earliest match
                match = min(filter(None, [bold_match, italic_match]), key=lambda m: m.start())

                # Add text before the match
                if match.start() > 0:
                    result_nodes.append(TextNode(text[:match.start()], "text"))

                # Add the matched text
                if bold_match and match == bold_match:
                    result_nodes.append(TextNode(match.group(1), "bold"))
                elif italic_match and match == italic_match:
                    result_nodes.append(TextNode(match.group(1), "italic"))

                # Update the remaining text
                text = text[match.end():]
        else:
            result_nodes.append(node)

    return result_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)
    

def split_nodes_image(nodes):
    result_nodes = []
    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    for node in nodes:
        if node.text_type == "text":
            text = node.text

            while True:
                match = image_pattern.search(text)
                if not match:
                    result_nodes.append(TextNode(text, "text"))
                    break

                # Add text before the match
                if match.start() > 0:
                    result_nodes.append(TextNode(text[:match.start()], "text"))

                # Add the image node
                alt_text = match.group(1)
                image_url = match.group(2)
                result_nodes.append(TextNode(alt_text, "image", url=image_url))

                # Update remaining text
                text = text[match.end():]
        else:
            result_nodes.append(node)

    return result_nodes

def split_nodes_link(nodes):
    result_nodes = []
    link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')

    for node in nodes:
        if node.text_type == "text":
            text = node.text
            #print(f"Processing text for link parsing: {text}")  # Debug print

            while True:
                match = link_pattern.search(text)
                if not match:
                    result_nodes.append(TextNode(text, "text"))
                    break

                # Add text before the match
                if match.start() > 0:
                    result_nodes.append(TextNode(text[:match.start()], "text"))

                # Add the link node
                link_text = match.group(1)
                link_url = match.group(2)
                #print(f"Found link: text='{link_text}', url='{link_url}'")  # Debug print
                result_nodes.append(TextNode(link_text, "link", url=link_url))

                # Update remaining text
                text = text[match.end():]
        else:
            result_nodes.append(node)

    return result_nodes

#This function takes care of the inline text.
def text_to_textnodes(text):
    
    initial_nodes = [TextNode(text, "text")]
    #print("Initial nodes:", initial_nodes)  # Debug print
    
    #print('===================================================')

    after_delimiters= split_nodes_delimiter(initial_nodes)
    #print("After splitting delimiters:", after_delimiters)  # Debug print
   
    #print('===================================================')

    after_images= split_nodes_image(after_delimiters)
    #print("After splitting images:", after_images)  # Debug print
    
    #print('===================================================')

    final_nodes= split_nodes_link(after_images)
    #print("Final nodes after splitting links:", final_nodes)  # Debug print

    return final_nodes






