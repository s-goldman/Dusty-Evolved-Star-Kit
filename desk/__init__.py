# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
The DESK contains python packages that are bundled with the package but
are external to it, and hence are developed in a separate source tree. Note
that this package is distinct from the /cextern directory of the source code
distribution, as that directory only contains C extension code.
"""

# -*- coding: utf-8 -*-

# Top-level package for Dusty-Evolved-Star-Kit.

__author__ = "Steven R. Goldman"
__email__ = "sgoldman@stsci.edu"
__title__ = "DESK"
__version__ = "1.6.24"
__repository__ = "https://github.com/s-goldman/Dusty-Evolved-Star-Kit"
__date_published = "2020-07-07"
__licence__ = "BSD"
__keywords__ = (
    "Asymptotic giant branch stars",
    "Circumstellar dust",
    "Stellar mass loss",
    "Late stellar evolution",
    "Mira variable stars",
    "Extreme carbon stars",
)

from desk import fitting, outputs, probabilities, set_up
