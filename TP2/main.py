def extraer_moneda(cod_pago):
    monedas_validas=("USD", "EUR", "ARS", "GBP", "JPY")
    cantidad_total=0
    moneda_encontrada=''
    for mon in monedas_validas:
        if mon in cod_pago:
            cantidad_total += 1
            if moneda_encontrada == '':
                moneda_encontrada = mon
            elif moneda_encontrada != mon:
                return '', True

    if cantidad_total == 0:
        return '', True  # No se encontró ninguna moneda válida
    else:
        return moneda_encontrada, False  # Una o más veces la misma moneda


def calculo_comisiones(moneda,algoritmo_comision,monto_nominal):
    #destinatario, cod_identificacion, ord_pago, monto, cod_comision, cod_cal_impositivo=capturar_datos();
    comision=0
    monto_base=0
    if algoritmo_comision==1:
        comision=(monto_nominal*9)//100
        monto_base=monto_nominal-comision
    elif algoritmo_comision==2:
        if monto_nominal<50000:
            monto_base=monto_nominal
        elif 50000<=monto_nominal<80000:
            comision = (monto_nominal*5)//100
            monto_base = monto_nominal - comision
        elif monto_nominal>=80000:
            comision = (monto_nominal * 7.8) // 100
            monto_base = monto_nominal - comision
    elif algoritmo_comision==3:
        monto_fijo = 100
        if monto_nominal>=25000:
            comision = (monto_nominal * 6) // 100
            monto_base = monto_nominal - (monto_fijo+comision)
        else:
            monto_base=monto_nominal-monto_fijo
    elif algoritmo_comision==4 and moneda=="JPY":
        if monto_nominal <= 100000:
            comision = 500
            monto_base = monto_nominal - comision
        else:
            comision=1000
            monto_base = monto_nominal - comision
    elif algoritmo_comision==5:
        if monto_nominal<500000:
            comision=0
            monto_base=monto_nominal
        elif monto_nominal>=500000:
            comision = (monto_nominal * 7) // 100
            if comision>500000:
                comision = 50000
                monto_base = monto_nominal-comision
            else:
                monto_base = monto_nominal - comision

    elif algoritmo_comision == 7 and moneda == "JPY":
        if monto_nominal <= 75000:
            comision = 3000
        elif monto_nominal > 75000:
            comision = (monto_nominal - 75000) * 5 // 100

        if comision > 10000:
            comision = 10000

        monto_base = monto_nominal - comision

    else:
        monto_base = monto_nominal

    return monto_base

def calculo_impositivo(monto_base,algoritmo_impositivo):
    impuesto=0
    monto_final=0
    if algoritmo_impositivo==1:
        if monto_base<=300000:
            monto_final=monto_base
        elif monto_base>300000:
            excedente=monto_base-300000
            impuesto= (excedente * 25) // 100
            monto_final=monto_base-impuesto
    elif algoritmo_impositivo==2:
        if monto_base<50000:
            impuesto=50
            monto_final=monto_base-impuesto
        elif monto_base>=50000:
            impuesto = 100
            monto_final = monto_base - impuesto
    elif algoritmo_impositivo==3:
        impuesto= (monto_base * 3) // 100
        monto_final = monto_base - impuesto

    else:
        monto_final = monto_base

    return monto_final

def leer_archivo(nombre):
    archivo = open(nombre)
    time_stamp = archivo.readline()
    return archivo


def capturar_datos(linea):
    destinatario = cod_identificacion = ord_pago = monto = cod_comision= cod_cal_impositivo = ""
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
        elif c in "-_" or c == " ":
            estado = True
        else:
            estado = False
            break

    return estado

def calcular_porcentaje(total, parte):
    return (parte * 100) // total

def calcular_promedio(total, cantidad):
    resultado=0
    if cantidad!=0:
        resultado=total // cantidad

    return resultado

def mostrar_resultados(cant_inv_por_moneda,cant_inv_por_destinatario,cant_operaciones_validas,suma_mf_validas,cant_ARS,cant_USD,cant_EUR,cant_GBP,cant_JPY,cod_pago_mayor,monto_nominal_mayor, monto_final_mayor,nom_primer_benef,cant_nom_primer_benef,porcentaje,promedio):
     print(' (r1) - Cantidad de ordenes invalidas - moneda no autorizada:', cant_inv_por_moneda)
     print(' (r2) - Cantidad de ordenes invalidas - beneficiario mal identificado:', cant_inv_por_destinatario)
     print(' (r3) - Cantidad de operaciones validas:', cant_operaciones_validas)
     print(' (r4) - Suma de montos finales de operaciones validas:', suma_mf_validas)
     print(' (r5) - Cantidad de ordenes para moneda ARS:', cant_ARS)
     print(' (r6) - Cantidad de ordenes para moneda USD:', cant_USD)
     print(' (r7) - Cantidad de ordenes para moneda EUR:', cant_EUR)
     print(' (r8) - Cantidad de ordenes para moneda GBP:', cant_GBP)
     print(' (r9) - Cantidad de ordenes para moneda JPN:', cant_JPY)
     print('(r10) - Codigo de la orden de pago con mayor diferencia  nominal - final:', cod_pago_mayor)
     print('(r11) - Monto nominal de esa misma orden:', monto_nominal_mayor)
     print('(r12) - Monto final de esa misma orden:', monto_final_mayor)
     print('(r13) - Nombre del primer beneficiario del archivo:', nom_primer_benef)
     print('(r14) - Cantidad de veces que apareció ese mismo nombre:', cant_nom_primer_benef)
     print('(r15) - Porcentaje de operaciones inválidas sobre el total:', porcentaje)
     print('(r16) - Monto final promedio de las ordenes validas en moneda ARS:', promedio)


