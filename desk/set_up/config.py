# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu

target = dict(distance_in_kpc=50, assumed_gas_to_dust_ratio=200, input_unit="Jy")

path = str(__file__.replace("set_up/config.py", ""))

fitting = dict(
    model_grid="Zubko-Crich-bb",
    wavelength_min=0.00001,
    wavelength_max=100,
    lum_min=1000,
    lum_max=150000,
    number_of_tries=400,
)
output = dict(
    printed_output="True",
    output_unit="Wm^-2",
    # output_unit='Jy',
    create_figure="yes",
)
grids = [
    "Crystalline-20-bb",
    "H11-LMC",
    "H11-SMC",
    "J1000-LMC",
    "J1000-SMC",
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
