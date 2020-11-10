"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

servicefile = '201801-1-citibike-tripdata.csv'
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("****************************************************")
    print("RETO No. 4 CitiBike")
    print("[ 1 ] Inicializar Analizador")
    print("[ 2 ] Cargar información de citibyke en newyork")
    print("[ 3 ] Cantidad de clusters de viajes")
    print("[ 4 ] Ruta turistica circular")
    print("[ 5 ] Estaciones criticas ")
    print("[ 6 ] Ruta turistisca por resistencia")
    print("[ 7 ] Recomendador de Rutas")
    print("[ 8 ] Ruta de interes turistico")
    print("[ 9 ] Identificacion de estaciones para publicidad")
    print("[10 ] Identificacion de bicicletas para mantenimiento")
    print("[ 0 ] Salir")
    print("****************************************************")


def optionTwo():
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))


def optionThree():
    print('Under construction.... ')

def optionFour():
    print('Under construction.... ')

def optionFive():
    print('Under construction.... ')

def optionSix():
    print('Under construction.... ')

def optionSeven():
    print('Under construction.... ')

def optionEight():
    print('Under construction.... ')

def optionNine():
    print('Under construction.... ')

def optionTen():
    print('Under construction.... ')

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando el controlador...")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionSix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionSeven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optionEight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionNine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))


    elif int(inputs[0]) == 10:
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)