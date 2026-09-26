import os

from tabulate import tabulate
import pandas as pd

def tabla(f :str, resultados: dict, guardar_archivo: bool = False):

    df = pd.DataFrame({"Aproximación x_n":resultados["historial_puntos"],
                       "Evaluación f(x_n)": resultados["historial_evaluaciones"],
                       "Error de aproximación": resultados["historial_errores"]})

    df.index.name = "Iteración"

    encabezado = f"--- Tabla de la ecuación {f} = 0 ---\n----- Valor Inicial: {resultados['valor_inicial']} -----\n----- Método de {resultados['nombre']} -----\n"
    tabla = tabulate(df, 
                    headers='keys',
                    tablefmt = "pipe", # Cambiar "pipe" por "latex" para formato LaTeX.
                    colalign=("center", "center", "center", "center"))
    
    if guardar_archivo:
        carpeta = "tests"
        os.makedirs(carpeta, exist_ok=True)
        nombre_archivo = f"tabla_{f}.txt".replace(" ", "").replace("/", "___").replace("*", "·")
        ruta = os.path.join(carpeta, nombre_archivo)
        
        with open(ruta, "a", encoding="utf-8") as file:
            file.write(encabezado + tabla + "\n\n")
    
    print(encabezado + tabla)
