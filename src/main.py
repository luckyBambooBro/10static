import os, pprint, shutil

src = "static"
dst = "public"

def copy_src_to_dst(src, dst):
    def copy_contents(src, dst):
        for item in os.listdir(src):
            item_path = os.path.join(src,item)
            if os.path.isfile(item_path):
                print(f"copying file: {item_path}")
                shutil.copy(item_path, dst)
            else:
                src_subdir_path = os.path.join(src,item)
                dst_subdir_path = os.path.join(dst,item)
                if not os.path.exists(dst_subdir_path):
                    print(f"creating folder: {dst_subdir_path}")
                    os.mkdir(dst_subdir_path)
                copy_contents(src_subdir_path, dst_subdir_path)
    shutil.rmtree(os.path.abspath(dst))
    os.mkdir(dst)
    copy_contents(src, dst)


if __name__ == "__main__":
    copy_src_to_dst(src, dst)

