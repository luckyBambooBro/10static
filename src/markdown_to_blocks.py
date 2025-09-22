from enum import Enum
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    O_LIST = "unordered_list"
    U_LIST = "ordered_list"
    
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
    blocks = [b for b in blocks if b]
    return blocks

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")    
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return Blocktype.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return Blocktype.CODE
    if markdown_block.startswith(">"):
        return Blocktype.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return Blocktype.PARAGRAPH
        return Blocktype.U_LIST
    if markdown_block.startswith("1. "):
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return Blocktype.PARAGRAPH
            counter += 1
        return Blocktype.O_LIST
    return Blocktype.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case Blocktype.PARAGRAPH:
            return paragraph_to_html_node(block)
        case Blocktype.HEADING:
            return heading_to_html_node(block)
        case Blocktype.CODE:
            return code_to_html_node(block)
        case Blocktype.O_LIST:
            return o_list_to_html_node(block)
        case Blocktype.U_LIST:
            return u_list_to_html_node(block)
        case Blocktype.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}") #blocks against empty headings, cos if they entered "# ", it would actually work
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block): #TODO: this is different to the lessons solution and is to be tested. Boots tested it and said it was ok though
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.CODE)
    child = text_node_to_html_node(raw_text_node)
    return ParentNode("pre", [child])

def o_list_to_html_node(block):
    list_items = block.split("\n")
    text_items = [item[3:] for item in list_items]
    children = [ParentNode("li", text_to_children(text_item)) for text_item in text_items]
    return ParentNode("ol", children)

def u_list_to_html_node(block):
    list_items = block.split("\n")
    text_items = [item[2:] for item in list_items]
    children = [ParentNode("li", text_to_children(text_item)) for text_item in text_items]
    return ParentNode("ul", children)

def quote_to_html_node(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

