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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# import datetime

# # using now() to get current time
# current_time = datetime.datetime.now()
# print ("Year : ", end = "")
# print (current_time.year)

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
        citibike['dates'] = om.newMap(omaptype='RBT',
                                   comparefunction=compareDates)

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
    edad = 2020 - int(trip['birth year'])
    type = trip['usertype']
    date = trip['starttime'][:10]
    bikeId = trip['bikeid']
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
    addStop(citibike, origin, latitude1, longitude1, edad, 's', type)
    addStop(citibike, destination, latitude2, longitude2, edad, 'll', type)
    addConnection(citibike, origin, destination, duration)
    addPairs(citibike, origin, destination)
    addDate(citibike, date, bikeId, origin, destination, duration)

def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike['graph'], stationid):
            gr.insertVertex(citibike['graph'], stationid)
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

def addStop(citibike, stationid, latitude, longitude, edad, s_ll, type):
    if m.contains(citibike['stops'], stationid):
        retorno = m.get(citibike['stops'], stationid)['value']
        m.remove(citibike['stops'], stationid)
    else:
        retorno = [latitude,longitude,{'0-10':0,
                                '11-20':0,
                                '21-30':0,
                                '31-40':0,
                                '41-50':0,
                                '51-60':0,
                                '60+':0,
                                'total':0}, {'0-10':0,
                                        '11-20':0,
                                        '21-30':0,
                                        '31-40':0,
                                        '41-50':0,
                                        '51-60':0,
                                        '60+':0,
                                        'total':0}, type]
    if s_ll == 's':
        a = 2
    else:
        a = 3

    if edad in range(0,11):
        nuevo = retorno[a].get('0-10') + 1
        retorno[a]['0-10'] = nuevo
    elif edad in range(11,21):
        nuevo = retorno[a].get('11-20') + 1
        retorno[a]['11-20'] = nuevo
    elif edad in range(21,31):
        nuevo = retorno[a].get('21-30') + 1
        retorno[a]['21-30'] = nuevo
    elif edad in range(31,41):
        nuevo = retorno[a].get('31-40') + 1
        retorno[a]['31-40'] = nuevo
    elif edad in range(41,51):
        nuevo = retorno[a].get('41-50') + 1
        retorno[a]['41-50'] = nuevo
    elif edad in range(51,61):
        nuevo = retorno[a].get('51-60') + 1
        retorno[a]['51-60'] = nuevo
    else:
        nuevo = retorno[a].get('60+') + 1
        retorno[a]['60+'] = nuevo

    nuevo = retorno[a].get('total') + 1
    retorno[a]['total'] = nuevo

    m.put(citibike['stops'], stationid, retorno)

    return citibike

def addPairs(citibike, origin, destination):
    pair = str(origin) + ',' + str(destination) # Creo la llave compuesta por:
                                            # string con los ids de las estaciones
                                            # de origen concatenadas y separadas
                                            # por una coma ','

    existe = m.contains(citibike['pairs'], pair)
    # print(existe)
    if not existe:
        # entry = me.newMapEntry(pair, 1)
        m.put(citibike['pairs'], pair, 1)
    else:
        entry = m.get(citibike['pairs'], pair)
        value = me.getValue(entry)
        m.put(citibike['pairs'], pair, value + 1)

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
        entry = m.get(citibike['pairs'], pair)

        repetitions = entry['value']
        average = element['weight']/repetitions
        # if str(element['vertexA']) == '72':
        #    print(average)
        ed.updateWeight(element, average)
    return citibike

