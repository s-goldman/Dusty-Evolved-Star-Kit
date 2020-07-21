# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""

"""

# -*- coding: utf-8 -*-

# Top-level package for Dusty-Evolved-Star-Kit.

__author__ = "Steven R. Goldman"
__email__ = "sgoldman@stsci.edu"
__title__ = "DESK"
__version__ = "1.6.25"
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

# # to import all submodules
# import pkgutil
#
# __all__ = []
# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     __all__.append(module_name)
#     _module = loader.find_module(module_name).load_module(module_name)
#     globals()[module_name] = _module
