import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_links(old_node.text)
            # text_to_split = old_node.text
            delimiters = []
            old_node_text_copy = old_node.text
            for alt_text, url in matches:
                delimiter = f"[{alt_text}]({url})"
                delimiters.append(delimiter)
                text = old_node_text_copy.split(delimiter)
                if text[0]:
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                old_node_text_copy = text[1]
            if old_node_text_copy:
                new_nodes.append(TextNode(old_node_text_copy, TextType.TEXT))
            print(new_nodes)
node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])