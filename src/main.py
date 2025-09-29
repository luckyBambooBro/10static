import os, shutil, sys
from copy_static import copy_src_to_dst
from generate_page import generate_pages_recursive

src = "./static"
dst = "./public"
template_path = "./template.html"
dir_path_content = "./content"
basepath = sys.argv[1] if len(sys.argv) > 1 else "/"



if __name__ == "__main__":
    print(basepath)
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
        dst, basepath)


