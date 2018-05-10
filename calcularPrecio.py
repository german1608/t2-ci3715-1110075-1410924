# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import unittest
from decimal import Decimal
from Tarifa import Tarifa

def calcularPrecio(tarifa,tiempoDeServicio):
    
    #Primer argumento debe ser de tipo object
    if not isinstance(tarifa, Tarifa):
        raise TypeError ("ERROR: Primer argumento debe ser de tipo object")
    #Segundo argumento debe ser de tipo lista
    if not isinstance(tiempoDeServicio, list):
        raise TypeError ("ERROR: Segundo argumento debe ser de tipo lista")
    #Primer elemento de la lista debe ser de tipo datetime
    if not isinstance(tiempoDeServicio[0], datetime.datetime):
        raise TypeError ("ERROR: Primer elemento de la lista debe ser de tipo datetime")
    #Segundo elemento de la lista debe ser de tipo datetime
    if not isinstance(tiempoDeServicio[1], datetime.datetime):
        raise TypeError ("ERROR: Segundo elemento de la lista debe ser de tipo datetime")

    if (tiempoDeServicio[1] < tiempoDeServicio[0]):
        raise ValueError ("ERROR:Tiempo de servicio debe tener sentido")

    if abs(tiempoDeServicio[1].weekday() - tiempoDeServicio[0].weekday()) >7:
        raise ValueError ("ERROR: debe durar maximo 7 dias en el servicio")
    if (tiempoDeServicio[1].minute - tiempoDeServicio[0].minute < 15):
        raise ValueError ("ERROR: debe durar al menos 15 minutes en el servicio")

    '''
    Caso_1: entra y sale en un mismo dia.
    '''
    cantHrs = 1
    monto = 1
    #Quice minutos exactos entre semana
    if (tiempoDeServicio[0].weekday() >=0 and tiempoDeServicio[0].weekday() <=4 and 
        tiempoDeServicio[0].weekday() == tiempoDeServicio[1].weekday()):
        if (tiempoDeServicio[1].minute - tiempoDeServicio[0].minute == 15):
            monto = monto*tarifa.tarifa_entre_semana
            print monto
        return monto
    #Quice minutos exactos en el fin de semana
    if (tiempoDeServicio[0].weekday() >=5 and tiempoDeServicio[0].weekday() <=6 and 
        tiempoDeServicio[0].weekday() == tiempoDeServicio[1].weekday()):
        if (tiempoDeServicio[1].minute - tiempoDeServicio[0].minute == 15):
            monto = monto*tarifa.tarifa_fin_semana
            print monto
        return monto

    if (tiempoDeServicio[1].weekday() == tiempoDeServicio[0].weekday()):
        cantHrs = (tiempoDeServicio[1].hour - tiempoDeServicio[0].hour)
        #Except para al menos 15 minutos en el servicio
        if (tiempoDeServicio[1].hour == tiempoDeServicio[0].hour):
            cantHrs = 1
        monto = cantHrs*tarifa.tarifa_entre_semana
        return monto
    else:
        for i in range(tiempoDeServicio[0].weekday(), tiempoDeServicio[1].weekday()):
            for j in range(tiempoDeServicio[0].hour, 24):
                cantHrs = cantHrs +1
                monto = tarifa_entre_semana*cantHrs
        return monto
    print "Duro %s hr en el servicio. Se le cancelan Bs.%s " %(cantHrs, monto)        