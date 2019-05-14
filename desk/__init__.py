# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This packages contains python packages that are bundled with the package but
are external to it, and hence are developed in a separate source tree. Note
that this package is distinct from the /cextern directory of the source code
distribution, as that directory only contains C extension code.
"""

# -*- coding: utf-8 -*-

"""Top-level package for Dusty-Evolved-Star-Kit."""

__author__ = """Steven R. Goldman"""
__email__ = 'sgoldman@stsci.edu'
__version__ = '1.4.7'

import desk.sed_fit
import desk.plotting_seds
import desk.config
import desk.get_padova
import desk.remove_old_files
import desk.parameter_ranges