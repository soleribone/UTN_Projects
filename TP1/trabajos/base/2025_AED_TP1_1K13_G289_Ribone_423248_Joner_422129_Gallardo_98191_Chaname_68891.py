beneficiario =input()

codigo = input()

monto_nominal = float(input())



if "USD" in codigo:
    monto_base= round(monto_nominal-(monto_nominal*7)/100,2)
    moneda = "USD"
elif "EUR" in codigo:
    monto_base= round(monto_nominal-(monto_nominal*7)/100,2)
    moneda = "EUR"
elif "ARS" in codigo:
    monto_base=round(monto_nominal-(monto_nominal*5)/100,2)
    moneda = "ARS"
elif "GBP" in codigo:
    monto_base=round(monto_nominal-(monto_nominal*9)/100,2)
    moneda = "GBP"
elif "JPY" in codigo:
    comision = 0
    if monto_nominal >= 15000:
        if 15000 <= monto_nominal <=500000:
            comision = (monto_nominal*9)/100
            if comision > 950000:
                comision = 950000

        elif 500000 < monto_nominal <= 1500000:
            comision = (monto_nominal*7.8)/100
            if comision > 950000:
                comision = 950000

        elif 1500000 <= monto_nominal <=10000000:
            comision = (monto_nominal*5.5)/100
            if comision > 950000:
                comision = 950000
        else:
            comision = (monto_nominal*5)/100   #MONTO NOMINAL> 19000000
            if comision > 950000:
                comision = 950000

        monto_base = round(monto_nominal- comision,2)
        moneda = "JPY"
    else:
        monto_base = 0
        moneda = "Monto mínimo para JPY no alcanzado"


else:
    moneda = "Moneda no autorizada"
    monto_base = 0



if monto_base>500000:
    monto_final = round(monto_base - (monto_base*21)/100,2)
elif monto_base<500000:
    monto_final=monto_base


print("Beneficiario:", beneficiario)
print("Moneda:", moneda)
print("Monto base (descontadas las comisiones):", monto_base)
print("Monto final (descontados los impuestos):", monto_final)


#que secan todos los codigos
#que se calculen bien segun cada codigo
#que se calcule el monto final