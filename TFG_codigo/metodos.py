import time
from typing import Callable, Dict, Any
import numpy as np

TOLF = 1e-14
TOLX = 1e-14
MAX_ITER = 100

def metodo1(metodo: str, f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float],
            x0: float, tolx: float = TOLX, tolf: float = TOLF, max_iter: int=MAX_ITER) -> Dict[str, Any]:
    
    v_inicial = x0    
    errores, raices, evaluaciones, conv = [np.nan,], [x0,],  [f(x0),], False
    t0 = time.perf_counter()
    i = 0

    mensaje_final = "Diverge"

    while i < max_iter and not conv:
        try:
            x1 = metodo(f,df,ddf,x0)
            fx1 = f(x1)
            raices.append(x1)
            evaluaciones.append(fx1)
            errores.append(abs(x1 - x0))

            if errores[-1] < tolx and abs(fx1) < tolf:
                conv = True
                mensaje_final = "Converge"
            else:
                x0 = x1
            i += 1

        except ZeroDivisionError:
            mensaje_final = "División entre 0"
            break

    t1 = time.perf_counter()
    return {
        "nombre": metodo, "funcion": f, "valor_inicial": v_inicial, "raiz": raices[-1], "iteraciones": i,
        "historial_errores": errores, "historial_puntos": raices,
        "historial_evaluaciones": evaluaciones, "convergencia": conv,
        "tiempo": t1 - t0, "mensaje": mensaje_final}

# METODOS UN UNICO VALOR INCIAL: NEWTON-RAPHSON, NEWTON MODIFICADO, STEFFENSEN, HALLEY, CHEBYSHEV, OSTROWSKI, JARRATT
def newton_raphson(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:
        
    fx0 = f(x0)
    dfx0 = df(x0)
    x1 = x0 - (fx0 / dfx0)

    return x1  

def newton_modificado(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:
    
    fx0 = f(x0)
    dfx0 = df(x0)
    ddfx0 = ddf(x0)
    x1 = x0 - (fx0 * dfx0) / (dfx0**2 - fx0 * ddfx0)

    return x1

def halley(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:
    
    fx0 = f(x0)
    dfx0 = df(x0)
    ddfx0 = ddf(x0)    
    denominador = dfx0**2 - (fx0 * ddfx0)/2

    x1 = x0 - (fx0 * dfx0) / denominador

    return x1

def chebyshev(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:

    fx0 = f(x0)
    dfx0 = df(x0)
    ddfx0 = ddf(x0)

    x1 = x0 - (fx0 / dfx0) * (1 + (fx0 * ddfx0) / (2 * dfx0**2)) 

    return x1

def ostrowski(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:

    fx0 = f(x0)
    dfx0 = df(x0)
    y = x0 - fx0 / dfx0
    fy = f(y)
    x1 = y - (fy * (y - x0)) /(2*fy - fx0)

    return x1

def jarratt(f: Callable[[float], float], df: Callable[[float], float], ddf: Callable[[float], float], x0: float) -> float:

    fx0 = f(x0)
    dfx0 = df(x0)

    y = x0 - (2*fx0) / (3*dfx0)
    dfy = df(y)

    x1 = x0 - (1/2)*(fx0 / dfx0) + fx0 / (dfx0 - 3* dfy)

    return x1


# METODOS CON DOS VALORES INCIALES: BISECCION, SECANTE, REGULA-FALSI, ILLINOIS PEGASUS
def metodo2(metodo: str, f: Callable[[float], float], x0: float, x1: float,
            tolx: float = TOLX, tolf: float = TOLF, max_iter: int=MAX_ITER) -> Dict[str, Any]:
    
    v_iniciales = (x0,x1)
    errores, raices, evaluaciones, conv = [np.nan,abs(x0-x1)], [x0,x1,], [f(x0),f(x1), ], False
    t0 = time.perf_counter()
    i = 0

    mensaje_final = "Diverge"
    valores = (x0, x1, f(x0), f(x1))

    while i < max_iter and not conv:
        try:
            x_nuevo, fx_nuevo, error, valores = metodo(f, *valores)

            raices.append(x_nuevo)
            evaluaciones.append(fx_nuevo)
            errores.append(error)

            if errores[-1] < tolx and abs(fx_nuevo) < tolf:
                conv = True
                mensaje_final = "Converge"
        
            i += 1

        except ZeroDivisionError:
            mensaje_final = "División entre 0"
            break

    t1 = time.perf_counter()
    return {
        "nombre": metodo, "funcion": f, "valor_inicial": v_iniciales, "raiz": raices[-1], "iteraciones": i,
        "historial_errores": errores, "historial_puntos": raices,
        "historial_evaluaciones": evaluaciones, "convergencia": conv,
        "tiempo": t1 - t0, "mensaje": mensaje_final}


def biseccion(f: Callable[[float], float], a: float, b: float, fa: float, fb: float):

    if fa * fb >= 0:  raise ValueError("Error: La condición inicial no satisface el teorema de Bolzano.")

    x = a + (b-a)/2
    fx = f(x)
    error = abs((b-a)/2)

    if fa * fx < 0:
        sig =(a, x, fa, fx)
    else: 
        sig = (x, a, fx, fb)
           
    return x, fx, error, sig

def secante(f: Callable[[float], float], x0: float, x1: float, fx0: float, fx1: float):

    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
    fx2 = f(x2)
    error = abs(x2 - x1)

    sig = (x1, x2, fx1, fx2)
           
    return x2, fx2, error, sig

def regula_falsi(f: Callable[[float], float], x0: float, x1: float, fx0: float, fx1: float):

    if fx0 * fx1 >= 0:  raise ValueError("Error: La condición inicial no satisface el teorema de Bolzano.")

    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
    fx2 = f(x2)
    error = abs(x2 - x1)

    if fx2 * fx1 < 0: # Raiz el intervalo entre x1 y x2
        sig = (x1, x2, fx1, fx2)
    else:
        sig = (x0, x2, fx0, fx2)
           
    return x2, fx2, error, sig

def illinois(f: Callable[[float], float], x0: float, x1: float, fx0: float, fx1: float):

    if fx0 * fx1 >= 0:  raise ValueError("Error: La condición inicial no satisface el teorema de Bolzano.")

    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
    fx2 = f(x2)
    error = abs(x2 - x1)

    if fx2 * fx1 < 0:
        sig = (x1, x2, fx1, fx2)
    else:
        sig = (x0, x2, fx0/2, fx2)
           
    return x2, fx2, error, sig

def pegasus(f: Callable[[float], float], x0: float, x1: float, fx0: float, fx1: float):

    if fx0 * fx1 >= 0:  raise ValueError("Error: La condición inicial no satisface el teorema de Bolzano.")

    x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
    fx2 = f(x2)
    error = abs(x2 - x1)

    if fx2 * fx1 < 0: 
        sig = (x1, x2, fx1, fx2)
    else:
        sig = (x0, x2, fx0 * fx1 / (fx1 + fx2), fx2)
           
    return x2, fx2, error, sig