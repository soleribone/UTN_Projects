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
    monto_base=round(monto_nominal-(monto_nominal*9)/100,2)
    moneda = "JPY"
else:
    print("Moneda no autorizada")
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