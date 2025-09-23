import os, shutil

def copy_src_to_dst(src, dst):
    for item in os.listdir(src):
        src_subdir_path = os.path.join(src,item)
        dst_subdir_path = os.path.join(dst,item)
        if os.path.isfile(src_subdir_path):
            print(f"copying file: {src_subdir_path}")
            shutil.copy(src_subdir_path, dst)
        else:
            if not os.path.exists(dst_subdir_path):
                os.mkdir(dst_subdir_path)
            copy_src_to_dst(src_subdir_path, dst_subdir_path)
