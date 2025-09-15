from enum import Enum
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class Blocktype(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
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
        for line in lines:
            if not line.startswith(">"):
                return Blocktype.PARAGRAPH
        return Blocktype.QUOTE
    if markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return Blocktype.PARAGRAPH
        return Blocktype.UNORDERED_LIST
    if markdown_block.startswith("1. "):
        counter = 1
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return Blocktype.PARAGRAPH
            counter += 1
        return Blocktype.ORDERED_LIST
    return Blocktype.PARAGRAPH

def text_to_children(block, blocktype):
    match blocktype:
        case Blocktype.PARAGRAPH:
            for line in block.split("\n"):
                text_nodes = text_to_textnodes(line)
                html_nodes = []
                for node in text_nodes:
                    html_node = text_node_to_html_node(node)
                    html_nodes.append(html_node)
                print(html_nodes)

        case Blocktype.HEADING:
            pass
        case Blocktype.CODE:
            pass
        case Blocktype.QUOTE:
            pass
        case Blocktype.UNORDERED_LIST:
            pass
        case Blocktype.ORDERED_LIST:
            pass
        case _:
            raise TypeError("blocktype must be a Blocktype class object")

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_w_tags = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case Blocktype.PARAGRAPH:
                child_nodes = text_to_children(block, block_type)
                parent_node = ParentNode("<p>", [block])
            case Blocktype.HEADING:
                level = 0
                for i in block[:6]:
                    if i == "#":
                        level += 1
                if not 1 <= level <= 6:
                    raise ValueError("Heading must be between <h1> to <h6>")
                parent_node = ParentNode(f"h{level}", block[level + 1:])
            case Blocktype.CODE:
                parent_node = ParentNode("<code>", block.strip("```"))
            case Blocktype.QUOTE:
                parent_node = ParentNode("<blockquote>", block)
                           

# md = """
# #### Firstly here is a <h4> heading

# This is **bolded** paragraph
# text in a p
# tag here

# This is another paragraph with _italic_ text and `code` here

# and an unordered list:

# - tim tims
# - boost
# - honey soy chicken chips
# """
# html_nodes = markdown_to_html(md)
# print(html_nodes)

text_to_children("this is the first line with _italics_ in it\n this is the second line\n and here is some **bolded text** in the 3rd line", Blocktype.PARAGRAPH)