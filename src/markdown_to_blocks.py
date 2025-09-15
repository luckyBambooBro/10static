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
            html_nodes = []
            for line in block.split("\n"):
                text_nodes = text_to_textnodes(line)
                for node in text_nodes:
                    html_node = text_node_to_html_node(node)
                    html_nodes.append(html_node)
            return html_nodes #TODO this doesnt add the line break to 
        # the html string. line break should be <br> and only goes at the 
        # end of each line, not beginning and end like many other 
        # html nodes. i have a fix for this but im not implementing it 
        # yet because it requires me to change the Leafnode class, which 
        # would make it different to the lessons solution. consider 
        # changing it after. i have saved the solution in a file 
        # called "return_to_later/FIX_FOR_Leafnode.py" in the root of the project

        case Blocktype.HEADING:
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for node in text_nodes:
                html_nodes.append(text_node_to_html_node(node))
            return html_nodes
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
                parent_node = ParentNode("p", child_nodes)
                
            case Blocktype.HEADING:
                level = 0
                for i in block[:6]:
                    if i == "#":
                        level += 1
                if not 1 <= level <= 6:
                    raise ValueError("Heading must be between <h1> to <h6>")
                child_nodes = text_to_children(block[level + 1: ], block_type)
                parent_node = ParentNode(f"h{level}", child_nodes)
                return parent_node

            case Blocktype.CODE:
                #TODO up to here!
                child_nodes = text_to_children(block.strip("```"), block_type)
                parent_node = ParentNode("code", )

            case Blocktype.QUOTE:
                child_nodes = text_to_children() #incomplete
                parent_node = ParentNode("blockquote", child_nodes)

            case Blocktype.UNORDERED_LIST:
                child_nodes = text_to_children() #incomplete
                parent_node = ParentNode("ul", child_nodes)
                           

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

# testing for Blocktype.PARAGRAPH
# text_to_children("this is the first line with _italics_ in it\nthis is the second line\nand here is some **bolded text** in the 3rd line", Blocktype.PARAGRAPH)

#testing for Blocktype.HEADING
markdown_to_html("### this is a level 3 title\nblah text whatever **bold** _italic_ regular")