def addDate(citibike, date, bikeId, origin, destination, duration):
    if not om.contains(citibike['dates'], date): # No está la fecha
        ids = {}                                 # Agregar info
        stops = lt.newList(cmpfunction=compareIds)
        lt.addFirst(stops, origin)
        lt.addFirst(stops, destination)
        ids[bikeId] = (duration, stops)
        om.put(citibike['dates'], date, ids)
    else:                                       # Está la fecha
        value = om.get(citibike['dates'], date)

        # print(value.keys())
        # print(bikeId)
        if bikeId not in value.keys():          # No está la bici
            stops = lt.newList(cmpfunction=compareIds) # Agregar bici
            lt.addFirst(stops, origin)
            lt.addFirst(stops, destination)
            value[bikeId] = (duration, stops)
        else:                                   # Está la bici
            # print(value[bikeId])
            uso = value[bikeId][0]
            value[bikeId] = (uso + duration, value[bikeId][1])
            if not lt.isPresent(value[bikeId][1], origin): # No está la estación
                lt.addLast(value[bikeId][1], origin)
            else:
                pass
            if not lt.isPresent(value[bikeId][1], destination): # No está la estación
                lt.addLast(value[bikeId][1], destination)
            else:
                pass




# ==============================
# Funciones de consulta
# ==============================

def req1 (citibike, station1, station2):
    sc = scc.KosarajuSCC(citibike['graph'])
    num = scc.connectedComponents(sc)
    strongly = scc.stronglyConnected(sc, station1, station2)
    return (num,strongly)

def req2(citibike, disponible, station1):
    fixed = station1
    search = dfs.DepthFirstSearchCycles(citibike['graph'], station1, fixed)
    return search['total']

def req3 (citibike):
    lstArrival = []
    lstDeparture = []
    lstLeast = []

    iterador = it.newIterator(m.keySet(citibike['stops']))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(citibike['stops'],element)
        salida = dicc['value'][2]['total']
        llegada = dicc['value'][3]['total']
        ambas = salida + llegada

        if len(lstArrival) < 3:
                lstArrival.append({'key':dicc['key'], 'value':salida})
                lstDeparture.append({'key':dicc['key'], 'value':llegada})
                lstLeast.append({'key':dicc['key'], 'value':ambas})
        else:
            for j in lstArrival:
                if salida > j['value']:
                    lstArrival.append({'key':dicc['key'], 'value':salida})
                    lstArrival.remove(j)
                    break
            for j in lstDeparture:
                if llegada > j['value']:
                    lstDeparture.append({'key':dicc['key'], 'value':llegada})
                    lstDeparture.remove(j)
                    break
            for j in lstLeast:
                if ambas < j['value']:
                    lstLeast.append({'key':dicc['key'], 'value':ambas})
                    lstLeast.remove(j)

    return (lstArrival,lstDeparture,lstLeast)


def req4(citibike, resis, inicio):
    "William Mendez"
    pendientes = [] #str del id
    encontrados = {} #{llegada: (origen, duracion)}
    primeros = gr.adjacents(citibike['graph'], inicio)

    iterator = it.newIterator(primeros)
    while it.hasNext(iterator):
        element = it.next(iterator)
        # print(element)
        durac = ed.weight(gr.getEdge(citibike['graph'], inicio, element)) / 60
        if  durac <= resis:
            encontrados[element] = (inicio, round(durac, 2))
            pendientes.append(element)

    while len(pendientes) > 0:
        for i in pendientes:
            adya = gr.adjacents(citibike['graph'], i)
            if adya['size'] != 0:
                # print(adya)

                iterator = it.newIterator(adya)
                while it.hasNext(iterator):
                    element = it.next(iterator)
                    # print(element)
                    if element not in encontrados.keys() and \
                         element not in pendientes and element != inicio:

                        durac = 0
                        llega = i

                        # print(i, element)
                        while llega != inicio:
                            # print(durac)
                            durac += encontrados[llega][1]
                            llega = encontrados[llega][0]
                            # print(durac)

                        relativ = ed.weight(gr.getEdge(citibike['graph'], i,
                                            element)) / 60
                        # print(durac, relativ, durac + relativ, resis)
                        if  (durac + relativ) <= resis:
                            encontrados[element] = (i, round(relativ, 2))
                            pendientes.append(element)

            pendientes.remove(i)
            # print(len(pendientes))
    # print(encontrados)
    return encontrados

