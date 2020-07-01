# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
The DESK contains python packages that are bundled with the package but
are external to it, and hence are developed in a separate source tree. Note
that this package is distinct from the /cextern directory of the source code
distribution, as that directory only contains C extension code.
"""

# -*- coding: utf-8 -*-

# Top-level package for Dusty-Evolved-Star-Kit.

__author__ = """Steven R. Goldman"""
__email__ = "sgoldman@stsci.edu"
__version__ = "1.6.20"

from desk import fitting, outputs, probabilities, set_up
