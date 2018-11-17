'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
'''

target = dict(
    distance_in_kpc=50,
    assumed_gas_to_dust_ratio=400,
    input_unit='Jy'
)
fitting = dict(
    model_grid='Crystalline-20-bb',
    wavelength_min=0.01,
    wavelength_max=25,
    min_norm=1e-16,
    max_norm=1e-12,
    ntrials=2000
)
output = dict(
    printed_output='True',

    output_unit='Wm^-2',
    # output_unit = 'Jy',

    single_or_mulitple_figures='single'
)
