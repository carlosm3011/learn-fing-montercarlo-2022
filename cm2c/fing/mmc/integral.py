"""
Montecarlo para integrales.
(c) Carlos M. martinez, marzo-abril 2022
"""

import random
import math
import tabulate
import time
from scipy.stats import norm
import functools
from cm2c.fing.mmc.utils import sortearPuntoRN
from pathos.multiprocessing import ProcessPool as Pool   

_VERSION = "Integracion MMC v0.1 - Carlos Martinez abril 2022"

def version():
    return _VERSION
# end def

def integracionMonteCarlo(Phi, dim, n, delta):
    """
    Integracion por Montecarlo.
    Phi: funcion a integrar
    n: tamaño de la muestra (cantidad de iteraciones)
    dim: dimensionalidad del problema
    delta: intervalo de confianza

    Resultado: (estimacion valor integral, estimacion varianza)
    """
    S = 0
    T = 0
    for j in range(1, n+1):
        # sortear X({j} con distribución uniforme en R(n)
        Xj = sortearPuntoRN(dim)
        # print(Xj, Phi(Xj))
        if j>1:
            T = T + (1-1/j)*(Phi(Xj)-S/(j-1))**2
            S = S + Phi(Xj)
    # end for
    estimZ = S / n
    estimSigma2 = T / (n-1)
    estimVar = estimSigma2 / n

    return (estimZ, estimVar)
## end def

if __name__ == "__main__":
    print("Es una biblioteca, no es para correr directamente")