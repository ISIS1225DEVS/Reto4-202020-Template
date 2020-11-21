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
import math
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
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
    try:
        citibike = {'graph': None,
                    'stops': None,
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
    latitude1 = float(trip['start station latitude'])
    longitude1 = float(trip['start station longitude'])
    latitude2 = float(trip['end station latitude'])
    longitude2 = float(trip['end station longitude'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addStop(citibike, origin, latitude1, longitude1)
    addStop(citibike, destination, latitude2, longitude2)

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
    return citibike

def addStop(citibike, stationid, latitude, longitude):
    if not m.contains(citibike['stops'], stationid):
        m.put(citibike['stops'], stationid, (latitude,longitude))
    return citibike

# ==============================
# Funciones de consulta
# ==============================

def req1 (citibike, station1, station2):
    sc = scc.KosarajuSCC(citibike['graph'])
    num = scc.connectedComponents(sc)
    strongly = scc.stronglyConnected(sc, station1, station2)
    return (num,strongly)

def req3 (citibike):
    lstArrival = []
    lstDeparture = []
    diccLeast = {}
    lstLeast = []

    for i in citibike['graph']['indegree']['table']['elements']:
        if i['key'] != None:
            diccLeast[i['key']] = i['value']
            if len(lstArrival) < 3:
                lstArrival.append(i)
            else : 
                for j in lstArrival:
                    if i == j:
                        j['value'] = j.get('value') + i['value']
                    elif i['value'] > j['value']:
                        lstArrival.append(i)
                        lstArrival.remove(j)
                        break


    for i in citibike['graph']['vertices']['table']['elements']:
        if i['key'] != None:
            if i['key'] not in diccLeast.keys():
                diccLeast[i['key']] = lt.size(i['value'])
            else:
                diccLeast[i['key']] = diccLeast.get(i['key']) + lt.size(i['value'])

            if len(lstDeparture) < 3:
                lstDeparture.append({'key': i['key'], 'value':lt.size(i['value'])})
            else : 
                for j in lstDeparture:
                    if lt.size(i['value']) > j['value']:
                        lstDeparture.append({'key': i['key'], 'value':lt.size(i['value'])})
                        lstDeparture.remove(j)
                        break
    
    for i in diccLeast:
        if len(lstLeast) < 3:
                lstLeast.append((i,diccLeast[i]))
        else: 
            for j in lstLeast:
                if diccLeast[i] < j[1]:
                    lstLeast.append((i,diccLeast[i]))
                    lstLeast.remove(j)
                    break

    return (lstArrival,lstDeparture,lstLeast)

   
def req6(citibike, lat1, lon1, lat2, lon2):
    iterador = it.newIterator(m.keySet(citibike['stops']))
    radio_salida = 10000
    radio_llegada = 10000
    estacion_salida = ''
    estacion_llegada = ''
    while it.hasNext(iterador):
        llave = it.next(iterador)
        diccCoord = m.get(citibike['stops'],llave)
        lat = diccCoord['value'][0]
        lon = diccCoord['value'][1]
        haver_salida = (math.sin(math.radians((lat - lat1)) / 2))**2 \
                        + math.cos(math.radians(lat)) \
                        * math.cos(math.radians(lat)) \
                        * (math.sin(math.radians((lon - lon1)) / 2))**2
        d_s = 2*6371*math.asin(math.sqrt(haver_salida))
        if d_s <= radio_salida:
            radio_salida = d_s
            estacion_salida = diccCoord['key']

        haver_llegada = (math.sin(math.radians((lat - lat2)) / 2))**2 \
                        + math.cos(math.radians(lat)) \
                        * math.cos(math.radians(lat)) \
                        * (math.sin(math.radians((lon - lon2)) / 2))**2
        d_ll = 2*6371*math.asin(math.sqrt(haver_llegada))
        if d_ll <= radio_llegada:
            radio_llegada = d_ll
            estacion_llegada = diccCoord['key']

    print (estacion_llegada, estacion_salida)

    
    

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
