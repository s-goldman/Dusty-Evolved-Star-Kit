import ipdb
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from astropy.table import Table, Column, vstack, hstack

__all__ = ["users"]


class users(object):
    """docstring for user."""

    def __init__(self, source, distance, grid):
        self.source = source
        self.distance = distance
        self.grid = grid
        self.target = dict(
            distance_in_kpc=50, assumed_gas_to_dust_ratio=200, input_unit="Jy"
        )
