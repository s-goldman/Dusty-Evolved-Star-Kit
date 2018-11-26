import os, shutil
import fnmatch


def remove():
    bad_list = ['model.dat', 'model_directory.tar.gz', 'J1000']

    for item in os.listdir('.'):
        for bad in bad_list:
            if fnmatch.fnmatch(item, bad):
                os.remove(item)
            if os.path.isdir(bad):
                shutil.rmtree(bad)
