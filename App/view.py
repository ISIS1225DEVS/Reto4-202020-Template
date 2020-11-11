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
# ___________________________________________________
#  Variables
# ___________________________________________________

file1 = '201801-1-citibike-tripdata.csv'
file2 = '201801-2-citibike-tripdata.csv'
file3 = '201801-3-citibike-tripdata.csv'
file4 = '201801-4-citibike-tripdata.csv'
totalFiles = [file1]


# ___________________________________________________
#  Menu principal
# ___________________________________________________

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de rutas citybike")
    print("3- Cantidad de clusters de Viajes")
    print("4- Ruta turística Circular")
    print("5- Estaciones críticas ")
    print("6- Ruta turística por resistencia ")
    print("7- Recomendador de Rutas  ")
    print("8- Ruta de interés turístico  ")
    print("9- Identificación de Estaciones para Publicidad ")
    print("10- Identificación de Bicicletas para Mantenimiento ")
    print("0- Salir")
    print("*******************************************")

def optionTwo():
    print("\nCargando información de rutas citybike ....")
    controller.loadFiles(analyzer, totalFiles)
    numTrips = controller.totalTrips(analyzer)
    numedges = controller.totalConnections(analyzer)
    numvertex = controller.totalStations(analyzer)
    print('Numero de viajes: ' + str(numTrips))
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))


def optionThree():
    try:
        print('El número de componentes conectados es: ' +
              str(controller.connectedComponents(analyzer)))
        if id1.isdigit() and id2.isdigit():
            connected = controller.verticesSCC(analyzer, id1, id2)
            if connected:
                print("Las estaciones con codigo "+id1+" y "+id2+" pertenecen al mismo cluster")
            elif connected is None:
                print("No se puede hacer la busqueda, intente con estaciones diferentes")
            else:
                print("Las estaciones con codigo "+id1+" y "+id2+" no pertenecen al mismo cluster")
        else:
            print("Los ID tienen que ser un numero natural, intente con entradas diferentes")
    except:
            print("Hubo un error en la busqueda")

def optionFour():
    pass

def optionFive():
    pass

def optionSix():
    pass

def optionSeven():
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
        analyzer = controller.init()
        print("\nAnalizador iniciado con exito")

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        id1 = input('Ingrese el ID de la primera estacion: ' )
        id2 = input('Ingrese el ID de la segunda estacion: ' )
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

    else:
        sys.exit(0)
sys.exit(0)