def contar_monedas(moneda, c_monedas, param):
    if param in moneda:
        c_monedas += 1
    return c_monedas

def main():
    nombre = "ordenes100.txt"
    archivo_leido = leer_archivo(nombre)
    #Variables
    destinatario= cod_identificacion= ord_pago= monto= cod_comision= cod_cal_impositivo = ""

    # -----------------R1,R2------------------:
    cant_inv_por_destinatario,cant_inv_por_moneda=0,0
    # -----------------R3------------------:
    cant_operaciones_validas=0
    # -----------------R4------------------:
    suma_mf_validas=0
    # -----------------R5,R6,R7,R8,R9------------------:
    cant_JPY = cant_GBP = cant_ARS = cant_USD = cant_EUR = 0

    #------------------R10,R11,R12--------------------:
    mayor_diferencia = 0
    cod_pago_mayor = ''

    #
    # -----------------R13,R14,R15,R16------------------:
    nom_primer_benef = None
    cant_nom_primer_benef = 0
    porcentaje = 0
    cant_operaciones_validas_R16, monto_base_R16, monto_final_R16, suma_mf_validas_R16 = 0, 0, 0, 0

    for linea in archivo_leido:
        destinatario, cod_identificacion, ord_pago, monto_nominal, cod_comision, cod_cal_impositivo = capturar_datos(linea)
        monto_nominal = int(monto_nominal)
        cod_comision = int(cod_comision)
        cod_cal_impositivo = int(cod_cal_impositivo)

        #-----------------R1,R2------------------:
        moneda, flag_moneda = extraer_moneda(ord_pago)
        flag_destinatario = validar_cod_identificacion(cod_identificacion)
        if flag_moneda:
            cant_inv_por_moneda += 1
        elif not flag_destinatario:
            cant_inv_por_destinatario += 1

        elif flag_moneda and not flag_destinatario: #Operación inválida por ambos motivos
            cant_inv_por_moneda += 1

        # -----------------R3,R4------------------:
        if not flag_moneda and flag_destinatario:
            cant_operaciones_validas+=1
            monto_base=calculo_comisiones(moneda,cod_comision,monto_nominal)
            monto_final=calculo_impositivo(monto_base,cod_cal_impositivo)
            suma_mf_validas+=monto_final

        # -----------------R5,R6,R7,R8,R9------------------:
        if not flag_moneda:
            cant_ARS = contar_monedas(moneda, cant_ARS, "ARS")
            cant_USD = contar_monedas(moneda, cant_USD, "USD")
            cant_EUR = contar_monedas(moneda, cant_EUR, "EUR")
            cant_GBP = contar_monedas(moneda, cant_GBP, "GBP")
            cant_JPY = contar_monedas(moneda, cant_JPY, "JPY")

        #-------------R10,R11,R12----------
        monto_base_r10=calculo_comisiones(moneda,cod_comision,monto_nominal)
        monto_final_r10 =calculo_impositivo(monto_base_r10, cod_cal_impositivo)

        diferencia = monto_nominal-monto_final_r10
        if diferencia > mayor_diferencia:
            mayor_diferencia = diferencia
            cod_pago_mayor = ord_pago
            monto_nominal_mayor = monto_nominal
            monto_final_mayor = monto_final_r10


        #  -----------------R13,R14------------------:

        if nom_primer_benef is None:
            nom_primer_benef = destinatario
            cant_nom_primer_benef += 1
        elif nom_primer_benef == destinatario:
            cant_nom_primer_benef += 1

        #  -----------------R15-----------------:

        cant_total_operaciones = cant_operaciones_validas + cant_inv_por_moneda + cant_inv_por_destinatario
        cant_total_operaciones_invalidas = cant_inv_por_moneda + cant_inv_por_destinatario

        porcentaje = calcular_porcentaje(cant_total_operaciones, cant_total_operaciones_invalidas)

        #  -----------------R16-----------------:

        if not flag_moneda:
            if moneda == "ARS" and flag_destinatario:
                cant_operaciones_validas_R16 += 1
                monto_base_R16 = calculo_comisiones(moneda, cod_comision, monto_nominal)
                monto_final_R16 = calculo_impositivo(monto_base_R16, cod_cal_impositivo)
                suma_mf_validas_R16 += monto_final_R16

        promedio = calcular_promedio(suma_mf_validas_R16, cant_operaciones_validas_R16)

    #  --------------------------------------:

    mostrar_resultados(cant_inv_por_moneda,cant_inv_por_destinatario,cant_operaciones_validas,suma_mf_validas,cant_ARS,cant_USD,cant_EUR,cant_GBP,cant_JPY,cod_pago_mayor,monto_nominal_mayor, monto_final_mayor,nom_primer_benef,cant_nom_primer_benef,porcentaje,promedio)
    archivo_leido.close()

if __name__ == "__main__":
    main()

# TODO: r8 Cantidad de ordenes para moneda GBP:', cant_GBP) Resultado: 5
# TODO: r9 Cantidad de ordenes para moneda JPN:', cant_JPY) Resultado: 4
# TODO: r10 Codigo de la orden de pago con mayor diferencia  nominal - final:', cod_my) Resultado: MEURMUCGC
# TODO: r11 Monto nominal de esa misma orden:', mont_nom_my) Resultado: 835807747
# TODO: r12 Monto final de esa misma orden:', mont_fin_my) Resultado: 589319388
