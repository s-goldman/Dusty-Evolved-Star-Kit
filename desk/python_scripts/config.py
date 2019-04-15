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

# model options
# Built-in options: Zubko-Crich-aringer, Oss-Orich-bb, Oss-Orich-aringer, Crystalline-20-bb, corundum-20-bb
# Padova options: J400, J1000, H11, R12, R13

fitting = dict(
    model_grid='Zubko-Crich-aringer_outputs',
    # model_grid='Oss-Orich-aringer',
    wavelength_min=0.01,
    wavelength_max=25,
    min_norm=1e-16,
    max_norm=1e-12,
    ntrials=2000
)
output = dict(
    printed_output='True',

    # output_unit='Wm^-2',
    output_unit='Jy',

    figures_single_multiple_or_none='multiple'
)
