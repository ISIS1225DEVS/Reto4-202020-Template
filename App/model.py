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
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

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

   
def req6(analyzer, lat_centro, lon_centro, radio):

    iterator = it.newIterator(analyzer['accidentes'])
    while it.hasNext(iterator):
        element = it.next(iterator)
        haver_entrada = (math.sin(math.radians((float(element['Start_Lat']) - lat_centro)) / 2))**2 \
                        + math.cos(math.radians(float(element['Start_Lat']))) \
                        * math.cos(math.radians(float(element['Start_Lat']))) \
                        * (math.sin(math.radians((float(element['Start_Lng']) - lon_centro)) / 2))**2
        d = 2*6371*math.asin(math.sqrt(haver_entrada))
        if d <= radio:
            total += 1
            occurreddate = element['Start_Time']
            accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
            if accidentdate.weekday() == 0:
                dias['Lunes'] += 1
            elif accidentdate.weekday() == 1:
                dias['Martes'] += 1
            elif accidentdate.weekday() == 2:
                dias['Miercoles'] += 1
            elif accidentdate.weekday() == 3:
                dias['Jueves'] += 1
            elif accidentdate.weekday() == 4:
                dias['Viernes'] += 1
            elif accidentdate.weekday() == 5:
                dias['Sabado'] += 1
            elif accidentdate.weekday() == 6:
                dias['Domingo'] += 1
    return (total, dias)
'''
'''
    for i in citibike['graph']['outdegree']['table']['elements']:
        if i['key'] != None:
            if i['key'] not in diccLeast.keys():
                diccLeast[i['key']] = i['value']
            else:
                diccLeast[i['key']] = diccLeas.get(i['key']) + i['value']
            if len(lst) < 4:
                lstDeparture.append(i)
            else : 
                for j in lstDeparture:
                    if i['value'] > j['value']:
                        lstDeparture.append(i)
                        lstDeparture.remove(j)
    
    

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
