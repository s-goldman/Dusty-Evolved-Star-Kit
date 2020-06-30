# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
import os
import sys
import ipdb
import numpy as np
import h5py
import urllib
from astropy.table import Table
from desk.set_up import config


def read_hdf5(filename, testing):
    f = h5py.File(filename, "r")
    key = list(f.keys())[0]
    if testing == True:
        data = list(f[key][1:4])
    else:
        data = list(f[key])
    f.close()
    out = Table(np.array(data))
    return out


def get_remote_models(model_grid_name):
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

    grids = config.grids
    models = {
        "arnold-palmer": "https://stsci.box.com/shared/static/5uw23xy6dzrjeb012tw8250r6zfquq1d.hdf5",
        "big-grains": "https://stsci.box.com/shared/static/iwd1wi62rosqhxps2m5ebl8jmv7edx1z.hdf5",
        "corundum-20-bb": "https://stsci.box.com/shared/static/y4ayifjft106j9qbnrc1nl7gly9ajsof.hdf5",
        "Crystalline-20-bb": "https://stsci.box.com/shared/static/9dnzbkhlfvwsfoocelkfop49wpo3ahig.hdf5",
        "fifth-iron": "https://stsci.box.com/shared/static/xtqkm8htmr3xe1n0mcl2p27smtan93a2.hdf5",
        "grams-carbon": "https://stsci.box.com/shared/static/bb8em53lug4a3alggndcqro6cxxv4rkk.hdf5",
        "grams-oxygen": "https://stsci.box.com/shared/static/12oqk52b52sghzo9zb6smxcvwm0zsxqf.hdf5",
        "H11-LMC": "https://stsci.box.com/shared/static/hgnmd8jwem3pm3ewjazdpssu9fst60hl.hdf5",
        "H11-SMC": "https://stsci.box.com/shared/static/ofes4gsscf0y8g8fu72alu5cx40lry58.hdf5",
        "half-iron": "https://stsci.box.com/shared/static/q5j9ey5ci5vtu2nnl6qf76entxt3xsr5.hdf5",
        "J1000-LMC": "https://stsci.box.com/shared/static/3ed8e7ulpu30cbyri3ex7m08g5jztk6m.hdf5",
        "J1000-SMC": "https://stsci.box.com/shared/static/a7j1z18sz4mr3k2dxqj5cob6wqutfcad.hdf5",
        "one-fifth-carbon": "https://stsci.box.com/shared/static/olpt7phvjd4kin6wn0w9y1wez9037f73.hdf5",
        "Oss-Orich-aringer": "https://stsci.box.com/shared/static/xytr8t139h8zuanwtf773a8bzt32bxcc.hdf5",
        "Oss-Orich-bb": "https://stsci.box.com/shared/static/arczjrc25xi601rlwxco08b14vabpp52.hdf5",
        "Zubko-Crich-aringer": "https://stsci.box.com/shared/static/yq8vbohgybuo7nmkwu0w535q6tjeyw1v.hdf5",
        "Zubko-Crich-bb": "https://stsci.box.com/shared/static/4ocskl59q8tvrhxbpcvpo26qm1wy9ytg.hdf5",
    }
    outputs = {
        "arnold-palmer": "https://stsci.box.com/shared/static/bc8up4ra3b1a8crpebnjvhl9bxnhws52.hdf5",
        "big-grains": "https://stsci.box.com/shared/static/apiwiek17yjjey6hx7b87w5oeupnxbq7.hdf5",
        "corundum-20-bb": "https://stsci.box.com/shared/static/o6bx04qfbs4nof93e16jr0gl0lt04vmi.hdf5",
        "Crystalline-20-bb": "https://stsci.box.com/shared/static/aee6evhqfp6m8p8wsqnj6finsxj022bq.hdf5",
        "fifth-iron": "https://stsci.box.com/shared/static/4jkhznyw1566wprc4w3og0ps2e6pyk60.hdf5",
        "grams-carbon": "https://stsci.box.com/shared/static/m0gc3eils06b0zcy1t75l8x6h8ftpij1.hdf5",
        "grams-oxygen": "https://stsci.box.com/shared/static/mc6h7hhew918du9nudez1w2obja1ydqy.hdf5",
        "H11-LMC": "https://stsci.box.com/shared/static/ndzqw7s6yr8kmmkq71hnvi10gb42fx6k.hdf5",
        "H11-SMC": "https://stsci.box.com/shared/static/9q7yh6mawezxbt5ipvmqrui2r0gld4f0.hdf5",
        "half-iron": "https://stsci.box.com/shared/static/r26hehfxy92cb5cweihkl9159xr9a7fe.hdf5",
        "J1000-LMC": "https://stsci.box.com/shared/static/242covljjj7iri59tjsd9ah80rbgsptg.hdf5",
        "J1000-SMC": "https://stsci.box.com/shared/static/ampoqu2a9azpmrql09b51lv8rch2ubmb.hdf5",
        "one-fifth-carbon": "https://stsci.box.com/shared/static/vfg9ab4gs1y5zsvmrd8qd1g3xhfno4nz.hdf5",
        "Oss-Orich-aringer": "https://stsci.box.com/shared/static/t75dvs50380lpffsjh2f4yjrvgoi8r4y.hdf5",
        "Oss-Orich-bb": "https://stsci.box.com/shared/static/ov83sjmx69ddgy8bahg5p8yu2c2gxfqo.hdf5",
        "Zubko-Crich-aringer": "https://stsci.box.com/shared/static/0nrjesla9jgxh8ioatnmrmrc5tkcf3pf.hdf5",
        "Zubko-Crich-bb": "https://stsci.box.com/shared/static/d0651w7ztavoiir7341lda8xzbwrfq9g.hdf5",
    }
    # grid_csv_link = [
    #     "https://stsci.box.com/shared/static/jxtabj6h5zi7a8ggb0mbtag3v6b4b9i7.csv",
    #     "https://stsci.box.com/shared/static/z0hnvo0hz0qxcwlcvbmf01avdjlhewah.csv",
    #     "https://stsci.box.com/shared/static/j7f01dwbsbluq4htdwlsx3v0jknye883.csv",
    #     "https://stsci.box.com/shared/static/o6dp1cyj86jw2ifuuco983kgb2uf16sf.csv",
    #     "https://stsci.box.com/shared/static/fuhrcgo4vh4m7ca121p1f0vuss4vszcz.csv",
    #     "https://stsci.box.com/shared/static/he92pt1yov18x6ska5f4f4q94gal6tr5.csv",
    #     "https://stsci.box.com/shared/static/pnljezbu8c7rcyorb27yh6hylk5wy2fs.csv",
    #     "https://stsci.box.com/shared/static/x9fg8lacbbiye591tz723ilcqgcomyjh.csv",
    #     "https://stsci.box.com/shared/static/4b9rc9zl110khexeuo8thb8r58mrl73g.csv",
    #     "https://stsci.box.com/shared/static/4gxmapkhml7lnxsiu9dzto8a7zwnmzd5.csv",
    #     "https://stsci.box.com/shared/static/kfaq7jqt4t69vitf1cifk5gurx7lnogn.csv",
    #     "https://stsci.box.com/shared/static/xf6rrfnp1jdin94iwhwb47cxoplu3aux.csv",
    #     "https://stsci.box.com/shared/static/5zqshpzw748n0doykm7d5cxnlvhue4kk.csv",
    #     "https://stsci.box.com/shared/static/x7328lqy8fyg19wswqwq4md4gm398ewi.csv",
    #     "https://stsci.box.com/shared/static/8j73qttzj10eu5sct0ds0835uxbxu3s8.csv",
    #     "https://stsci.box.com/shared/static/ldocm4yto4vtxfcg21o23a8uilb3a3do.csv",
    #     "https://stsci.box.com/shared/static/iy6dsqrnhi96ecnlsozo1ljr5g8b1jwx.csv",
    # ]
    # grid_fits_link = [
    #     "https://stsci.box.com/shared/static/1suiv6nqbc7yoqutli2q9q98ste31o1y.fits",
    #     "https://stsci.box.com/shared/static/bq384o6m1xm41bkx7s8oloohqkd87hy8.fits",
    #     "https://stsci.box.com/shared/static/faekj3usdme9go3lmynga3uk0oln8v3k.fits",
    #     "https://stsci.box.com/shared/static/w0e3f1a0r886u17vjosk8lvqrnvnw6ce.fits",
    #     "https://stsci.box.com/shared/static/e0nvigaed722a67043rvmqhjzkonttp4.fits",
    #     "https://stsci.box.com/shared/static/60sns7ua91ixuz4rddul2ufrmc0pu5yo.fits",
    #     "https://stsci.box.com/shared/static/hr113z7lgvggyybh9eygi6nj69gu1gzv.fits",
    #     "https://stsci.box.com/shared/static/hvgfnug5xxcepcz083cnrizsukgddttw.fits",
    #     "https://stsci.box.com/shared/static/c5gdw6o3b96kaphe07y459zd7ba6590f.fits",
    #     "https://stsci.box.com/shared/static/b78ks7cjzenagoznqqrdfoyh6bonw2sy.fits",
    #     "https://stsci.box.com/shared/static/lw6gp2s8surgbbtmcnyev673faxqg9h6.fits",
    #     "https://stsci.box.com/shared/static/yq6pbvepyt8a420ealg6i111xc7hcty5.fits",
    #     "https://stsci.box.com/shared/static/qjuq780xr0ihj9p909wmijwkpclu2njd.fits",
    #     "https://stsci.box.com/shared/static/ht6edjsrupwhytwuwa9hjg53dof2zzy0.fits",
    #     "https://stsci.box.com/shared/static/n1ng9f4s8s7ps0ah8vp24gk0fzsxp0aj.fits",
    #     "https://stsci.box.com/shared/static/l1qayndbz40lwewvlpg1qxu22rs9f9xu.fits",
    #     "https://stsci.box.com/shared/static/jho46vam6d0k9jwg78gxx4eh7emwx4oz.fits",
    # ]
    if model_grid_name in models:
        url_outputs = outputs[model_grid_name]
        url_models = models[model_grid_name]
    else:
        raise ValueError(
            "ERROR: Model name not an option. \nCurrent downloadable options: \n \t Zubko-Crich-aringer \n \t Oss-Orich-bb \n \t Oss-Orich-aringer \n \t Crystalline-20-bb \n \t corundum-20-bb \n \t arnold-palmer \n \t big-grains \n \t fifth-iron \n \t one-fifth-carbon"
        )

    # \n Padova options: J400, J1000, H11, R12, R13'

    # Download files
    print(". . . Downloading model: " + model_grid_name + " . . .")
    urllib.request.urlretrieve(
        url_outputs, config.path + "/models/" + model_grid_name + "_outputs.hdf5"
    )
    urllib.request.urlretrieve(
        url_models,
        config.path + "/models/" + model_grid_name + "_models.hdf5",
        reporthook,
    )
    print("Download Complete!")


