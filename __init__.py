# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This packages contains python packages that are bundled with the package but
are external to it, and hence are developed in a separate source tree. Note
that this package is distinct from the /cextern directory of the source code
distribution, as that directory only contains C extension code.
"""

from desk import config
from desk import get_padova
from desk import plotting_seds
from desk import remove_old_files
from desk import sed_fit