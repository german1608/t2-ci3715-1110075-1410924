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
    #el tamanho de la lista debe ser 2
    if len(tiempoDeServicio) != 2:
        raise ValueError("ERROR: el tamanho de la lista debe ser 2")

    fecha_inicio, fecha_final = tiempoDeServicio
    #Primer elemento de la lista debe ser de tipo datetime
    if not isinstance(fecha_inicio, datetime.datetime):
        raise TypeError ("ERROR: Primer elemento de la lista debe ser de tipo datetime")
    #Segundo elemento de la lista debe ser de tipo datetime
    if not isinstance(fecha_final, datetime.datetime):
        raise TypeError ("ERROR: Segundo elemento de la lista debe ser de tipo datetime")

    if (fecha_final < fecha_inicio):
        raise ValueError ("ERROR:Tiempo de servicio debe tener sentido")

    if (fecha_final.minute - fecha_inicio.minute < 15):
        print('hla')
        raise ValueError ("ERROR: debe durar al menos 15 minutes en el servicio")
    
    '''
    Caso_1: entra y sale en un mismo dia.
    '''
    cantHrs = 1
    monto = 1
    #Quice minutos exactos entre semana
    if (fecha_inicio.weekday() >=0 and fecha_inicio.weekday() <=4 and 
        fecha_inicio.weekday() == fecha_final.weekday()):
        if (fecha_final.minute - fecha_inicio.minute == 15):
            monto = monto*tarifa.tarifa_entre_semana
        return monto
    #Quice minutos exactos en el fin de semana
    if (fecha_inicio.weekday() >=5 and fecha_inicio.weekday() <=6 and 
        fecha_inicio.weekday() == fecha_final.weekday()):
        if (fecha_final.minute - fecha_inicio.minute == 15):
            monto = monto*tarifa.tarifa_fin_semana
        return monto

    if (fecha_final.weekday() == fecha_inicio.weekday()):
        cantHrs = (fecha_final.hour - fecha_inicio.hour)
        #Except para al menos 15 minutos en el servicio
        if (fecha_final.hour == fecha_inicio.hour):
            cantHrs = 1
        monto = cantHrs*tarifa.tarifa_entre_semana
        return monto
    else:
        for i in range(fecha_inicio.weekday(), fecha_final.weekday()):
            for j in range(fecha_inicio.hour, 24):
                cantHrs = cantHrs +1
                monto = tarifa_entre_semana*cantHrs
        return monto
    print "Duro %s hr en el servicio. Se le cancelan Bs.%s " %(cantHrs, monto)        