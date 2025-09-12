from textnode import TextNode, TextType
import re, pprint

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                node = TextNode(sections[i], TextType.TEXT)
            elif i % 2 == 1:
                node = TextNode(sections[i], text_type)
            split_nodes.append(node)
        new_nodes.extend(split_nodes)
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        text = old_node.text
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for alt_text, url in links:
            delimiter = f"[{alt_text}]({url})"
            text = text.split(delimiter, 1)
            if len(text) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if text[0]:
                new_nodes.append(TextNode(text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            text = text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_img(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        text = old_node.text
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for alt_text, url in images:
            delimiter = f"![{alt_text}]({url})"
            text = text.split(delimiter, 1)
            if len(text) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if text[0]:
                new_nodes.append(TextNode(text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text = text[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
                
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    
def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    for text_type in [TextType.BOLD, TextType.ITALIC, TextType.CODE]:
        nodes = split_nodes_delimiter(nodes, text_type.value, text_type)
    nodes = split_nodes_link(split_nodes_img(nodes))
    return nodes


# textnodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
# pprint.pprint(textnodes)

# textnodes = text_to_textnodes("[this is a google link](https://google.com)")
# pprint.pprint(textnodes)
