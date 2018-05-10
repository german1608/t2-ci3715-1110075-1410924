# -*- coding: utf-8 -*-
#!/usr/bin/python
from decimal import Decimal
import datetime


class Tarifa():


    def __init__(self, tarifa_entre_semana, tarifa_fin_semana):
        if not isinstance(tarifa_entre_semana, Decimal):
            raise TypeError ("tarifa_entre_semana debe ser Decimal")
        if not isinstance(tarifa_fin_semana, Decimal):
            raise TypeError ("tarifa_fin_semana debe ser Decimal")
        if (Decimal(tarifa_entre_semana) < 0):
        	raise ValueError (("tarifa_entre_semana no debe ser negativa"))
        if (Decimal(tarifa_fin_semana) < 0):
        	raise ValueError (("tarifa_fin_semana no debe ser negativa"))
        self.tarifa_entre_semana = tarifa_entre_semana
        self.tarifa_fin_semana = tarifa_fin_semana