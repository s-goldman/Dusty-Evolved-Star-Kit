import os
import pdb
import ipdb
import shutil
import sys
import tarfile
import urllib
from fnmatch import fnmatch

import numpy as np
from astropy.table import vstack, Table, Column
from tqdm import tqdm


def get_models(model_grid_name):
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.0f%% %*d / %d KB" % (
                percent,
                len(str(totalsize)),
                readsofar / 1e3,
                totalsize / 1e3,
            )
            sys.stderr.write(s)
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))

    full_path = str(__file__.replace("get_remote_models.py", ""))
    grids = [
        "Crystalline-20-bb",
        "H11-SMC",
        "H11-LMC",
        "J1000-SMC",
        "J1000-LMC",
        "Oss-Orich-aringer",
        "Oss-Orich-bb",
        "Zubko-Crich-aringer",
        "Zubko-Crich-bb",
        "arnold-palmer",
        "big-grain",
        "corundum-20-bb",
        "fifth-iron",
        "half-iron",
        "one-fifth-carbon",
        "grams-oxygen",
        "grams-carbon",
    ]
    grid_csv_link = [
        "https://stsci.box.com/shared/static/jxtabj6h5zi7a8ggb0mbtag3v6b4b9i7.csv",
        "https://stsci.box.com/shared/static/z0hnvo0hz0qxcwlcvbmf01avdjlhewah.csv",
        "https://stsci.box.com/shared/static/j7f01dwbsbluq4htdwlsx3v0jknye883.csv",
        "https://stsci.box.com/shared/static/o6dp1cyj86jw2ifuuco983kgb2uf16sf.csv",
        "https://stsci.box.com/shared/static/fuhrcgo4vh4m7ca121p1f0vuss4vszcz.csv",
        "https://stsci.box.com/shared/static/he92pt1yov18x6ska5f4f4q94gal6tr5.csv",
        "https://stsci.box.com/shared/static/pnljezbu8c7rcyorb27yh6hylk5wy2fs.csv",
        "https://stsci.box.com/shared/static/x9fg8lacbbiye591tz723ilcqgcomyjh.csv",
        "https://stsci.box.com/shared/static/4b9rc9zl110khexeuo8thb8r58mrl73g.csv",
        "https://stsci.box.com/shared/static/4gxmapkhml7lnxsiu9dzto8a7zwnmzd5.csv",
        "https://stsci.box.com/shared/static/kfaq7jqt4t69vitf1cifk5gurx7lnogn.csv",
        "https://stsci.box.com/shared/static/xf6rrfnp1jdin94iwhwb47cxoplu3aux.csv",
        "https://stsci.box.com/shared/static/5zqshpzw748n0doykm7d5cxnlvhue4kk.csv",
        "https://stsci.box.com/shared/static/x7328lqy8fyg19wswqwq4md4gm398ewi.csv",
        "https://stsci.box.com/shared/static/8j73qttzj10eu5sct0ds0835uxbxu3s8.csv",
        "https://stsci.box.com/shared/static/ldocm4yto4vtxfcg21o23a8uilb3a3do.csv",
        "https://stsci.box.com/shared/static/iy6dsqrnhi96ecnlsozo1ljr5g8b1jwx.csv",
    ]
    grid_fits_link = [
        "https://stsci.box.com/shared/static/1suiv6nqbc7yoqutli2q9q98ste31o1y.fits",
        "https://stsci.box.com/shared/static/bq384o6m1xm41bkx7s8oloohqkd87hy8.fits",
        "https://stsci.box.com/shared/static/faekj3usdme9go3lmynga3uk0oln8v3k.fits",
        "https://stsci.box.com/shared/static/w0e3f1a0r886u17vjosk8lvqrnvnw6ce.fits",
        "https://stsci.box.com/shared/static/e0nvigaed722a67043rvmqhjzkonttp4.fits",
        "https://stsci.box.com/shared/static/60sns7ua91ixuz4rddul2ufrmc0pu5yo.fits",
        "https://stsci.box.com/shared/static/hr113z7lgvggyybh9eygi6nj69gu1gzv.fits",
        "https://stsci.box.com/shared/static/hvgfnug5xxcepcz083cnrizsukgddttw.fits",
        "https://stsci.box.com/shared/static/c5gdw6o3b96kaphe07y459zd7ba6590f.fits",
        "https://stsci.box.com/shared/static/b78ks7cjzenagoznqqrdfoyh6bonw2sy.fits",
        "https://stsci.box.com/shared/static/lw6gp2s8surgbbtmcnyev673faxqg9h6.fits",
        "https://stsci.box.com/shared/static/yq6pbvepyt8a420ealg6i111xc7hcty5.fits",
        "https://stsci.box.com/shared/static/qjuq780xr0ihj9p909wmijwkpclu2njd.fits",
        "https://stsci.box.com/shared/static/ht6edjsrupwhytwuwa9hjg53dof2zzy0.fits",
        "https://stsci.box.com/shared/static/n1ng9f4s8s7ps0ah8vp24gk0fzsxp0aj.fits",
        "https://stsci.box.com/shared/static/l1qayndbz40lwewvlpg1qxu22rs9f9xu.fits",
        "https://stsci.box.com/shared/static/jho46vam6d0k9jwg78gxx4eh7emwx4oz.fits",
    ]
    if any(ext in model_grid_name for ext in grids):
        match_index = [i for i, item in enumerate(grids) if model_grid_name == item][0]
        url_csv = grid_csv_link[match_index]
        url_fits = grid_fits_link[match_index]
    else:
        raise ValueError(
            "ERROR: Model name not an option. \nCurrent downloadable options: \n \t Zubko-Crich-aringer \n \t Oss-Orich-bb \n \t Oss-Orich-aringer \n \t Crystalline-20-bb \n \t corundum-20-bb \n \t arnold-palmer \n \t big-grains \n \t fifth-iron \n \t one-fifth-carbon"
        )

    # \n Padova options: J400, J1000, H11, R12, R13'

    # Download files
    print(". . . Downloading model: " + model_grid_name + " . . .")
    urllib.request.urlretrieve(
        url_csv, full_path + "/models/" + model_grid_name + "_outputs.csv"
    )
    urllib.request.urlretrieve(
        url_fits, full_path + "/models/" + model_grid_name + "_models.fits", reporthook
    )
    print("Download Complete!")


if __name__ == "__main__":
    get_models()
