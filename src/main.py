from enum import Enum
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from markdown_to_blocks import (
    markdown_to_blocks, 
    block_to_block_type, 
    Blocktype
)

def text_to_children(block, blocktype):
    def list_processor(reformatted_list):
            text_nodes = []
            for text in reformatted_list:
                text_nodes.extend(text_to_textnodes(text))
            return [text_node_to_html_node(text_node) for text_node in text_nodes]
    
    match blocktype:
        case Blocktype.PARAGRAPH | Blocktype.HEADING | Blocktype.CODE | Blocktype.QUOTE:
            text_nodes = text_to_textnodes(block)
            return [text_node_to_html_node(text_node) for text_node in text_nodes] 

        case Blocktype.UNORDERED_LIST:
            reformatted_list = [text.replace("- ", "<li>") + "</li>" for text in block.split("\n")]
            return list_processor(reformatted_list)
        
        case Blocktype.ORDERED_LIST:
            reformatted_list = ["<li>" + text[3:] + "</li>" for text in block.split("\n")]
            return list_processor(reformatted_list)

        case _:
            raise TypeError("blocktype must be a Blocktype class object")



def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case Blocktype.PARAGRAPH:
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
                block = block.strip("\n")
                child_nodes = text_to_children(block, Blocktype.CODE)
                parent_node = ParentNode("code", child_nodes)
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


#TODO: nothing to do just letting myself know this is the test below
md_text = markdown_to_html("- paragraph lorem ipsum\n- more random text\n- blah blah blah\n\n# new heading 1\n\n###### new heading 6\n\n" \
"####### tried 7 #'s for heading so should be a paragraph\n\n- tim tams\n- boost\n\nnew line of text\n\n" \
"1. tim tams\n2. boost\n\n```code\nmore code\nend code\n```\n\n>quote\nmore text in quote but no > so should be paragraph?\n\n" \
"> proper quote here maybe\n> more quote i hope\n> cos im including the >\n\nactually both the quotes should work but the 2nd one should" \
"have > in every line")
print(md_text.to_html())