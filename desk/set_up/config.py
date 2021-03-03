# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
target = dict(distance_in_kpc=50, assumed_gas_to_dust_ratio=200, input_unit="Jy")

path = str(__file__.replace("set_up/config.py", ""))

fitting = dict(
    lum_min=1000,
    lum_max=150000,
    default_grid="Oss-Orich-bb",
    default_wavelength_min=0.01,
    default_wavelength_max=1000,
    default_number_of_times_to_scale_models=50,
)
output = dict(printed_output="True", output_unit="Wm^-2", create_figure="yes")
grids = [
    "Crystalline-20-bb",
    "Oss-Orich-aringer",
    "Oss-Orich-bb",
    "Zubko-Crich-aringer",
    "Zubko-Crich-bb",
    "arnold-palmer",
    "big-grains",
    "corundum-20-bb",
    "fifth-iron",
    "half-iron",
    "one-fifth-carbon",
    "desk-mix",
]
external_grids = [
    "H11-LMC",
    "H11-SMC",
    "J1000-LMC",
    "J1000-SMC",
    "grams-oxygen",
    "grams-carbon",
]
