from textnode import TextNode
from htmlnode import HTMLNode,markdown_to_html_node, markdown_to_blocks
import os
import shutil



def clear_directory(directory):
    if os.path.exists(directory):
        print("Clearing directory")
        shutil.rmtree(directory)
    os.mkdir(directory)

#src = source directory, dst = destination directory
def recursive_copy(src,dst):
    #If path doesn't exist, make the directory
    if not os.path.exists(dst):
        os.mkdir(dst)
       
    #List all items in the source directory and assign them a path
    for item in os.listdir(src):
        src_item_path = os.path.join(src, item)
        dst_item_path = os.path.join(dst, item)

        if os.path.isfile(src_item_path):
        #copy file
            shutil.copy(src_item_path, dst_item_path)
            print(f"Copied file: {src_item_path}")
        elif os.path.isdir(src_item_path):
            #Recursively copy dir
            recursive_copy(src_item_path,dst_item_path) 

def extract_title(markdown):
    lines = markdown.strip().split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError('No h1 header found in the markdown.')


        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    #print(f"Markdown Content:{markdown_content[:100]}...")

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    #print(f"Template Content:{template_content}...")

    # Convert markdown to HTML Node
    html_node = markdown_to_html_node(markdown_content)
    #print(f"HTML Node Content:{html_node}...")

    # Use the to_html() method to get a string representation
    html_content = html_node.to_html()
    #print(f"HTML Content:{html_content}...")

    # Extract title
    title = extract_title(markdown_content)
    #print(f"Title: {title}")

    # Replace placeholders in template
    final_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    #print(f"Final HTML Content:{final_html}...")


    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML to dest_path
    with open(dest_path, 'w') as f:
        f.write(final_html)

    print("Page generated successfully!")

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    
    dir_list = os.listdir(dir_path_content)

    for item in dir_list:
        item_full_path = os.path.join(dir_path_content, item)
        print(f"Processing: {item_full_path}")

        if os.path.isfile(item_full_path) and item.endswith('.md'):
            dest_file_name = item.replace('.md', '.html')
            dest_file_path = os.path.join(dest_dir_path, dest_file_name)
            print(f"Generating HTML file: {dest_file_path}")

            generate_page(item_full_path,template_path,dest_file_path)
            

        elif os.path.isdir(item_full_path):
            new_dest_dir_path = os.path.join(dest_dir_path,item)
            print(f"Creating/Ensuring directory: {new_dest_dir_path}")

            os.makedirs(new_dest_dir_path, exist_ok=True)
            generate_page_recursive(item_full_path,template_path,new_dest_dir_path)




def main():
    from_path='/home/crimsonchamp/workspace/github.com/Crimsonchamp/ssgenerator/content'
    template_path='/home/crimsonchamp/workspace/github.com/Crimsonchamp/ssgenerator/template.html'
    destination_path='/home/crimsonchamp/workspace/github.com/Crimsonchamp/ssgenerator/public'


    generate_page_recursive(from_path,template_path,destination_path)






if __name__ == "__main__":
    main()

#======================================================================================





