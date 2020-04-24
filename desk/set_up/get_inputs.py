# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
__all__ = ["users"]


class users(object):

    """Docstring for users."""

    def __init__(self, source, distance, grid):
        # Initialize user-inputted data
        self.source = source
        self.distance = distance
        self.grid = grid
        self.target = dict(
            distance_in_kpc=50, assumed_gas_to_dust_ratio=200, input_unit="Jy"
        )
