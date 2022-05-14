"""
Montecarlo para problemas de conteo.
(c) Carlos M. martinez, mayo 2022
"""

import random
import math
import tabulate
import time
from scipy.stats import norm
import functools
from cm2c.fing.mmc.utils import sortearPuntoRN
from pathos.multiprocessing import ProcessPool as Pool   

_VERSION = "Problemas de conteo MMC v0.1.1 - Carlos Martinez mayo 2022"


def version():
    return _VERSION
# end def
