import urllib
import sys
import tarfile
import shutil
import pdb
import os
from fnmatch import fnmatch
from tqdm import tqdm
import numpy as np
from astropy.table import vstack, Table, Column


def get_models(model_grid_name):

    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))


    full_path = str(__file__.replace('get_remote_models.py', ''))
    grids = ['Crystalline-20-bb',
                  'H11-LMC',
                  'Oss-Orich-aringer',
                  'Oss-Orich-bb',
                  'Zubko-Crich-aringer',
                  'Zubko-Crich-bb',
                  'arnold-palmer',
                  'big-grain',
                  'corundum-20-bb',
                  'fifth-iron',
                  'half-iron',
                  'one-fifth-carbon'
                  ]
    grid_csv_link = ['https://stsci.box.com/shared/static/jxtabj6h5zi7a8ggb0mbtag3v6b4b9i7.csv',
                  'https://stsci.box.com/shared/static/j7f01dwbsbluq4htdwlsx3v0jknye883.csv',
                  'https://stsci.box.com/shared/static/he92pt1yov18x6ska5f4f4q94gal6tr5.csv',
                  'https://stsci.box.com/shared/static/pnljezbu8c7rcyorb27yh6hylk5wy2fs.csv',
                  'https://stsci.box.com/shared/static/x9fg8lacbbiye591tz723ilcqgcomyjh.csv',
                  'https://stsci.box.com/shared/static/4b9rc9zl110khexeuo8thb8r58mrl73g.csv',
                  'https://stsci.box.com/shared/static/4gxmapkhml7lnxsiu9dzto8a7zwnmzd5.csv',
                  'https://stsci.box.com/shared/static/kfaq7jqt4t69vitf1cifk5gurx7lnogn.csv',
                  'https://stsci.box.com/shared/static/xf6rrfnp1jdin94iwhwb47cxoplu3aux.csv',
                  'https://stsci.box.com/shared/static/5zqshpzw748n0doykm7d5cxnlvhue4kk.csv',
                  'https://stsci.box.com/shared/static/x7328lqy8fyg19wswqwq4md4gm398ewi.csv',
                  'https://stsci.box.com/shared/static/8j73qttzj10eu5sct0ds0835uxbxu3s8.csv'
                  ]
    grid_fits_link = ['https://stsci.box.com/shared/static/1suiv6nqbc7yoqutli2q9q98ste31o1y.fits',
                  'https://stsci.box.com/shared/static/faekj3usdme9go3lmynga3uk0oln8v3k.fits',
                  'https://stsci.box.com/shared/static/60sns7ua91ixuz4rddul2ufrmc0pu5yo.fits',
                  'https://stsci.box.com/shared/static/hr113z7lgvggyybh9eygi6nj69gu1gzv.fits',
                  'https://stsci.box.com/shared/static/hvgfnug5xxcepcz083cnrizsukgddttw.fits',
                  'https://stsci.box.com/shared/static/c5gdw6o3b96kaphe07y459zd7ba6590f.fits',
                  'https://stsci.box.com/shared/static/b78ks7cjzenagoznqqrdfoyh6bonw2sy.fits',
                  'https://stsci.box.com/shared/static/lw6gp2s8surgbbtmcnyev673faxqg9h6.fits',
                  'https://stsci.box.com/shared/static/yq6pbvepyt8a420ealg6i111xc7hcty5.fits',
                  'https://stsci.box.com/shared/static/qjuq780xr0ihj9p909wmijwkpclu2njd.fits',
                  'https://stsci.box.com/shared/static/ht6edjsrupwhytwuwa9hjg53dof2zzy0.fits',
                  'https://stsci.box.com/shared/static/n1ng9f4s8s7ps0ah8vp24gk0fzsxp0aj.fits'
                  ]
    if any (ext in model_grid_name for ext in grids):
        match_index = [i for i, item in enumerate(grids) if model_grid_name == item][0]
        url_csv = grid_csv_link[match_index]
        url_fits = grid_fits_link[match_index]
    else:
        raise ValueError(
            'ERROR: Model name not an option. \nCurrent downloadable options: \n \t Zubko-Crich-aringer \n \t Oss-Orich-bb \n \t Oss-Orich-aringer \n \t Crystalline-20-bb \n \t corundum-20-bb \n \t arnold-palmer \n \t big-grains \n \t fifth-iron \n \t one-fifth-carbon')

    # \n Padova options: J400, J1000, H11, R12, R13'

    # Download files
    print(". . . Downloading model: "+model_grid_name+ ' . . .')
    urllib.request.urlretrieve(url_csv, full_path+'/models/' + model_grid_name + '_outputs.csv', reporthook)
    urllib.request.urlretrieve(url_fits, full_path+'/models/' + model_grid_name + '_models.fits', reporthook)
    print("Download Complete!")

if __name__ == '__main__':
    get_models()