def req5 (citibike, edad):

    if edad in range(0,11):
        key = '0-10'
    elif edad in range(11,21):
        key = '11-20'
    elif edad in range(21,31):
        key = '21-30'
    elif edad in range(31,41):
        key = '31-40'
    elif edad in range(41,51):
        key = '41-50'
    elif edad in range(51,61):
        key = '51-60'
    else:
        key = '60+'

    iterador = it.newIterator(m.keySet(citibike['stops']))
    estacion_salida = 'Ninguna'
    max_salida = 0
    estacion_llegada = 'Ninguna'
    llegada_2 = 'Ninguna'
    max_llegada = 0
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(citibike['stops'],element)
        salida = dicc['value'][2]
        llegada = dicc['value'][3]
        if salida[key] > max_salida:
            max_salida = salida[key]
            estacion_salida = dicc['key']
        if llegada[key] > max_llegada:
            llegada_2 = estacion_llegada
            max_llegada = llegada[key]
            estacion_llegada = dicc['key']

    if estacion_llegada == estacion_salida:
        estacion_llegada = llegada_2

    ruta = []
    dijsktra = djk.Dijkstra(citibike['graph'],str(estacion_salida))
    if djk.hasPathTo(dijsktra, estacion_llegada):
        if djk.hasPathTo(dijsktra, estacion_llegada):
            ruta_lt = djk.pathTo(dijsktra, estacion_llegada)
            iterador = it.newIterator(ruta_lt)
            ruta.append(estacion_salida)
            while it.hasNext(iterador):
                element = it.next(iterador)
                ruta.append(element['vertexB'])
    else:
        ruta = 'No hay ruta'
    return (estacion_salida, estacion_llegada, ruta)

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


    if estacion_llegada != '' and estacion_salida != '':
        ruta = []
        dijsktra = djk.Dijkstra(citibike['graph'],str(estacion_salida))
        if djk.hasPathTo(dijsktra, estacion_llegada):
            ruta_lt = djk.pathTo(dijsktra, estacion_llegada)
            iterador = it.newIterator(ruta_lt)
            ruta.append(estacion_salida)
            while it.hasNext(iterador):
                element = it.next(iterador)
                ruta.append(element['vertexB'])
    else:
        ruta = 'No hay ruta'

    return (estacion_salida, estacion_llegada, ruta)

def req7 (citibike, rango):
    lista = gr.edges(citibike['graph'])
    iterador = it.newIterator(lista)
    maximo = 0
    pareja = 'No hay'
    while it.hasNext(iterador):
        elemento = it.next(iterador)
        diccA = m.get(citibike['stops'],elemento['vertexA'])
        diccB = m.get(citibike['stops'],elemento['vertexB'])
        if diccA['value'][4] == 'Customer' and diccB['value'][4] == 'Customer':
            suma = diccA['value'][2].get(rango) + diccB['value'][3].get(rango)
            if suma > maximo:
                pareja = elemento

    return (pareja)


def req8(citibike, date, id):
    infoFecha = om.get(citibike['dates'], date)
    # print(infoFecha.keys())
    infoBici = infoFecha[id]
    t_uso = round((infoBici[0]) / 60)
    t_libre = 1440 - t_uso
    stops = []

    iterator = it.newIterator(infoBici[1])
    while it.hasNext(iterator):
        element = it.next(iterator)
        stops.append(element)
    return (t_uso, t_libre, stops)


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
    stopcode = str(keyvaluestop['key'])
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def comparePairs(id1, id2):
    id2 = id2['key']
    # print(id1, id2)
    if (id1 == id2):
        return 0
    elif (id1 < id2):
        return -1
    else:
        return 1

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareIds(date1, date2):
    # print(date1, date2)
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1