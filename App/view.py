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

# ___________________________________________________
#  Variables
# ___________________________________________________
import controller

servicefile = '201801-1-citibike-tripdata.csv'
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar datos de Citibike")
    print("3- REQUERIMIENTO 1")
    print("4- REQUERIMIENTO 2")
    print("5- REQUERIMIENTO 3")
    print("6- REQUERIMIENTO 4")
    print("7- REQUERIMIENTO 5")
    print("8- REQUERIMIENTO 6")
    print("0- Salir")
    print("*******************************************")


def CargarDatos(): #CARGAR INFORMACION
    print("\nCargando información de transporte de singapur ....")
    # para todos los archivos
    #controller.loadTrips(cont)
    # para uno solo
    controller.loadFile(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalVertex(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def Requerimiento1():
    Station1= input("Ingrese una estacion de interés: ")
    Station2= input("Ingrese otra estacion de interés: ")
    print('El número de componentes conectados es: ' + 
            str(controller.numSCC(cont)))
    print("Entre "+str(Station1)+" y "+str(Station2)+": "+
            str(controller.sameCC(cont,Station1,Station2))+ "que pertenezcan al mismo cluster")

def Requerimiento2():
    
def Requerimiento3();
def Requerimiento4():

def Requerimiento5():

def Requerimiento6():



"""
Menu principal
"""
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
        executiontime = timeit.timeit(CargarDatos, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(Requerimiento1, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(Requerimiento2, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(Requerimiento3, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(Requerimiento4, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(Requerimiento5, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(Requerimiento6, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)


