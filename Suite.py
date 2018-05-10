"""
Test Suite para la funcion calcularPrecio.
Usa la metodologia de casos de pruebas por fronteras.

@author: German Robayo 14-10924
"""

import unittest
import datetime
from decimal import Decimal
from Tarifa import Tarifa
from calcularPrecio import calcularPrecio


class TestTarifa(unittest.TestCase):
    '''
    Prueba la clase Tarifa, mas que todo se encarga que
    los argumentos son pasados correctamente
    '''
    failure_msg = 'Tarifa no deberia aceptar parametros no enteros'

    def test_primer_argumento(self):
        # Prueba que el primer argumento debe ser tipo entero,
        # en caso contrario, lanza un error ValueError
        self.assertRaises(TypeError, Tarifa, "hola", Decimal(1))
        self.assertRaises(TypeError, Tarifa, [], Decimal(2))
        tarifa = Tarifa(Decimal(2), Decimal(2)) # Esto no deberia lanzar error pues 2 es int

    def test_segundo_argumento(self):
        # Igual que el anterior, pero con el segundo argumento
        self.assertRaises(TypeError, Tarifa, Decimal(1), "hola")
        self.assertRaises(TypeError, Tarifa, Decimal(1), [])
        tarifa = Tarifa(Decimal(2), Decimal(2))

    def test_numeros_negativos(self):
        self.assertRaises(ValueError, Tarifa, Decimal(-1), Decimal(1))
        self.assertRaises(ValueError, Tarifa, Decimal(1), Decimal(-11))

class TestCalcularPrecio(unittest.TestCase):
    """
    Casos de pruebas para la funcion calcularPrecio
    """

    # todas las pruebas usaran el mismo objeto Tarifa
    def setUp(self):
        self.tarifa_entre_semana = Decimal(40)
        self.tarifa_fin_semana = Decimal(50)
        self.lunes = {
            'day': 7,
            'month': 5,
            'year': 2018
        }
        self.domingo = {
            'day': 13,
            'month': 5,
            'year': 2018
        }
        self.tarifa = Tarifa(self.tarifa_entre_semana, self.tarifa_fin_semana)

    # Caso borde: 15min
    def test_quince_minutos_exactos_entre_semana(self):
        fecha_inicio = datetime.datetime(**self.lunes)
        quince_minutos = datetime.timedelta(minutes=15)
        periodo_trabajo = [fecha_inicio, fecha_inicio + quince_minutos]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo), self.tarifa_entre_semana)

    def test_quince_minutos_exactos_fin_de_semana(self):
        fecha_inicio = datetime.datetime(**self.domingo)
        quince_minutos = datetime.timedelta(minutes=15)
        periodo_trabajo = [fecha_inicio, fecha_inicio + quince_minutos]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo), self.tarifa_fin_semana)

    def test_tipos_argumentos(self):
        today = datetime.datetime.today()
        un_segundo = datetime.timedelta(seconds=1)
        antes = today - un_segundo
        despues = today + un_segundo
        # primer argumento debe ser tarifa
        self.assertRaises(TypeError, calcularPrecio, [1,2], [today, despues])
        self.assertRaises(TypeError, calcularPrecio, object(), [today, despues])
        # segundo argmento debe ser lista de datetimes
        self.assertRaises(TypeError, calcularPrecio, self.tarifa, [1, despues])
        self.assertRaises(TypeError, calcularPrecio, self.tarifa, [today, 1])
        # segundo argumento debe cumplir que el periodo debe tener sentido
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [today, antes])
        # deberia lanzar un ValueError cuando el segundo parametro
        # sea una lista de longitud distinta a 2
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [])
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [today])
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [today, today, today])

    def test_menor_quince_minutos(self):
        fecha_inicio = datetime.datetime(**self.domingo)
        catorce_minutos_y_pico = datetime.timedelta(minutes=14, seconds=59)
        periodo_trabajo = [fecha_inicio, fecha_inicio + catorce_minutos_y_pico]
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, periodo_trabajo)
        # Esto no deberia lanzar ValueError
        calcularPrecio(self.tarifa, [fecha_inicio, fecha_inicio + datetime.timedelta(days=1) + catorce_minutos_y_pico])

    def test_maximo_7_dias(self):
        # las dos siguientes fechas presentan un rango valido
        fecha_inicio = datetime.datetime(**self.lunes)
        fecha_final = datetime.datetime(**self.domingo)
        dias = []
        for i in range(1, 7):
            dias.append(datetime.timedelta(days=i))
        # lunes a lunes
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [fecha_inicio, fecha_final + dias[0]])
        # martes a martes
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [fecha_inicio + dias[0], fecha_final + dias[1]])
        # martes al jueves de la siguiente
        self.assertRaises(ValueError, calcularPrecio, self.tarifa, [fecha_inicio + dias[1], fecha_final + dias[2]])

    def test_hora_y_quince_minutos(self):
        fecha_inicio = datetime.datetime(**self.domingo)
        hora_y_quince_minutos = datetime.timedelta(hours=1, minutes=15)
        periodo_trabajo = [fecha_inicio, fecha_inicio + hora_y_quince_minutos]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo), self.tarifa_fin_semana * 2)
        fecha_inicio = datetime.datetime(**self.lunes)
        periodo_trabajo = [fecha_inicio, fecha_inicio + hora_y_quince_minutos]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo), self.tarifa_entre_semana * 2)

    def test_2_dias_alternados(self):
        fecha_inicio = datetime.datetime(**self.domingo)
        un_dia = datetime.timedelta(days=2)
        periodo_trabajo = [fecha_inicio, fecha_inicio + un_dia]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo),
            self.tarifa_entre_semana * 24 + self.tarifa_fin_semana * 24)

    def test_medio_domingo_medio_lunes(self):
        doce_horas = datetime.timedelta(hours=12)
        fecha_inicio = datetime.datetime(**self.domingo) + doce_horas
        periodo_trabajo = [fecha_inicio, fecha_inicio + doce_horas * 2]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo),
            self.tarifa_entre_semana * 12 + self.tarifa_fin_semana * 12)

if __name__ == '__main__':
    unittest.main()
