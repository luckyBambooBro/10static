from enum import Enum

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
    
