import os, pprint, shutil
from markdown_to_blocks import markdown_to_html_node

src = "static"
dst = "public"

def copy_src_to_dst(src, dst):
    def copy_contents(src, dst):
        for item in os.listdir(src):
            src_subdir_path = os.path.join(src,item)
            dst_subdir_path = os.path.join(dst,item)
            if os.path.isfile(src_subdir_path):
                print(f"copying file: {src_subdir_path}")
                shutil.copy(src_subdir_path, dst)
            else:
                if not os.path.exists(dst_subdir_path):
                    os.mkdir(dst_subdir_path)
                copy_contents(src_subdir_path, dst_subdir_path)
    shutil.rmtree(os.path.abspath(dst))
    os.mkdir(dst)
    copy_contents(src, dst)


# def extract_title(markdown):
#     root_node = markdown_to_html_node(markdown)
#     h1_header = None
#     for node in root_node.children:
#         if node.tag == "h1":
#             h1_header = node
#         break
#     if not h1_header:
#         raise Exception("Header not provided in markdown text")
#     return h1_header
# print(extract_title("# Hello"))

if __name__ == "__main__":
    copy_src_to_dst(src, dst)

