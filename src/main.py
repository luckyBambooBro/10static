import os, shutil
from copy_static import copy_src_to_dst
from markdown_to_blocks import markdown_to_html_node

src = "./static"
dst = "./public"

def extract_title(markdown):
    title = markdown.split("# ")[1]
    title = title.split("\n\n")[0]
    return title

def generate_page(from_path, template_path, dest_path):
    

extract_title("# Hello")

# if __name__ == "__main__":
#     print(f"deleting {dst} directory...")
#     if os.path.exists(os.path.abspath(dst)):
#         shutil.rmtree(os.path.abspath(dst))
#     os.mkdir(dst)
#     print(f"copying {src} --> {dst}")
#     copy_src_to_dst(src, dst)

