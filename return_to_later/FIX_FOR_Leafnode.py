# Add void tags in for things like line breaks in 
# the Blocktype.PARAGRAPH for src/markdown_to_blocks.py 
# text_to_children()
# this will have to be added to the LeafNode class
# the LeafNode class should look like this eventually
# look like this:

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    VOID_TAGS = {"br", "img", "hr", "input", "meta", "link", "source", "track", "area", "col", "embed", "param", "wbr"}

    def to_html(self):
        if self.tag in self.VOID_TAGS:
            # ignore value, no closing tag
            return f"<{self.tag}{self.props_to_html()}>"
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
