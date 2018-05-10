# -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import unittest
from decimal import Decimal
from Tarifa import Tarifa

def es_fin_de_semana(date):
    return 5 <= date.weekday() <= 6

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

    diferencia = fecha_final - fecha_inicio
    if (diferencia.days > 6):
        raise ValueError("ERROR: debe ser maximo 7 dias")

    if (diferencia.days == 0 and diferencia.seconds < 15 * 60):
        raise ValueError ("ERROR: debe durar al menos 15 minutes en el servicio")
    
    '''
    Caso_1: entra y sale en un mismo dia.
    '''
    fecha_actual = fecha_inicio
    monto_total = 0
    tarifa_entre_semana = tarifa.tarifa_entre_semana
    tarifa_fin_semana = tarifa.tarifa_fin_semana
    while fecha_actual < fecha_final:
        if es_fin_de_semana(fecha_actual):
            monto_total += tarifa_fin_semana
        else:
            monto_total += tarifa_entre_semana
        fecha_actual = fecha_actual + datetime.timedelta(hours=1)

    return monto_total
