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
        try:
            tarifa = Tarifa("hola", 1)
            self.fail(self.failure_msg)
        except ValueError:
            pass

        try:
            tarifa = Tarifa([], 2)
            self.fail(self.failure_msg)
        except ValueError:
            pass

        tarifa = Tarifa(2, 2) # Esto no deberia lanzar error pues 2 es int


    def test_segundo_argumento(self):
        # Igual que el anterior, pero con el segundo argumento
        try:          
            tarifa = Tarifa(1, "hola")
            self.fail(self.failure_msg)
        except ValueError:
            pass

        try:
            tarifa = Tarifa(1, [])
            self.fail(self.failure_msg)
        except ValueError:
            pass

        tarifa = Tarifa(2, 2) # Esto no deberia lanzar error pues 2 es int

    def test_atributos_son_decimal(self):
        # Prueba que los tipos de los atributos sean decimal.
        tarifa = Tarifa(40, 40)
        self.assertEqual(type(tarifa.tarifa_entre_semana), Decimal, 'tarifa_entre_semana debe ser de tipo decimal')
        self.assertEqual(type(tarifa.tarifa_fin_semana), Decimal, 'tarifa_fin_semana debe ser de tipo decimal')

class TestCalcularPrecio(unittest.TestCase):
    """
    Casos de pruebas para la funcion calcularPrecio
    """

    # todas las pruebas usaran el mismo objeto Tarifa
    def setUp(self):
        self.tarifa_entre_semana = 40
        self.tarifa_fin_semana = 50
        self.tarifa = Tarifa(self.tarifa_entre_semana, self.tarifa_fin_semana)

    # Caso borde: 15min
    def testQuinceMinutosExactos(self):
        # El 9 de mayo del 2018 fue un dia entre semana
        fecha_inicio = datetime.datetime(year=2018, month=5, day=9)
        quince_minutos = datetime.timedelta(minutes=15)
        periodo_trabajo = [fecha_inicio, fecha_inicio + quince_minutos]
        self.assertEqual(calcularPrecio(self.tarifa, periodo_trabajo), self.tarifa_entre_semana)


if __name__ == '__main__':
    unittest.main()
