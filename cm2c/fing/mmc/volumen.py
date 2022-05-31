"""
Biblioteca de métodos Montecarlo
(c) Carlos M. Martinez, marzo-abril 2022
carlos@cagnazzo.uy
"""

import random
import math
import tabulate
import time
from scipy.stats import norm
import functools
from pathos.multiprocessing import ProcessPool as Pool   

random.seed()

_VERSION = "Volúmenes en R^N MMC v0.1.1 - Carlos Martinez marzo 2022"

def version():
    return _VERSION
# end def

def sortearPuntoRN(dim, randfun):
    """
    Seortea un punto en R^N dentro del hiper-cubo [0,1]^N
    randfun es una funcion con la misma API que random.uniform
    """
    punto = []
    for n in range(0, dim):
        # punto.append(random.uniform(0.0, 1.0))
        punto.append(randfun(0.0, 1.0))
    # end for

    return punto
# end fun sortearPuntoRN

# Implemento pseudocodigo Montecarlo

#@functools.lru_cache(maxsize=128)
def MetodoMonteCarlo(N, FVolumen, randfun = random.uniform):
    """
    Implementa el pseudocodigo de MC
    N: cantidad de muestras
    FVolumen: funcion que define el volumen, devuelve 0 si el punto esta fuera, 1 si esta dentro
    """
    random.seed()
    t0 = time.perf_counter()
    S = 0
    for j in range(0, N):
        punto = sortearPuntoRN(6, randfun)
        if FVolumen(punto):
            phi = 1
        else: 
            phi = 0
        S = S + phi
    # end for
    VolR = S / N
    VarVorR = (S/N)*(1-S/N)/(N-1)
    return (VolR, VarVorR, S,  time.perf_counter()-t0)
# end def

# Version paralelizada de Montecarlo
def MetodoMonteCarloParalelo(N, hilos, FVolumen, randfun=random.uniform):
    """
        version paralelizada del montecarlo
        N: numero de muestras
        FVolumen: funcion que implementa el volumen
        randfun: funcion para generar numeros aleatorios con la misma firma que random.uniform()
        hilos: cantidad de hilos en el pool de tareas
    """
    t0 = time.perf_counter()

    args1 = []
    args2 = [] 
    args3 = []
    for x in range(0,hilos):
        args1.append( math.ceil(N/hilos) )
        args2.append(FVolumen)
        args3.append(randfun)
    
    p = Pool(hilos)
    resultados = p.map(MetodoMonteCarlo, args1, args2, args3 )
    #print(resultados)

    # unir los resultados para producir el resultado final
    Stotal = 0
    Ntotal = 0
    for i in range(0, hilos):
        Stotal = Stotal + resultados[i][2]
        Ntotal = Ntotal + math.ceil(N/hilos)
    #
    VolR = Stotal / Ntotal
    VarVorR = (Stotal/Ntotal)*(1-Stotal/Ntotal)/(Ntotal-1)

    return (VolR, VarVorR, Stotal,  time.perf_counter()-t0)
   
# end def

# Formula de Chebyshev
def tamMuestraChebyshev(epsilon, delta):
    """
    Calculo del tamaño de muestra de acuerdo al criterio de Chebyshev.
    epsilon: error deseado 
    delta: intervalo de confianda (1-delta)
    """
    nc =  1.0 / (4.0 * delta * epsilon**2)
    return math.ceil(nc)
#

# Formula Teo Central Limite
def tamMuestraTeoCentralLimite(epsilon, delta):
    """
    Cálculo del tamaño de muestra de acuerdo al Teorema Central del Límite
    epsilon: error deseado 
    delta: intervalo de confianda (1-delta)
    """
    x = norm.ppf(1.0 - delta/2.0)
    # nn = norm.ppf(x)**2
    return math.ceil( ( x/ (2.0*epsilon) ) **2 )
    # return x
# 

# Formula de Hoeffding
def tamMuestraHoeffding(epsilon, delta):
    """
    Estimacion del tamano de muestra segun Hoeffding.
    epsilon: error deseado
    delta: intervalo de confianza
    """
    num = 2 * math.log(2/delta)
    den = 4 * epsilon**2
    return math.ceil(num/den)
# end def

## Calculo de int de confianza por Chebyshev

def intConfianzaChebyshev(S, n, delta):
    """
    Intervalo de confianza segun Chebyshev.
    Parámetros:
      - S: estimador, cantidad de puntos que caen dentro del volumen
      - n: cantidad de replicas (puntos sorteados)
      - delta: margen
    """
    def w1(z, n, beta):
        num = z + beta**2 - beta*math.sqrt( beta**2/4 + z*(n-z)/n )
        den = n + beta**2
        return num / den 
    # end def w1

    def w2(z, n, beta):
        num = z + beta**2 + beta*math.sqrt( beta**2/4 + z*(n-z)/n )
        den = n + beta**2
        return num / den
    # end def w2

    return ( w1(S, n, delta), w2(S, n, delta) )
## end intConfianzaChebyshev

def intConfianzaAC(S, n, delta):
    """
    Intervalo de confianza segun Agresti Coull.
    Parámetros:
      - S: estimador, cantidad de puntos que caen dentro del volumen
      - n: cantidad de replicas (puntos sorteados)
      - delta: margen, si el intervalo de conf es 95%, entonces delta = 0.05
    """
    kappa = norm.ppf(1-delta/2)

    Xg = S + kappa**2/2
    ng = n + kappa**2

    pg = Xg / ng
    qg = 1 - pg

    disc = kappa * math.sqrt(pg*qg)*( 1/math.sqrt(ng))

    return (pg-disc, pg+disc)
## end intConfianzaAC