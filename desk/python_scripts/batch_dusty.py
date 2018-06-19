from multiprocessing import cpu_count
import subprocess
import os
import sys
import time
from fnmatch import fnmatch

'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This package is a multiprocessing script for running the DUSTY code (Elitzur & Ivezic 2001, MNRAS, 327, 403). 
The input is just the directory containing the *.inp files. All * .inp files within the directory will be run.

'''

npro = cpu_count() - 1
start = time.time()

nn = 0
sleep_time = 10 
grid_name = 'astronomical'

print()
for item in os.listdir('.'):
    if not fnmatch(item, '*.*'):
        print(item)
print()

grid_name = input('directory name: ')

files_dir = os.getcwd()
files = []
for item in os.listdir(files_dir):
    if grid_name+"_" in item and '0.inp' in item:
        files.append(item.split('.')[0])
a = sorted(files)

running = {}
times = []
starts = {}
for n, item in enumerate(a):
    with open('dusty.inp', 'w') as f:
        f.write('\t'+str(item)+'\n')
        f.close()
    starts[n] = time.time()
    print(('\t \t running: ' + item))
    pro = subprocess.Popen(["./dusty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    running[n] = pro
    
    while len(running) >= npro:
        for nn, pro in list(running.items()):
            pro.poll()
        if pro.returncode is not None:
            times.append((time.time() - starts[nn])/(60*60))
            pro.communicate()
            del(starts[nn])
            del(running[nn])
        time.sleep(sleep_time)
    if len(times) > 0:
        avg_time = sum(times)/len(times)
        left_to_do = len(a) - n
        print((str(round(left_to_do*avg_time/npro, 2))+' hours left'+'\t\t'+str(left_to_do)+' / '+str(len(a))))
print("Complete")
end = time.time()
print(('total time = ' + str(round((end-start)/60/60))+" hours"))
