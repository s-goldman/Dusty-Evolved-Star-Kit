'''
Steve Goldman
Space Telescope Science Institute
May 17, 2018
sgoldman@stsci.edu

This script is for plotting the outputs of the sed_fitting script.
'''

target = dict(
    distance_in_kpc=50,
    assumed_gas_to_dust_ratio=200,
    input_unit='Jy'
)

# model options
# Built-in options: Zubko-Crich-aringer, Oss-Orich-bb, Oss-Orich-aringer, Crystalline-20-bb, corundum-20-bb
# Padova options: J400, J1000, H11, R12, R13
# Grams options:

fitting = dict(
    # model_grid='Zubko-Crich-aringer',
    model_grid='Oss-Orich-bb',
    wavelength_min=0.00001,
    wavelength_max=100,
)
output = dict(
    printed_output='True',

    # output_unit='Wm^-2',
    output_unit='Jy',

    figures_single_multiple_or_none='single'
)
