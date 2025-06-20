def extraer_moneda(cod_pago):
    monedas_validas=("USD", "EUR", "ARS", "GBP", "JPY")
    monedas_encontradas= 0
    flag_moneda=False
    cont=0
    moneda_incorrecta=False
    moneda_anterior= moneda=''
    for mon in monedas_validas:
        if mon in cod_pago:
            monedas_encontradas += 1
            if monedas_encontradas > 1 and moneda_anterior != moneda : # TODO:la condc. "dice hay dos o más diferentes", no lo hago and porque tengo que tener 2 o + y ser diferentes por eso la variable mondena anterior.
                moneda_incorrecta = True
            else:
                moneda = mon
        else:
            moneda_incorrecta = True

        moneda_anterior = mon

    return moneda,moneda_incorrecta



def calculo_comisiones(moneda,algoritmo,monto_nominal):
    destinatario, cod_identificacion, ord_pago, monto, cod_comision, cod_cal_impositivo=capturar_datos();



def leer_archivo(nombre):
    archivo = open(nombre)
    time_stamp = archivo.readline()
    return archivo


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

def mostrar_resultados(cant_GBP,cant_JPY,cod_my,mont_nom_my,mont_fin_my):
#     print(' (r1) - Cantidad de ordenes invalidas - moneda no autorizada:', cant_minvalida)
#     print(' (r2) - Cantidad de ordenes invalidas - beneficiario mal identificado:', cant_binvalido)
#     print(' (r3) - Cantidad de operaciones validas:', cant_oper_validas)
#     print(' (r4) - Suma de montos finales de operaciones validas:', suma_mf_validas)
#     print(' (r5) - Cantidad de ordenes para moneda ARS:', cant_ARS)
#     print(' (r6) - Cantidad de ordenes para moneda USD:', cant_USD)
#     print(' (r7) - Cantidad de ordenes para moneda EUR:', cant_EUR)
    print(' (r8) - Cantidad de ordenes para moneda GBP:', cant_GBP)
    print(' (r9) - Cantidad de ordenes para moneda JPN:', cant_JPY)
    print('(r10) - Codigo de la orden de pago con mayor diferencia  nominal - final:', cod_my)
    print('(r11) - Monto nominal de esa misma orden:', mont_nom_my)
    print('(r12) - Monto final de esa misma orden:', mont_fin_my)
#     print('(r13) - Nombre del primer beneficiario del archivo:', nom_primer_benef)
#     print('(r14) - Cantidad de veces que apareció ese mismo nombre:', cant_nom_primer_benef)
#     print('(r15) - Porcentaje de operaciones inválidas sobre el total:', porcentaje)
#     print('(r16) - Monto final promedio de las ordenes validas en moneda ARS:', promedio)


def contar_monedas(moneda, c_monedas, param):
    if param in moneda:
        c_monedas += 1
    return c_monedas


def calc_cod_may(monto_nominal, monto_final, ord_pago,cod_mayor,dif_anterior):
    diferencia = monto_nominal - monto_final
    if cod_mayor is None:
        cod_mayor = ord_pago
        dif_anterior = diferencia
    elif dif_anterior < diferencia:
        cod_mayor = ord_pago
        dif_anterior = diferencia
    return cod_mayor,dif_anterior



def main():
    nombre = "ordenes25.txt"
    archivo_leido = leer_archivo(nombre)
    #Contadores
    cant_GBP= cant_JPY= cod_my= mont_nom_my = mont_fin_my =dif_hist = cant_JPY = cant_GBP = 0
    #Variables
    destinatario= cod_identificacion= ord_pago= monto= cod_comision= cod_cal_impositivo = ""
    cod_mayor = None
    cod_my= ""
    #Banderas
    flag_destinatario = flag_mon = False
    for linea in archivo_leido:
        destinatario, cod_identificacion, ord_pago, monto_nominal, cod_comision, cod_cal_impositivo = capturar_datos(linea)

        moneda_extraida, flag_mon = extraer_moneda(moneda)
        flag_destinatario = validar_cod_identificacion(cod_identificacion)
        #TODO: calculo de monto final
        monto_final = 1
        # Validaciones
        if flag_mon:
            # TODO: R8,metodo para contar monedas, se supone que en este punto las monedas estan verificadas y cumplen las validaciones
            cant_GBP = contar_monedas(moneda, cant_GBP, "GBP")
            # TODO: R9, idem al anterior
            cant_JPY = contar_monedas(moneda, cant_JPY, "JPY")

        else:
            pass

        # TODO: r10 r11 12
        if flag_mon and flag_destinatario:
            cod_my,dif_hist = calc_cod_may(monto_nominal,monto_final,ord_pago,dif_hist)
            mont_nom_my = monto_nominal
            mont_fin_my = monto_final

        moneda, moneda_incorrecta = extraer_moneda(ord_pago)

        # Reinicio
        flag_destinatario = flag_mon = False

        # calculo_comisiones(moneda,cod_comision, monto_nominal)
        print(moneda, "..", moneda_incorrecta)
        moneda_extraida = ""

    archivo_leido.close() #TODO: puede generar error 
    mostrar_resultados(cant_GBP, cant_JPY, cod_my, mont_nom_my, mont_fin_my)
if __name__ == "__main__":
    main()

# TODO: r8 Cantidad de ordenes para moneda GBP:', cant_GBP) Resultado: 5
# TODO: r9 Cantidad de ordenes para moneda JPN:', cant_JPY) Resultado: 4
# TODO: r10 Codigo de la orden de pago con mayor diferencia  nominal - final:', cod_my) Resultado: MEURMUCGC
# TODO: r11 Monto nominal de esa misma orden:', mont_nom_my) Resultado: 835807747
# TODO: r12 Monto final de esa misma orden:', mont_fin_my) Resultado: 589319388
