# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu
class fitting_parameters(object):
    """Initializes fitting paramters."""

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
    ):
        """Initializes fitting paramters.

        Parameters
        ----------
        file_names : array of strings
            Array of the locations of target files.
            e.g.) array(['desk/put_target_data_here/MSX_LMC_807.csv'])
        source : str
            input source string.
            e.g.) 'desk/put_target_data_here/'
        distance : float
            Distance to source in kpc.
        grid : str
            Name of model grid to be used.
        n : int
            Number of times to scale model grid between config.fitting.lum_min
            and config.fitting.lum_min. A value to alter the density of the grid.
        model_wavelength_grid : array
            A 1-D np.array of the wavelengths of the model grid.
        full_model_grid : astropy table
            1-Column astropy table with arrays of model grid fluxes (wm-2) as rows.
        full_outputs : astropy table
            Model outputs as 2D astropy table.
        min_wavelength : float
            Minimum wavelength to fit (um).
        max_wavelength : float
            Maximum wavelength to fit (um).
        bayesian_fit : bool
            Flag for baysian fitting.
        testing : bool
            Flag for testing, used to limit size of model grid.

        Returns
        -------
        class variable
            Class with all fitting parameters.

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
