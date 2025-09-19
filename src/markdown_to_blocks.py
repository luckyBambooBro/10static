from enum import Enum
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

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
    def list_processor(reformatted_list):
            text_nodes = []
            for text in reformatted_list:
                text_nodes.extend(text_to_textnodes(text))
            return [text_node_to_html_node(text_node) for text_node in text_nodes]
    
    match blocktype:
        case Blocktype.PARAGRAPH | Blocktype.HEADING | Blocktype.QUOTE:
            text_nodes = text_to_textnodes(block)
            return [text_node_to_html_node(text_node) for text_node in text_nodes] 
        
        case Blocktype.CODE:
            return [text_node_to_html_node(TextNode(block, TextType.CODE))]

        case Blocktype.UNORDERED_LIST:
            reformatted_list = [text.replace("- ", "<li>") + "</li>" for text in block.split("\n")]
            return list_processor(reformatted_list)
        
        case Blocktype.ORDERED_LIST:
            reformatted_list = ["<li>" + text[3:] + "</li>" for text in block.split("\n")]
            return list_processor(reformatted_list)

        case _:
            raise TypeError("blocktype must be a Blocktype class object")



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case Blocktype.PARAGRAPH:
                block = block.replace("\n", "")
                child_nodes = text_to_children(block, Blocktype.PARAGRAPH)
                parent_node = ParentNode("p", child_nodes)
                parent_nodes.append(parent_node)
                
            case Blocktype.HEADING:
                level = 0
                for i in block[:6]:
                    if i == "#":
                        level += 1
                if not 1 <= level <= 6:
                    raise ValueError("Heading must be between <h1> to <h6>")
                child_nodes = text_to_children(block[level + 1: ], Blocktype.HEADING)
                parent_node = ParentNode(f"h{level}", child_nodes)
                parent_nodes.append(parent_node)

            case Blocktype.CODE:
                block = block.strip("```")
                block = block.lstrip("\n")
                child_nodes = text_to_children(block, Blocktype.CODE)
                parent_node = ParentNode("pre", child_nodes)
                parent_nodes.append(parent_node)

            case Blocktype.QUOTE:
                block = block.strip(">")
                child_nodes = text_to_children(block, Blocktype.QUOTE) 
                parent_node = ParentNode("blockquote", child_nodes)
                parent_nodes.append(parent_node)

            case Blocktype.UNORDERED_LIST:
                child_nodes = text_to_children(block, Blocktype.UNORDERED_LIST) 
                parent_node = ParentNode("ul", child_nodes)
                parent_nodes.append(parent_node)
                           
            case Blocktype.ORDERED_LIST:
                child_nodes = text_to_children(block, Blocktype.ORDERED_LIST) 
                parent_node = ParentNode("ol", child_nodes)
                parent_nodes.append(parent_node)
    root_parent_node = ParentNode("div", parent_nodes)
    return root_parent_node



md_text = markdown_to_html_node("""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

""")
# print(md_text.to_html())
