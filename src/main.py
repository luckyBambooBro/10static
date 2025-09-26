import os, shutil
from copy_static import copy_src_to_dst
from markdown_to_blocks import markdown_to_html_node
from generate_page import extract_title, generate_page, generate_pages_recursive

src = "./static"
dst = "./public"
template_path = "./template.html"
dir_path_content = "./content"

if __name__ == "__main__":
    print(f"deleting {dst} directory...")
    if os.path.exists(os.path.abspath(dst)):
        shutil.rmtree(os.path.abspath(dst))
    os.mkdir(dst)
    print(f"copying {src} --> {dst}")
    copy_src_to_dst(src, dst)

    print("Generating content...")
    generate_pages_recursive(
        dir_path_content, 
        template_path, 
        dst)
    # generate_pages_recursive()

