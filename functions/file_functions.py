import os, shutil


def clear_temportary_files(path):
    dir_list = os.listdir(path)
    for filename in dir_list:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)
        else:
            os.remove(filepath)