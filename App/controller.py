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

import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init(tamaño, carga):
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer(tamaño, carga)
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadFile(analyzer, tripfile):
    """
    """
    print('Cargando archivo: ' + tripfile)
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")

    for trip in input_file:
        model.addTrip(analyzer, trip)

    lastservice = None
    for service in input_file:
        if lastservice is not None:
            sameservice = lastservice['tripduration'] == service['tripduration']
            samedirection = lastservice['tripduration'] == service['tripduration']
            if sameservice and samedirection:
                model.addStopConnection(analyzer, lastservice, service)
        lastservice = service
    model.addRouteStation(analyzer, trip)
    
    return analyzer


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStation(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStation(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


# ___________________________________________________
#  Requerimientos
# ___________________________________________________

def cantidadClusters(cont,id1,id2):  #Req. 1
    return model.cantidadClusters(cont,id1,id2)

def rutaTuristicaCircular(cont, time, startStation):   #Req. 2
    return model.rutaTuristicaCircular(cont, time, startStation)
 
def estacionesCriticas(cont):   #Req. 3
    return model.estacionesCriticas(cont)

def rutaTuristicaResistencia(cont, time, idstation):   #Req. 4
    return model.rutaTuristicaResistencia(cont, time, idstation)
"""
def recomendadorRutas(cont, edades):   #Req. 5
    return model.recomendadorRutas(cont, edades)

def rutaInteresTuristico(cont, latlocal, longlocal, latfinal, longfinal):   #Req. 6
    return model.rutaInteresTuristico(cont, latlocal, longlocal, latfinal, longfinal)

def estacionesPublicidad(cont, rango):   #Req. 7*
    return model.estacionesPublicidad(cont, rango)

def bicicletasMantenimmiento(cont, idbike, fecha):   #Req. 8*
    return model.bicicletasMantenimmiento(cont, idbike, fecha)
"""