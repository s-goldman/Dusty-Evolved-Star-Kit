try:  # python 3
    from io import BytesIO
    from http.client import HTTPConnection
except ImportError:  # python 2
    from StringIO import StringIO as BytesIO
    from httplib import HTTPConnection

from astropy.table import Table


def query_sed(pos, radius):
    """Query VizieR Photometry (tool developed by Morgan Fouesneau)
    The VizieR photometry tool extracts photometry points around a given position
    or object name from photometry-enabled catalogs in VizieR.

    The VizieR photometry tool is developed by Anne-Camille Simon and Thomas Boch
    .. url:: http://vizier.u-strasbg.fr/vizier/sed/doc/

    Parameters
    ----------
    pos: tuple or str
        position tuple or object name
    radius: float
        position matching in arseconds.

    Returns
    -------
    table: astropy.Table
        VO table returned by the Vizier service.

    >>> query_sed((1.286804, 67.840))
    >>> query_sed("HD1")
    """
    try:
        ra, dec = pos
        target = "{0:f},{1:f}".format(ra, dec)
    except:
        target = pos

    url = "http:///viz-bin/sed?-c={target:s}&-c.rs={radius:f}"
    host = "vizier.u-strasbg.fr"
    port = 80
    path = "/viz-bin/sed?-c={target:s}&-c.rs={radius:f}".format(
        target=target, radius=radius
    )
    connection = HTTPConnection(host, port)
    connection.request("GET", path)
    response = connection.getresponse()

    table = Table.read(BytesIO(response.read()), format="votable")
    return table
