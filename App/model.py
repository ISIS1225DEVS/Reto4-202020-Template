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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import edge as e
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador
   trips: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'trips': None,
                    'components': None,
                    "NumTrips": 0
                    }

        analyzer['trips'] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1500,
                                  comparefunction=compareStations)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(analyzer, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)
    analyzer["NumTrips"] += 1

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(analyzer ["trips"], stationid):
            gr.insertVertex(analyzer ["trips"], stationid)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer ["trips"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["trips"], origin, destination, duration)
    else:
        weight = e.weight(edge)
        prom = (duration + weight)/2
        edge['weight'] = prom
    return analyzer


# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['trips'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer, station1, station2):
    """
    """
    sccDict = analyzer['components']
    return scc.stronglyConnected(sccDict, station1, station2)

def totalStations(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['trips'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['trips'])

def totalTrips(analyzer):
    """
    Retorna el total viajes
    """
    return analyzer['NumTrips']

def stationInGraph(analyzer, stationId):
    """
    Revisa que la estacion se encuentre en el grafo
    """
    graph = analyzer["trips"]
    return gr.containsVertex(graph, stationId)

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(satationId, keyvalueStat):
    """
    Compara dos estaciones
    """
    Statcode = keyvalueStat['key']
    if (satationId == Statcode):
        return 0
    elif (satationId > Statcode):
        return 1
    else:
        return -1

