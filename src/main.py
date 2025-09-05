from textnode import TextNode, TextType #does this need "." before textnode?

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
main()

