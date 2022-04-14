"""
Utils para Montecarlo
(c) Carlos Martinez, abril 2022
"""

import random

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