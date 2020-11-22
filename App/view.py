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
from App import model
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

citibike1 = 'Data\\201801-1-citibike-tripdata.csv'
citibike2 = 'Data\\201801-1-citibike-tripdata.csv'
citibike3 = 'Data\\201801-1-citibike-tripdata.csv'
citibike4 = 'Data\\201801-1-citibike-tripdata.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("------------------------------------------------------")
    print("Bienvenido al analizador de datos de CitiBike")
    print("------------------------------------------------------\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información CitiBike")
    print("3- Cantidad de clusters de viajes")
    print("4- Ruta turística cirular")
    print("5- Estaciones críticas")
    print("6- Ruta turística por resistencia")
    print("7- Recomendador de rutas")
    print("8- Ruta de interés turístico")
    print("9- Identificación de estaciones para publicidad")
    print("10- Identificación de bicicletas para mantenimiento")
    print("0- Salir")
    print("------------------------------------------------------")


def optionTwo():
    pass

def optionThree():
    pass

def optionFour():
    pass

def optionFive():
    retorno = controller.ejecutarreq3(cont)
    print ('Las Estaciones con más llegadas son: ', retorno[0])
    print ('Las Estaciones con más salidas son: ', retorno[1])
    print ('Las Estaciones con menos llegadas y salidas son: ', retorno[2])

def optionSix():
    pass

def optionSeven():
    pass

def optionEight():
    model.req6(cont, 41,-75,40,-74)

def optionNine():
    pass

def optionTen():
    pass

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:

        controller.loadTrips(cont)
        numedges = controller.totalConnections(cont)
        numvertex = controller.totalStops(cont)
        scc = controller.numSCC(cont)
        print('Numero de vertices: ' + str(numvertex))
        print('Numero de arcos: ' + str(numedges))
        print('Numero de elementos fuertemente conectados: ' + str(scc))

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

    elif int(inputs[0]) == 10 or inputs == 'C':
        executiontime = timeit.timeit(optionTen, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)