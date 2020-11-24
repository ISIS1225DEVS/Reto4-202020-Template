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
from DISClib.ADT import map as m
assert config
from time import process_time
from DISClib.DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________



tripfile = '201801-1-citibike-tripdata.csv'
#tripfile = '201801-4-citibike-tripdata.csv'

initialStation = None
recursionLimit = 30000

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("-"*75)
    print("Bienvenido")
    print("1- Inicializar analizador y Carga archivo CSV")
    print("2- Cantidad de Clusters de viajes")
    print("3- Ruta turística Circular")
    print("4- Estaciones críticas")
    print("5- Ruta turística por resistencia")
    print("6- Recomendador de rutas")
    print("7- Ruta de interés turístico")
    print('8- Indentificación de estaciones para publicidad')
    print('9- Identificacion de bicicletas para mantenimiento')
    print("0- Salir")
    print("-"*75)


def cargaDatos(cont):
    print("\nCargando información de CitiBike ....")
    controller.loadFile(cont, tripfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStation(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    controller.cantidadClusters(cont, '0','0')
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))
    # controller.cantidadClusters(cont, '','')

def cantidadClusters(cont): #REQ 1
    estacion1= input('Dijite la primera estación: ')
    estacion2 = input('Dijite la segunda estación: ')
    data  = controller.cantidadClusters(cont, estacion1, estacion2)
    if data == -1:
        print('No existe alguna de las estaciones','-'*75)
    else:
        print('Hay ',data[0]['size'], ' clusters dentro del gráfo')
        if data[1] == True:
            print('La estacion ',estacion1, ' y la estacion ',estacion2, ' están en el mismo clúster')
        else:
            print('La estacion ',estacion1, ' y la estacion ',estacion2, ' no están en el mismo clúster')

def rutaTuristicaCircular(cont): #REQ 2
    print('Use estos nodos segun el archivo cargado (sugerencia) --> 1: 119,2: 195: ,3: 440,4: 3654')
    inicio = input('Dijite el inicio del rango en minutos: ')
    final = input('Dijite el final del rango en minutos: ')
    estacion = input('Digite el identificador de la estación de inicio: ')
    data = controller.rutaTuristicaCircular(cont, (inicio,final), estacion)
    if data == -1:
        print('No se halló ningun resultado','-'*75)
    else:
        if data != -1 and data[0] != 0:
            print('Se hallaron', data[0],' rutas posibles: ')
            for i in range(1,len(data)):
                string = []
                reves = []
                iterator = it.newIterator(data[i][0])
                while it.hasNext(iterator):
                    current = it.next(iterator)
                    string.append('vertice '+current['vertexA']+' -> vertice '+current['vertexB'])
                    reves.insert(0,'vertice '+current['vertexB']+' -> vertice '+current['vertexA'])
                string = ", ".join(string)
                reves = ", ".join(reves)
                print('Ruta número ',i,' de duración', data[i][1],'minutos: ', string,' -> ', reves)
        elif data == -1:
            print('No existe la estación','-'*75)
        elif data[0] == 0:
            print('No hay rutas','-'*75)

#def optionFive():
    

def optionFive(cont): #REQ 3
    data=controller.estacionesCriticas(cont)
    print('Las salidas mas usadas son:')
    cnt1=0
    cnt2=0
    cnt3=0
    for i in data[0]:
        if cnt1 <3:
            print('Estación:', i[0])
        cnt1+=1
    print('Las entradas más usadas son:')
    for i in data[1]:
        if cnt2 <3:
            print('Estación:', i[0])
        cnt2+=1
    print('Las estaciones menos usadas son:')
    for i in data[2]:
        if cnt3<3:
            print('Estación:', i[0])
        cnt3+=1

        
def rutaTuristicaResistencia(cont):   #REQ. 4
    time = int(input('Digita el tiempo límite: '))
    idstation = int(input('Digita la estación de inicio: '))
    data = controller.rutaTuristicaResistencia(cont, time, idstation)
    print('En el tiempo limite de ', time, ' se encontraron los siguientes recorridos: ')
    fin = data.keys()
    camino = ':'
    print(str(idstation) + ' --> ' + str(fin) + '   Peso: ' + str(camino))

"""
def optionSeven():   #REQ. 5 
   """ 

def optionSeven(cont):
    data=controller.rutaInteresTuristico(cont,"4.076727.216",'-7.198.848.395',"4.076727.216",'-7.198.848.395')        
    print(data) 
"""

#def optionSix():
    

#def optionSeven():
    
"""


def main():
    cont = None
    while True:
        printMenu()
        inputs = int(input('Seleccione una opción para continuar\n-> '))

        if inputs == 1:   #Inicio y carga
            t1_start = process_time() #tiempo inicial
            print("\nInicializando.....")
            tamaño = int(input("Digita el tamaño de las tablas de hash: "))
            carga = float(input("Digita el factor de carga: "))
            cont = controller.init(tamaño, carga)
            cargaDatos(cont)
            t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 2:   #Req. 1
            print("\nCantidad de Clusters de viajes")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                cantidadClusters(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

        elif inputs == 3:   #Req. 2
            print("\nRuta turística Circular")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                rutaTuristicaCircular(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
        
        elif inputs == 4:   #Req. 3
            print("\nEstaciones críticas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                t1_start = process_time() #tiempo inicial
                estacionesCriticas(cont)
                t1_stop = process_time() #tiempo final
            print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
        
        
        elif inputs == 5:   #Req. 4
            print("\nRuta turística por resistencia")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                rutaTuristicaResistencia(cont)

        elif inputs == 6:   #Req. 5
            print("\nRecomendador de rutas")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                destStation = input("Estación destino (Ej: 15151-10): ")
            executiontime = timeit.timeit(optionSix, number=1)
            print("Tiempo de ejecución: " + str(executiontime))

        elif inputs == 7:   #Req. 6
            print("\nRuta de interés turístico")
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                
                optionSeven(cont)
            
        
        elif inputs == 8:   #Req. 7*
            print('\nIndentificación de estaciones para publicidad')
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                print('lolazo xd')
        
        elif inputs == 9:   #Req. 8*
            print('\nIdentificacion de bicicletas para mantenimiento')
            if cont == None:
                print('¡KELLY CARGUE EL ARCHIVO PRIMERO!')
            else:
                print('lolalisimo xd')
        
        elif inputs == 0:   #Salir
            print('Cerrando el programa ...')
            sys.exit(0)
        
        else:
            print('Opción incorrecta .....')
main()
