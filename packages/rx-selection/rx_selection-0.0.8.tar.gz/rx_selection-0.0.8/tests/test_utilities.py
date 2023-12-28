import selection.utilities as slut
import numpy

from logzero import logger as log
#------------------------------
def test_transform_bdt():
    for bdt in numpy.arange(-1, 1, 0.1):
        val = slut.transform_bdt(bdt)
        log.debug(f'{bdt:<10.3f}{"->"}{val:>10.3f}')
#------------------------------
if __name__ == '__main__':
    test_transform_bdt()

