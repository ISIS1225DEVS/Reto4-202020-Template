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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
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
    tiempoInicial= input("Ingrese su tiempo incial disponible para un viaje: ")
    tiempoFinal= input("Ingrese su tiempo final disponible para un viaje: ")
    id_salida= input("Ingrese el id de la estacion de partida: ")
    i=0
    respuesta= controller.RutasCirculares(cont, id_salida, tiempoInicial, tiempoFinal)
    
    iter=it.newIterator(respuesta)
    i=0
    print("Ruta #"+"\t"+"\t"+"ESTACION INCIAL"+"\t"+"\t"+"ESTACION FINAL"+"\t"+"\t"+"DURACION")
    print("-------------------------------------------------------")
    while it.hasNext(iter):
        ruta_circular= it.next(iter)
        cantidad_rutas=lt.size(ruta_circular) 
        iter2=it.newIterator(ruta_circular)
        while it.hasNext(iter2):
            informacion= it.next(iter2)
            nombre= informacion['estacion1']['value']
            nombre2=informacion['estacion2']['value']
            duracion= informacion['duracion']
            print(str(i)+"\t"+"\t"+ nombre+"\t"+"\t"+ nombre2+"\t"+"\t"+str(duracion))
            
            # nombre=informacion['estacion1']]['value']
            # print(nombre)
            i+=1
    print("Rutas Circulares encontradas: "+ str(cantidad_rutas))

    # imprimirReq2(respuesta[0], respuesta[1], tiempoInicial, tiempoFinal)
    
# def Requerimiento3():

def Requerimiento4():
    estacion = input(str("Ingrese la estación desde la cual va a salir: "))
    tiempo = input(str("Ingrese el tiempo máximo que desea demorarse: "))
    resp = controller.mejoresRutas(cont,estacion,tiempo)
    print("Camino más cortos en sus alrededores: "+str(resp))

# def Requerimiento5():

def Requerimiento6():
    centi = True
    while centi:
        latAct = input('Latitud Actual\n')
        lonAct = input('Longitud Actual\n')
        latDes = input('Latitud Destino\n')
        lonDes = input('Longitud Destino\n')
        try:
            latAct, lonAct, latDes, lonDes = float(latAct),float(lonAct),float(latDes),float(lonDes)
        except ValueError:
            print('Ingrese coordenadas validas')
        else:
            centi = False

    nearStationActual, nearStationDestiny, tripTime, stationList = controller.turistInteres(citibike, latAct, lonAct, latDes, lonDes)

    print(f'La estacion mas cercana a su ubicacion actual es: <{nearStationActual[1]}>')
    print(f'La estacion mas cercana a su ubicacion destino es: <{nearStationDestiny[1]}>')
    print(f'El tiempo estimado de viaje es: <{tripTime}>')
    print('La lista de estaciones en la ruta es:\n<')
    if stationList is not None:
        for item in range(lt.size(stationList)):
            station = lt.getElement(stationList, item)
            print(f'\t{item+1}) De {station[0]} a {station[1]}')
    else: print('\tNo hay estaciones de por medio')
    print('>')

def Requerimiento6():
    latitud_actual = input(str("Ingrese la latitud de su parada actual: "))
    longitud_actual = input(str("Ingrese la longitud de su parada actual: "))
    latitud_destino = input(str("Ingrese la latitud de su parada de destino: "))
    longitud_destino = input(str("Ingrese la longitud de su parada de destino: "))
    resp = controller.ruta_por_coordenadas(cont,latitud_actual,longitud_actual,latitud_destino,longitud_destino)
    print("La ruta más corta entre su ubicación actual es: "+str(resp))
    
    



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