def check_models(model_grid):

    """
    Checks if model grids are available and returns the full path to the model.
    If the model is not downloaded, it is downloaded via Box.

    Parameters
    ----------
    model_grid : str
        Name of model grid to use.

    Returns
    -------
    outputs_file: str
        The full path/name of the model outputs file.
    models_file: str
        The full path/name of the model grid file.

    """

    outputs_file = config.path + "models/" + model_grid + "_outputs.hdf5"
    models_file = config.path + "models/" + model_grid + "_models.hdf5"

    # Checks if grid is available
    if os.path.isfile(outputs_file) and os.path.isfile(models_file):
        print("\nYou already have the grid!\n")
    else:
        # asks if you want to download the models
        print("Models not found locally")
        get_remote_models(model_grid)
    return (outputs_file, models_file)


def get_model_grid(grid, testing):
    """
    Gets the real model grid name if the defaults were chosen,and runs check_models.

    Parameters
    ----------
    grid : str
        Model grid name.

    Returns
    -------
    grid_dusty : 2 column astropy table with array of wavelengths and array of
    fluxes in each column of each row
        The (intial) model grid wavelengths and fluxes. This is not the full model
        grid with appended scaled models.

    grid_outputs : astropy table
        The model grid parameters corresponding to the grid_dusty model grids
    """

    # User input for models
    if grid == "carbon":
        model_grid = "Zubko-Crich-bb"
    elif grid == "oxygen":
        model_grid = "Oss-Orich-bb"
    else:
        if grid in config.grids:
            model_grid = grid
        else:
            raise ValueError(
                "\n\nUnknown grid. Please make another model selection.\n\n To see options use: desk grids\n"
            )
    outputs_file_name, models_file_name = check_models(model_grid)

    grid_dusty = read_hdf5(models_file_name, testing)
    grid_outputs = read_hdf5(outputs_file_name, testing)

    return grid_dusty, grid_outputs
