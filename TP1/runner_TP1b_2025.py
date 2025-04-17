import os
import subprocess

# Directorio donde se almacenan los programas entregados por los estudiantes
SOURCES = "./trabajos/"

# Lotes de prueba contra los que serán corridos los programas de los estudiantes.
# ("CP\nDirección\nTipo de envío\nForma de pago\n", Contexto, r1, r2, r3, r4)

BATCH_COMMON = (
    # Códigos especiales
    ("Docente A.E.D.\nArS\n50000000\n", "Ítem a", "Docente A.E.D.", "Moneda no autorizada", "0", "0"),
    ("Docente A.E.D.\nUsD\n50000000\n", "Ítem b", "Docente A.E.D.", "Moneda no autorizada", "0", "0"),
    ("Docente A.E.D.\nEuR\n50000000\n", "Ítem c", "Docente A.E.D.", "Moneda no autorizada", "0", "0"),
    ("Docente A.E.D.\nGbP\n50000000\n", "Ítem d", "Docente A.E.D.", "Moneda no autorizada", "0", "0"),
    ("Docente A.E.D.\nJpY\n50000000\n", "Ítem e", "Docente A.E.D.", "Moneda no autorizada", "0", "0"),

    # Valores sin impuestos
    ("Docente A.E.D.\nARS\n526315\n", "Ítem f", "Docente A.E.D.", "ARS", "499999.25", "499999.25"),
    ("Docente A.E.D.\nUSD\n537634\n", "Ítem g", "Docente A.E.D.", "USD", "499999.62", "499999.62"),
    ("Docente A.E.D.\nEUR\n437634\n", "Ítem h", "Docente A.E.D.", "EUR", "406999.62", "406999.62"),
    ("Docente A.E.D.\nGBP\n549450\n", "Ítem i", "Docente A.E.D.", "GBP", ("499999.5", "499999.50"), ("499999.5", "499999.50")),
    ("Docente A.E.D.\nJPY\n449450\n", "Ítem j", "Docente A.E.D.", "JPY", ("408999.5", "408999.50"), ("408999.5", "408999.50")),

    # Valores con impuestos
    ("Docente A.E.D.\nARS\n526316\n", "Ítem k", "Docente A.E.D.", "ARS", ("500000.2", "500000.20"), "395000.16"), # 385000.158
    ("Docente A.E.D.\nUSD\n537635\n", "Ítem l", "Docente A.E.D.", "USD", "500000.55", "395000.43"), # 395000,4345
    ("Docente A.E.D.\nEUR\n537636\n", "Ítem m", "Docente A.E.D.", "EUR", "500001.48", "395001.17"), # 395001,1692
    ("Docente A.E.D.\nGBP\n549452\n", "Ítem n", "Docente A.E.D.", "GBP", "500001.32", "395001.04"), # 395001,0428
    ("Docente A.E.D.\nJPY\n549453\n", "Ítem o", "Docente A.E.D.", "JPY", "500002.23", "395001.76")  # 395001,7617,
)

BATCHES = {
    "base": BATCH_COMMON
}


# Muestra los valores contenidos en "text" en una línea de color rojo intenso.
def print_red(*text, end="\n"):
    for t in text:
        print(f"\033[91m{t}\033[00m", end=" ")
    print(end=end)


# Ejecuta el programa "script" y captura las salidas que sean dirigidas a la consola estándar.
def run(script):
    encoding = "utf-8"
    proc = subprocess.Popen(["python3", script], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc, encoding


def check_single_result(result, expected):
    if isinstance(expected, tuple):
        return result in expected
    return result == expected


def show_and_count(lines, results, data):
    # Índice para recorrer la lista "data" de resultados...
    # ... en esa lista, los resultados comienzan en la posición 2...
    k = 2

    # Contador de resultados correctos...
    ok = 0

    # print()
    for i in range(len(lines)):
        # ... mostrar el contexto del lote, si corresponde (líneas con número de orden divisible por 4)...
        if i % 4 == 0:
            print(f"\033[94mPrueba {data[1]}\033[00m")

        # ... mostrar el resultado tal como se mostró en el programa original...
        print("\t", lines[i], end="")

        # ... e informar correctos e incorrectos...
        if check_single_result(results[i].strip(), data[k]):
            ok += 1
            print(f"\033[92m --> Correcto\033[00m")
        else:
            print(f"\033[91m --> Incorrecto (esperado: {data[k]})\033[00m")

        if i % 4 == 3:
            print()

        k += 1

    # ...retornar el contador de respuestas correctas y salir...
    return ok


def collect_results(lines):
    # ... recolectar los resultados desde la consola estándar...
    results = []
    for i in range(len(lines)):
        # ...los resultados vienen luego de una secuencia ': '...
        r = lines[i].split(': ')
        results.append(r[1].strip())

    # ...retornar los resultados y salir...
    return results


# Procesa cada tupla "data" del lote "BATCH" con el programa "script" y analiza los resultados.
def start(script, batch):
    print_red("\n---------------------------------")
    print_red("Programa:", script.name)
    print_red("---------------------------------")

    ok = 0
    for data in batch:
        # Ejecutar el programa entregado por el estudiante...
        process, encoding = run(script.path)

        # Si hay datos tomados desde la línea de órdenes en la variable data, va esta línea...
        input_data = data[0].encode(encoding)
        output_lines, _ = process.communicate(input_data)

        # Si hay datos tomados desde la línea de órdenes en la variable data, va esta línea...
        # stdout_value = process.communicate(data[0].encode('utf-8'))[0].decode('utf-8')
        stdout_value = output_lines.decode(encoding)

        # Si NO hay datos desde la línea de órdenes, va esta otra...
        # ... para capturar lo que sea que se haya enviado a la consola de salida...
        # stdout_value = process.communicate()[0].decode('utf-8')

        # ... dividir en líneas esa salida...
        lines = stdout_value.splitlines()

        # ... eliminar los mensajes de input de la primera línea...
        r = lines[0].split(": ")[-2:]
        lines[0] = r[0] + ": " + r[1]

        # ...recolectar los resultados desde la consola estándar...
        results = collect_results(lines)

        # Mostrar las salidas del programa tal cual fueron generadas por los estudiantes...
        # ...pero indicando y contando los resultados correctos o no...
        ok += show_and_count(lines, results, data)

    ct = 4 * len(batch)
    prc = ok * 100 // ct
    print()
    print(f"\033[95mCantidad de resultados correctos: {ok}\033[00m")
    print(f"\033[95mPorcentaje de resultados correctos: {prc}%\033[00m")


# Inicia el test para todos los programas contenidos en el directorio "SOURCES".
def init():

    for a_day in BATCHES.keys():
        base_dir = f"{SOURCES}{a_day}"
        if not os.path.isdir(base_dir):
            print("Ignorando el directorio:", base_dir)
            continue

        print_red("\n\t\t*** Procesando lote", a_day.upper(), "***")
        with os.scandir(base_dir) as programs:
            for script in programs:
                if script.name.endswith(".py"):
                    try:
                        start(script, BATCHES[a_day])
                    except Exception as ex:
                        print()
                        print(f"\033[1;93;41m--> Error al ejecutar: ({ex})\033[00m")
                    print()
                    # input("Presione <Enter> para continuar con el siguiente trabajo...")


if __name__ == '__main__':
    init()
