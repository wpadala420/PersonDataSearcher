import os, shutil

def clear_temportary_files(path):
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            shutil.rmtree(filepath)