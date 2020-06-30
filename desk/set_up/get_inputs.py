# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
__all__ = ["users"]


class users(object):
    """Initializes user inputs."""

    def __init__(
        self,
        file_names,
        source,
        distance,
        grid,
        n,
        model_wavelength_grid,
        full_model_grid,
        full_outputs,
        min_wavelength,
        max_wavelength,
        bayesian_fit,
        testing,
        # counter,
    ):
        """
        Initializes user inputs.

        Parameters
        ----------
        source : str
            user input source directory/file.
        distance : int
            user input distance in kpc.
        grid : str
            user input grid name to use

        """
        # Initialize user-inputted data
        self.file_names = file_names
        self.source = source
        self.distance = distance
        self.grid = grid
        self.n = n
        self.model_wavelength_grid = model_wavelength_grid
        self.full_model_grid = full_model_grid
        self.full_outputs = full_outputs
        self.min_wavelength = min_wavelength
        self.max_wavelength = max_wavelength
        self.bayesian_fit = bayesian_fit
        self.testing = testing
        # self.counter = counter
