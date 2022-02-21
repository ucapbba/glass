# author: Nicolas Tessore <n.tessore@ucl.ac.uk>
# license: MIT
'''module for output'''

import logging
from itertools import count
import fitsio

from ._generator import generator


log = logging.getLogger('glass.output')


@generator('zmin, zmax, maps')
def write_map(filename, names, *, clobber=False):
    '''write map to FITS file'''

    log.info('filename: %s', filename)

    fits = fitsio.FITS(filename, 'rw', clobber=clobber)

    log.info('fields: %s', ', '.join(names))

    for i in count(1):
        try:
            zmin, zmax, maps = yield
        except GeneratorExit:
            break

        extname = f'MAP{i}'

        header = [
            {'name': 'ZMIN', 'value': zmin, 'comment': 'lower redshift bound'},
            {'name': 'ZMAX', 'value': zmax, 'comment': 'upper redshift bound'},
        ]

        fits.write_table(maps, names=names, extname=extname, header=header)

    fits.close()

    log.info('file closed')