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
import timeit
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

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

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________
def loadTrips(bikes):
    
    for filename in os.listdir(cf.data_dir):    
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(bikes, filename)
    return bikes

def loadFile(bikes, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(bikes, trip)
    return bikes



# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def numSCC(analyzer):
    return model.numSCC(analyzer)

def sameCC(analyzer, station1, station2):
    return model.sameCC(analyzer, station1, station2)

def totalVertex(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalVertex(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def hallartop3(analyzer,vertice):
    """
    Encontrar Top3 salida +
    """
    return model.Analizar_Top_Entry(analyzer,vertice)

def minimunEdges(analyzer):
    """
    Encontrar estaciones con menos arcos
    """
    return model.Never_top(analyzer)

def tripsyear(analyzer,numero):
    return model.getTripsFecha(analyzer,numero)

def RutaCircular(analyzer, vertex):
    return model.RutaCircular(analyzer, vertex)

def ruta(analyzer, startvertice, finalvertice):
    return model.hallar_ruta(analyzer, startvertice, finalvertice)