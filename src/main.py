import os, shutil 

def copy_files(source, destination):
    src = os.path.abspath(source)
    dst = os.path.abspath(destination)
    if not os.path.exists(src) or not os.path.exists(dst):
        raise FileNotFoundError("src or dst directory path does not exist")

    dst_files_paths = [os.path.join(dst, dst_file_path) for dst_file_path in os.listdir(dst)]
    for file in dst_files_paths:
        os.remove(file)
    print(f"successfully removed files in {destination}")

    source_file_paths = [os.path.join(src, src_file_path) for src_file_path in os.listdir(src)]
    print(source_file_paths)
    #TODO up to here. only gets me the image directory not the image files inside it

copy_files("static", "public")
