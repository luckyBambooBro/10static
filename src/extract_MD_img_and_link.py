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
            old_node_text_copy = old_node.text
            for alt_text, url in matches:
                delimiter = f"[{alt_text}]({url})"
                text = old_node_text_copy.split(delimiter)
                if text[0]:
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                old_node_text_copy = text[1]
            if old_node_text_copy:
                new_nodes.append(TextNode(old_node_text_copy, TextType.TEXT))
    return new_nodes

def split_nodes_img(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            matches = extract_markdown_images(old_node.text)
            old_node_text_copy = old_node.text
            for alt_text, url in matches:
                delimiter = f"![{alt_text}]({url})"
                text = old_node_text_copy.split(delimiter)
                if text[0]:
                    new_nodes.append(TextNode(text[0], TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                old_node_text_copy = text[1]
            if old_node_text_copy:
                new_nodes.append(TextNode(old_node_text_copy, TextType.TEXT))
    print(new_nodes)
    return new_nodes
                

# nodes = [TextNode(
#     "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
#     TextType.TEXT),
#     TextNode("This is text with a `code block` word", TextType.TEXT),
#     TextNode("and this is some bold text", TextType.BOLD)
# ]
# old_nodes = split_nodes_link(nodes)
# print(old_nodes)

nodes = [TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    ),
    TextNode("and here's some italicised text", TextType.ITALIC)
]
old_nodes = split_nodes_img(nodes)