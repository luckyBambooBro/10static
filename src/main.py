import os, shutil

source = "static"
dest = "public"

def copy_contents(source, dest):
    shutil.rmtree(os.path.join(dest))
    os.mkdir(dest)
    src_paths = obtain_src_paths(source)
    for item in src_paths:
        shutil.copy(item, dest)
    print(src_paths)
    #TODO: so far my function just copies the files straight into dst. i need to 
    # make it so that it copies the full file path including the subdirectories that 
    # contain the file#


def obtain_src_paths(source, paths=[]):
    dest_contents = os.listdir(source)
    if not dest_contents:
        paths.append(source)
        return
    for item in dest_contents:
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            paths.append(item_path)
        else:
            obtain_src_paths(os.path.join(source, item), paths)
    return paths

copy_contents(source, dest)