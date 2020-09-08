# Steve Goldman, Space Telescope Science Institute, sgoldman@stsci.edu


class Fitting_Range_Error(ValueError):
    """Specific error message for bad input range"""

    pass


class BadFilenameError(ValueError):
    """Specific error message for bad input source (filename)"""

    pass


class BadSourceDirectoryError(ValueError):
    """Specific error message for bad input source (directory)"""

    pass
