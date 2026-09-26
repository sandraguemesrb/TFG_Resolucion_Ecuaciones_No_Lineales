import os

from metodos import (
    metodo1, metodo2,
    newton_raphson, newton_modificado, halley, chebyshev, ostrowski, jarratt,
    biseccion, secante, regula_falsi, illinois, pegasus)

import sympy as sp


def comparar_metodos(f_str: str, configuraciones: list, guardar_archivo: bool = True):
    
    dicc_metodos1 = {
        "Newton-Raphson": newton_raphson,
        "Newton Modificado": newton_modificado, 
        "Halley": halley, "Chebyshev": chebyshev, 
        "Ostrowski": ostrowski, "Jarratt": jarratt 
    }

    dicc_metodos2 = {
        "Bisección": biseccion, "Secante": secante, 
        "Regula-Falsi": regula_falsi, "Illinois": illinois, "Pegasus": pegasus
    }
    
    # Preparar la función y sus derivadas una sola vez.
    x = sp.symbols('x')
    f_sp = sp.sympify(f_str)
    f_num = sp.lambdify(x, f_sp, 'numpy')
    
    df_sp = sp.diff(f_sp)
    df_num = sp.lambdify(x, df_sp, 'numpy')
    
    ddf_sp = sp.diff(df_sp)
    ddf_num = sp.lambdify(x, ddf_sp, 'numpy')

    resultados_tabla = []

    # Ejecutar cada método.
    for metodo, cond_iniciales in configuraciones:
        if metodo not in dicc_metodos1 and metodo not in dicc_metodos2:
            print(f" El método '{metodo}' no existe. Se omite.")
            continue
            
        args = [f_num]
        
        if metodo in dicc_metodos1:
            args.append(df_num)
            args.append(ddf_num)
            
        args.extend(cond_iniciales)
        
        # Formatear visualmente los Valores Iniciales
        # Si es un método de intervalos usa corchetes [a, b], si no, los separa por comas
        if metodo in ["Bisección", "Regula-Falsi"]:
            val_ini_str = f"[{', '.join(str(v) for v in cond_iniciales)}]"
        else:
            val_ini_str = ", ".join(str(v) for v in cond_iniciales)
        
        try:
            if metodo in dicc_metodos1:
                metodo_test = dicc_metodos1[metodo]
                res = metodo1(metodo_test, *args)
            elif metodo in dicc_metodos2:
                metodo_test = dicc_metodos2[metodo]
                res = metodo2(metodo_test, *args)
            
            if res["convergencia"]:
                raiz_val = float(res["raiz"])
                raiz_str = f"{raiz_val:.5f}"
                
                fx_val = float(res["historial_evaluaciones"][-1])
                if fx_val == 0:
                    fx_str = "0"
                else:
                    s = f"{fx_val:.5e}"  
                    base, exp = s.split('e')
                    exp = int(exp)
                    if exp == 0:
                        fx_str = f"${base}$"
                    else:
                        fx_str = f"${base}\\times10^{{{exp}}}$"
            else:
                raiz_str = "-"
                fx_str = res["mensaje"] # Aquí saldrá "Diverge" o "División entre 0"

            resultados_tabla.append({
                "Método": metodo,
                "Val. Iniciales": val_ini_str,
                "Iteraciones": str(res["iteraciones"]),
                "Raíz (\\alpha)": raiz_str,
                "f(\\alpha)": fx_str
            })
            
        except Exception as e:
            resultados_tabla.append({
                "Método": metodo,
                "Val. Iniciales": val_ini_str,
                "Iteraciones": "-",
                "Raíz (\\alpha)": "-",
                "f(\\alpha)": f"Error Python: {str(e)}"
            })

    #  Anchos máximos
    w_metodo = max(len(r["Método"]) for r in resultados_tabla) if resultados_tabla else 15
    w_val = max(len(r["Val. Iniciales"]) for r in resultados_tabla) if resultados_tabla else 15
    w_iter = max(len(r["Iteraciones"]) for r in resultados_tabla) if resultados_tabla else 11
    w_raiz = max(len(r["Raíz (\\alpha)"]) for r in resultados_tabla) if resultados_tabla else 15

    # Cuerpo de la tabla en LaTeX
    filas_latex = []
    for r in resultados_tabla:
        m = r["Método"].ljust(w_metodo)
        v = r["Val. Iniciales"].ljust(w_val)
        i = r["Iteraciones"].rjust(w_iter)
        ra = r["Raíz (\\alpha)"].ljust(w_raiz)
        y = r["f(\\alpha)"].ljust(20)

        fila = f"{m} & {v} & {i} & {ra} & {y} \\\\"
        filas_latex.append(fila)
        
    cuerpo_tabla = "\n\n".join(filas_latex)

    f_latex = sp.latex(f_sp)
    salida_final = (
        f"\\begin{{table}}[H]\n"
        f"\\centering\n\n"
        f"\\renewcommand{{\\arraystretch}}{{1.3}} % altura entre filas\n"
        f"\\setlength{{\\tabcolsep}}{{12pt}}      % espacio horizontal entre columnas\n\n"
        f"\\begin{{tabular}}{{ccccc}}\n"
        f"\\hline\n"
        f"Método & Val. Iniciales & Iteraciones & Raíz $(\\alpha)$ & $f(\\alpha)$ \\\\\n"
        f"\\hline\n\n"
        f"{cuerpo_tabla}\n\n"
        f"\\hline\n"
        f"\\end{{tabular}}\n\n"
        f"\\caption{{$f(x) = {f_latex}$}}\n"
        f"\\end{{table}}\n\n"
    )
    print(salida_final)

    if guardar_archivo:
        carpeta = "tests/12_06_varios"
        os.makedirs(carpeta, exist_ok=True)
        nombre_archivo = f"comparativa_{f_str[:15]}.tex".replace(" ", "").replace("/", "_").replace("*", "_")
        ruta = os.path.join(carpeta, nombre_archivo)
        
        with open(ruta, "w", encoding="utf-8") as file:
            file.write(salida_final + "\n")
        print(f"\n[INFO] Código LaTeX guardado exitosamente en: {ruta}")


if __name__ == "__main__":
    # --- ZONA DE CONFIGURACIÓN ---
    MI_FUNCION = "atan(x)"  # Cambia esta función por la que quieras evaluar.
    
    x0 = 1.39
    x00 = 1.4

    
    mis_pruebas = [    
        ("Newton-Raphson", [x0]),
        ("Newton-Raphson", [x00]),
        ("Halley", [x0]),
        ("Halley", [x00]),
        ("Chebyshev", [x0]),
        ("Chebyshev", [x00]),
        ("Ostrowski", [x0]),
        ("Ostrowski", [x00]),
        ("Jarratt", [x0]),
        ("Jarratt", [x00]),
    ]

    comparar_metodos(f_str=MI_FUNCION, configuraciones=mis_pruebas, guardar_archivo=True)
