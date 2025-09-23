import os, shutil
from copy_static import copy_src_to_dst
from markdown_to_blocks import markdown_to_html_node

src = "./static"
dst = "./public"

def extract_title(markdown):
    root_node = markdown_to_html_node(markdown)
    h1_header = None
    for node in root_node.children:
        if node.tag == "h1":
            h1_header = node
        break
    if not h1_header:
        raise Exception("Header not provided in markdown text")
    return h1_header
print(extract_title("# Hello"))

if __name__ == "__main__":
    print(f"deleting {dst} directory...")
    if os.path.exists(os.path.abspath(dst)):
        shutil.rmtree(os.path.abspath(dst))
    os.mkdir(dst)
    print(f"copying {src} --> {dst}")
    copy_src_to_dst(src, dst)

