import urllib
import tarfile
import shutil
import pdb
import os
from tqdm import tqdm
import numpy as np
from astropy.table import vstack, Table, Column


def get_model(model_grid_name):
    if model_grid_name == 'J400':
        url = 'http://starkey.astro.unipd.it/documents/10184/1932584/SMC_tables_J400.dat/f0107070-99b4-4f5a-b46c-f443f8b9e04f'
        url_tar = 'http://starkey.astro.unipd.it/documents/10184/1932584/J400.tar.gz/c1b50228-5c39-477d-8b83-b83a2f91c717'

    elif model_grid_name == 'J1000':
        url = 'http://starkey.astro.unipd.it/documents/10184/1932584/SMC_tables_J1000.dat/a84fed3a-46b4-4f74-a236-88e32225a6bc'
        url_tar = 'http://starkey.astro.unipd.it/documents/10184/1932584/J1000.tar.gz/46e1d848-3913-4052-a903-7ab64f17117c'

    elif model_grid_name == 'H11':
        url = "http://starkey.astro.unipd.it/documents/10184/1932584/SMC_tables_H11.dat/07c719d1-8b6c-4274-8e33-a6a79ec3d26c"
        url_tar = 'http://starkey.astro.unipd.it/documents/10184/1932584/H11.tar.gz/190bff99-74ef-472d-832e-74864e5799ba'

    elif model_grid_name == 'R12':
        url = "http://starkey.astro.unipd.it/documents/10184/1932584/SMC_tables_R12.dat/ba7b6583-47f9-43f6-bbcf-def477dbf699"
        url_tar = 'http://starkey.astro.unipd.it/documents/10184/1932584/R12.tar.gz/2fb77bf0-79d7-4867-b908-c55d67b0b6f6'

    elif model_grid_name == 'R13':
        url = "http://starkey.astro.unipd.it/documents/10184/1932584/SMC_tables_R13.dat/9a394ad3-25c3-43bf-847d-436760b80df8"
        url_tar = 'http://starkey.astro.unipd.it/documents/10184/1932584/R13.tar.gz/3732a57e-15b3-47a3-8869-bd01ef43d090'


    else:
        raise ValueError(
            'Model name not an option. \n Built-in options: Zubko-Crich-aringer, Oss-Orich-bb, Oss-Orich-aringer, Crystalline-20-bb, corundum-20-bb \n Padova options: J400, J1000, H11, R12, R13')

    # Download files
    print("Downloading")
    urllib.request.urlretrieve(url, 'model.dat')
    urllib.request.urlretrieve(url_tar, 'model_directory.tar.gz')
    print("Download Complete!")

    # Extract Tar file
    print("Extracting")
    tar = tarfile.open('model_directory.tar.gz', "r:gz")
    tar.extractall()
    tar.close()

    # Compile spectra into fits file
    output_files = os.listdir(model_grid_name)
    dusty_spectra = []
    print('Compiling spectra into single fits file')
    for item in tqdm(output_files):
        new_row = np.loadtxt(model_grid_name + '/' + item, skiprows=1, usecols=[0, 1], unpack=True)
        dusty_spectra.append(new_row)
    dusty_spectra_output = Table(np.array(dusty_spectra))
    dusty_spectra_output.write('../models/' + model_grid_name + '_models.fits', format='fits', overwrite=True)

    # reorder parameter file
    p_file = Table.read('model.dat', format='csv', delimiter=' ')
    p_file.rename_column('#dmdt', 'mdot')
    p_file.rename_column('Tinn', 'tinner')
    p_file.rename_column('Teff', 'teff')
    p_file.rename_column('tau10', 'odep')
    grid_name = Column([model_grid_name] * len(p_file), name='grid_name')
    output_array = Table(
        [grid_name, p_file['teff'], p_file['tinner'], p_file['M'], p_file['vexp'], p_file['mdot'], p_file['odep']])
    output_array.write('../models/' + model_grid_name + '_outputs.csv', format='csv', overwrite=True)

    # remove temporary files
    # os.remove('model.dat')
    # os.remove('model_directory.tar.gz')
    # shutil.rmtree(model_grid_name)
