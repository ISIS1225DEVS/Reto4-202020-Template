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
import operator
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error

from DISClib.Algorithms import Sorting as s

from DISClib.DataStructures import edge as e

assert config
#import obspy.geodetics as og
from math import radians, cos, sin, asin, sqrt 
"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def newAnalyzer(tamaño, carga):
    """ Inicializa el analizador
   stations: Tabla de hash para guardar los vertices del grafo
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {'graph': None,
                    'stations': None,
                    'paths': None,
                    'stationsName':None,
                    'Latitude&Longitude':None}
                    
        analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                        directed=True,
                        size=1000,
                        comparefunction=compareStations)

        analyzer['stations'] = m.newMap(numelements=tamaño,
                                     maptype='CHAINING',
                                     loadfactor=carga,
                                     comparefunction=compareStations)

        analyzer['paths'] = m.newMap(numelements=tamaño,
                                     maptype='CHAINING',
                                     loadfactor=carga,
                                     comparefunction=compareroutes)
        analyzer['stationsName'] = m.newMap(numelements=tamaño,
                                    maptype='CHAINING',
                                    loadfactor=carga,
                                    comparefunction=compareStations)
        analyzer['Latitude&Longitude'] = m.newMap(numelements=tamaño,
                                    maptype='CHAINING',
                                    loadfactor=carga,
                                    comparefunction=compareStations)
        analyzer['StationsById'] = m.newMap(numelements=tamaño,
                                    maptype='CHAINING',
                                    loadfactor=carga,
                                    comparefunction=compareStations)
        analyzer['StationTripTime'] = m.newMap(numelements=tamaño,
                                    maptype='CHAINING',
                                    loadfactor=carga,
                                    comparefunction=compareStations)
        analyzer['Top'] = m.newMap(numelements=tamaño,
                                    maptype='CHAINING',
                                    loadfactor=carga,
                                    comparefunction=compareStations)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo



def addTrip(analyzer, trip):
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addCoordenates(analyzer,trip)
    addStationName(analyzer,trip)
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addStationNamebyId(analyzer,trip)
    addTime(analyzer,trip)
    addConnection(analyzer, origin, destination, duration)
    addRouteStation(analyzer, trip)

def addCoordenates(analyzer,trip):
    latitude=trip['start station latitude']
    longitude=trip['start station longitude']
    coordenates=(latitude,longitude)
    entry=m.get(analyzer['Latitude&Longitude'],coordenates)
    if entry is None:
        m.put(analyzer['Latitude&Longitude'],trip['start station name'],coordenates)
    
def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['graph'], stationid):
            gr.insertVertex(analyzer['graph'], stationid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStation')

def addTime(analyzer,trip):
    entry=m.get(analyzer['StationTripTime'],trip['start station name'])
    if entry is None:
        m.put(analyzer['StationTripTime'],trip['start station name'], trip['tripduration'])
    return analyzer

def addRouteStation(analyzer, trip):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['stations'], trip['start station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)

        lt.addLast(lstroutes, trip['end station id'])
        m.put(analyzer['stations'], trip['start station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = trip['start station id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer

def addStationNamebyId(analyzer,trip):
    entry=m.get(analyzer['StationsById'],trip['end station name'])
    if entry is None:
        m.put(analyzer['StationsById'],trip['end station name'], trip['end station id'])
    return analyzer

def addStationName(analyzer,trip):
    entry = m.get(analyzer['stationsName'],trip['start station name'])
    if entry is None:
        lstnames = lt.newList(cmpfunction=compareConnections)
        lt.addLast(lstnames, trip['start station name'])
        m.put(analyzer['stationsName'],trip['start station id'],lstnames)
    else:
        lstnames = entry['value']
        info = trip['start station id']
        if not lt.isPresent(lstnames, info):
            lt.addLast(lstnames,info)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['graph'], origin, destination)
    if edge is not None:
        edge['pesos'] += round((duration / 60),2)
        edge['size'] += 1
        edge['weight'] = round((edge['pesos']/edge['size']),2)
    else:
        gr.addEdge(analyzer['graph'], origin, destination, round((duration / 60),2))

# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['stations'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['stations'])

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
    return analyzer

def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path

def totalStation(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def numberStations(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stations'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stations'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg

# =============================
# Funciones Helper
# ==============================

def formatVertex(station):
    """
    Se formatea el nombre del vertice con el id de la estación
    seguido de la ruta.
    """
    name = station['start station id']
    return name

# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(station, keyvaluestation):
    stationcode = keyvaluestation['key']
    if (station == stationcode):
        return 0
    elif (station > stationcode):
        return 1
    else:
        return -1

def compareroutes(route1, route2):
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def compareConnections(connection1, connection2):

    if (connection1 == connection2):
        return 0
    elif (connection1 > connection2):
        return 1
    else:
        return -1

# ==============================
# Requerimientos
# ==============================

def cantidadClusters(analyzer, id1 , id2): #Req. 1
    """
    ----------REQUERIMIENTO 1------------
    OUTPUTS:
        TUPLE: (1,2)
            1: Clusters
            2: Sí dos nodos están en el mismo clúster
            3: Variable del algoritmo
    """
    try:
        var = scc.KosarajuSCC(analyzer['graph'])
        vertices = gr.vertices(analyzer['graph'])
        clusters = {'size': 0}
        iterator = it.newIterator(vertices)
        while it.hasNext(iterator):
            current = it.next(iterator)
            cod = m.get(var['idscc'], current)['value']
            if cod not in clusters:
                clusters[cod] = lt.newList(cmpfunction=compareConnections)
                clusters['size'] += 1
            lt.addLast(clusters[cod],current)
        conected = False
        if m.get(var['idscc'],id1) != None and m.get(var['idscc'],id2) != None:
            conected = scc.stronglyConnected(var,id1,id2)
        return (clusters,conected,var)
    except:
        return -1

def rutaTuristicaCircular(analizador, time, startStation):   #Req. 2
    try:
        analyzer = analizador.copy()
        clusters = cantidadClusters(analyzer,'1','2')
        cluster = clusters[0][m.get(clusters[2]['idscc'],startStation)['value']]
        caminos = [0]
        iterator = it.newIterator(cluster)
        search = djk.Dijkstra(analyzer['graph'],startStation)
        while it.hasNext(iterator):
            current = it.next(iterator)
            camino = djk.pathTo(search, current)
            trip = djk.distTo(search, current)
            if trip*2 > int(time[0]) and trip*2 < int(time[1]):
                caminos[0] += 1
                caminos.append((camino,trip*2))   
        return caminos
    except:
        return -1

def estacionesCriticas(analyzer):   #Req. 3
    vertices = gr.vertices(analyzer['graph'])
    values = {}
    iterator = it.newIterator(vertices)
    while it.hasNext(iterator):
        current = it.next(iterator)
        edges = gr.adjacentEdges(current)
        iterator2 = it.newIterator(edges)
        while it.hasNext(iterator2):
            current2 = it.newIterator(iterator2)
            if current not in values:
                values[current] = current2['size']
            else:
                values[current] += current2['size']
    #return hallarTop(values)
    
        

def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6
    StationName=m.valueSet(analyzer['stationsName'])
    iterator=it.newIterator(StationName)
    minimal=1000000000000
    nameminimal=''
    minimal1=1000000000000
    nameminimal1=''
    while it.hasNext(iterator):
        actual=it.next(iterator) #lista
        iterator2=it.newIterator(actual)
        while it.hasNext(iterator2):
            actual2=it.next(iterator2)
            coordenate=m.get(analyzer['Latitude&Longitude'],actual2) #tupla latitude=(coordenate['value'][0]) y longitude=(coordenate['value'][1])
            latlst=(coordenate['value'][0])
            longlst=(coordenate['value'][1])
            ATS=distance(latlocal,latlst,longlocal,longlst)
            STP=distance(latlst,latfinal,longlst,longfinal)
            if ATS < minimal:
                nameminimal=coordenate['key']
                minimal=ATS
            if STP < minimal1:
                nameminimal1=coordenate['key']
                minimal1=STP
    duration = float(m.get(analyzer['StationTripTime'],nameminimal)['value']) + float(m.get(analyzer['StationTripTime'],nameminimal1)['value'])
    
    #####
    return (nameminimal, nameminimal1, duration)

# ==============================
# Funciones Auxiliares
# ==============================

def gradosAkilometros(x):
    a=x.split('.')
    try:
        return str(a[0])+'.'+str(a[1])+str(a[2])
    except:
        return str(a[0])+'.'+str(a[1])

def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(float(gradosAkilometros(lon1)))
    lon2 = radians(float(gradosAkilometros(lon2)))
    lat1 = radians(float(gradosAkilometros(lat1))) 
    lat2 = radians(float(gradosAkilometros(lat2)))
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 


def rutaTuristicaResistencia(analyzer, time, idstation):   #Req. 4
    vertices = {}
    res = gr.adjacentEdges(analyzer['graph'], '144') #res = lista
    iterator = it.newIterator(res)
    while it.hasNext(iterator):
        current = it.next(iterator)
        if current['weight'] < time:
            vertices[current['vertexB']] = {}
            vertices[current['vertexB']]['weight'] = current['weight']
    return vertices


"""#def recomendadorRutas(analyzer, edades):   #Req. 5
#def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6
#def estacionesPublicidad(analyzer, rango):   #Req. 7*
#def bicicletasMantenimmiento(analyzer, idbike, fecha):   #Req. 8*"""

# ==============================
# Funciones Auxiliares
# ==============================

def gradosAkilometros(x):
    a=x.split('.')
    try:
        return str(a[0])+'.'+str(a[1])+str(a[2])
    except:
        return str(a[0])+'.'+str(a[1])

def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(float(gradosAkilometros(lon1)))
    lon2 = radians(float(gradosAkilometros(lon2)))
    lat1 = radians(float(gradosAkilometros(lat1))) 
    lat2 = radians(float(gradosAkilometros(lat2)))
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 


"""    
#def rutaTuristicaResistencia(analyzer, time, idstation):   #Req. 4

#def recomendadorRutas(analyzer, edades):   #Req. 5

#def rutaInteresTuristico(analyzer, latlocal, longlocal, latfinal, longfinal):   #Req. 6

#def estacionesPublicidad(analyzer, rango):   #Req. 7*

#def bicicletasMantenimmiento(analyzer, idbike, fecha):   #Req. 8*"""

