import os, shutil
import fnmatch


def remove():
    bad_list = ['model.dat', 'model_directory.tar.gz', 'J400', 'J1000', 'H11', 'R12', 'R13']

    for item in os.listdir('.'):
        for bad in bad_list:
            if fnmatch.fnmatch(item, bad):
                if os.path.isdir(bad):
                    shutil.rmtree(bad)
                else:
                    os.remove(item)
