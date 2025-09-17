from enum import Enum
from htmlnode import ParentNode, LeafNode 
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from markdown_to_blocks import (
    markdown_to_blocks, 
    block_to_block_type, 
    Blocktype
)
import pprint

def text_to_children(block, blocktype):
    match blocktype:
        case Blocktype.PARAGRAPH:
            text_nodes = []
            html_nodes = []
            for line in block.split("\n"):
                text_nodes.extend(text_to_textnodes(line + "<br>"))    
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
     
        case Blocktype.HEADING:
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
        case Blocktype.CODE:
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
        case Blocktype.QUOTE:
            text_nodes = text_to_textnodes(block)
            html_nodes = []
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
        case Blocktype.UNORDERED_LIST:
            reformatted_list = []
            for text in block.split("\n"):
                reformatted_list.append(text.replace("- ", "<li>") + "</li>")
            text_nodes = []
            html_nodes = []
            for text in reformatted_list:
                text_nodes.extend(text_to_textnodes(text))
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
        case Blocktype.ORDERED_LIST:
            reformatted_list = []
            for text in block.split("\n"):
                reformatted_list.append("<li>" + text[3:] + "</li>")
            text_nodes = []
            html_nodes = []
            for text in reformatted_list:
                text_nodes.extend(text_to_textnodes(text))
            for text_node in text_nodes:
                html_nodes.append(text_node_to_html_node(text_node))
            return html_nodes
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