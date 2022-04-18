"""
Utils para Montecarlo
(c) Carlos Martinez, abril 2022
"""

import random
import time

class timeit:
    """
    Medir tiempos
    """
    def __init__(self):
        self._t0 = time.perf_counter()
        self._laps = []

    def lap(self):
        t1 = time.perf_counter()
        _lap = t1 - self._t0
        self._t0 = t1
        self._laps.append(_lap)
        return _lap

    def reset(self):
        self._t0 = time.perf_counter()
# end class timeit

# def timeit(method):
#     """
#     Medición de ejecución, para usar como decorador
#     method: es una función a medir su tiempo
#     imprime el resultado
#     """
#     def timed(*args, **kw):
#         ts = time.time()
#         result = method(*args, **kw)
#         te = time.time()
#         if 'log_time' in kw:
#             name = kw.get('log_name', method.__name__.upper())
#             kw['log_time'][name] = int((te - ts) * 1000)
#         else:
#             print ('%r  %2.2f ms' % \
#                   (method.__name__, (te - ts) * 1000) ) 
#         return result
#     return timed

def sortearPuntoRN(dim=2):
    """
    Seortea un punto en R^N dentro del hiper-cubo [0,1]^N
    """
    punto = []
    for n in range(0, dim):
        punto.append(random.uniform(0.0, 1.0))
    # end for

    return punto
# end fun sortearPuntoRN

random.seed()

if __name__ == "__main__":
    print("Es una biblioteca, no es para correr directamente")