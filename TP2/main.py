def leer_archivo(nombre):
    archivo = open(nombre)
    texto = archivo.readlines()
    return texto,archivo


def capturar_datos(linea):
    destinatario = cod_identificacion = ord_pago = monto = cod_comision= cod_cal_impositivo =  ""
    destinatario = linea[0:20]
    cod_identificacion = linea[20:30]
    ord_pago = linea[30: 40] #Moneda
    monto = linea[40: 50]
    cod_comision = linea[50:52]
    cod_cal_impositivo = linea[52:54]
    return destinatario,cod_identificacion,ord_pago,monto,cod_comision,cod_cal_impositivo


def mostrar_pagos(destinatario,cod_identificacion,ord_pago,monto,cod_comision,cod_cal_impositivo):
    print(
        "*" * 15, "NUEVO PAGO", "*" * 15, "\n",
        "1 DESTINATARIO =", destinatario, "\n",
        "2 COD_IDENTIFICACION =", cod_identificacion, "\n",
        "3 ORD_PAGO =", ord_pago, "\n",
        "4 MONTO =", monto, "\n",
        "5 COD_COMISION  =", cod_comision, "\n",
        "6 COD_CALC_IMPOSITIVO = " + cod_cal_impositivo + "."
    )


def validar_moneda(cod_identificacion):
    mensaje = ''
    pass


def validar_cod_identificacion(destinatario):
    estado = False
    for c in destinatario:
        if "A" <= c <= "Z" or c in "0123456789" or c == " ":
            estado = True
        elif estado  and c in "-_" or c == " ":
            estado = True
        else:
            estado = False
            break

    return estado



def main():
    nombre = "ordenes25.txt"
    texto,archivo_leido = leer_archivo(nombre)

    archivo_leido.close()

    #Contadores
    saltos = 0
    #Variables
    destinatario= cod_identificacion= ord_pago= monto= cod_comision= cod_cal_impositivo = ""

    #Banderas

    for linea in texto:
        if saltos >= 1:
            
            destinatario,cod_identificacion,ord_pago,monto,cod_comision,cod_cal_impositivo = capturar_datos(linea)
            mostrar_pagos(destinatario,cod_identificacion,ord_pago,monto,cod_comision,cod_cal_impositivo)

            #Validar Monedas
            moneda = validar_moneda(cod_identificacion)
            #Validar Destinatorio
            if validar_cod_identificacion(cod_identificacion):
                print("Cod Identificacion valido.")
            else:
                print("Cod Identificacion invalido.")
        
            
        saltos += 1

if __name__ == "__main__":
    main()