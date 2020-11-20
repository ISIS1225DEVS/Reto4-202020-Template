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
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------
def newAnalyzer():
    try:
        citibike = {'graph': None,
                    'stops': None,
                    'pairs': None
                    #'components': None,
                    #'paths': None
                    }

        citibike['stops'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareStations)
        citibike['pairs'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=comparePairs)

        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo

def addTrip(citibike, trip):
    """
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addPairs(citibike, origin, destination)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['graph'], stationid):
            gr.insertVertex(citibike ['graph'], stationid)
    return citibike

def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(citibike['graph'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['graph'], origin, destination, duration)
    else:
        prev_duration = int(ed.weight(edge))
        duration += prev_duration
        ed.updateWeight(edge, duration)

    return citibike

def addPairs(citibike, origin, destination):
    # edge = gr.getEdge(citibike['graph'], origin, destination)
    repetitions = 0
    pair = str(origin)+','+str(destination) # Creo la llave compuesta por: 
                                            # string con los ids de las estaciones
                                            # de origen concatenadas y separadas
                                            # por una coma ','
    repetitions = 0
    entry = me.newMapEntry(pair, repetitions)
    
    if entry['value'] >= 1:
        repetitions = entry['value'] + 1
        me.setValue(entry, repetitions)
        print(entry)
        
    else:
        repetitions = 1
        entry = me.newMapEntry(pair, repetitions)
        me.setKey(entry,pair)

    #print(m.get(citibike['pairs'], pair))
    return citibike

def avgDuration(citibike):
    """
    Actualiza el valor de los arcos al promedio de la duración de los
    viajes entre dos estaciones
    """
    edges = gr.edges(citibike['graph'])
    iterator = it.newIterator(edges)

    while it.hasNext(iterator):
        element = it.next(iterator)
        pair = str(element['vertexA']) + ',' + str(element['vertexB'])
        #entry = m.get(citibike['pairs'], pair)
        #repetitions = entry['value']
        #average = element['weight']/repetitions
    return citibike

# ==============================
# Funciones de consulta
# ==============================

def req1 (citibike, station1, station2):
    sc = scc.KosarajuSCC(citibike['graph'])
    num = scc.connectedComponents(sc)
    strongly = scc.stronglyConnected(sc, station1, station2)
    return (num,strongly)

def numSCC(graph):
    sc = scc.KosarajuSCC(graph['graph'])
    return scc.connectedComponents(sc)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

# ==============================
# Funciones Helper
# ==============================

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def comparePairs(id1, id2):
    if (id1 == id2):
        return 0
    else:
        return 1
