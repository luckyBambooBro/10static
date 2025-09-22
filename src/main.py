import os, pprint, shutil

source = "static"
dest = "public"

def copy_contents(source, dest, paths=[]):
    shutil.rmtree(os.path.abspath(dest))
    os.mkdir(dest)
    
    for item in os.listdir(source):
        #TODO up to here but this is a good start
        if os.path.isfilepath(item):
            paths.append(item)
        else:
            if not os.path.exists(item):
                os.mkdir(os.path.join(dest, item))
                #   TODO continue


copy_contents(source, dest)