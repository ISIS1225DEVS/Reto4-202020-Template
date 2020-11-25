
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
from DISClib.Algorithms.Graphs import dfs
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



def createDataStructures():
    citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST', 
                                    directed=True, 
                                    size=1000, 
                                    comparefunction=compareStations)
    return citibike

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }

        analyzer['stops'] = m.newMap(numelements=1001,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al grafo


def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(analyzer, filename)
    return analyzer


def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
    return citibike


def addTrip(citibike, trip):
    """
    Añade un viaje
    """
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)
     
    return citibike


def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['connections'], stationid):
            gr.insertVertex(citibike ['connections'], stationid)

    return citibike


def addConnection(citibike, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones. Si el arci existe se actualiza su peso con el promedio
    """
    edge = gr.getEdge(citibike['connections'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, distance)
    else:
        ed.updateAverageWeight(edge, distance)

    return citibike

  
def addStopConnection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = formatVertex(lastservice)
        destination = formatVertex(service)
        cleanServiceDistance(lastservice, service)
        distance = float(service['tripduration']) - float(lastservice['tripduration'])
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['stops'], service['end station id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['end station name'])
        m.put(analyzer['stops'], service['end station id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['end station name']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer


def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['stops'])
    stopsiterator = it.newIterator(lststops)
    while it.hasNext(stopsiterator):
        key = it.next(stopsiterator)
        lstroutes = m.get(analyzer['stops'], key)['value']
        prevrout = None
        routeiterator = it.newIterator(lstroutes)
        while it.hasNext(routeiterator):
            route = key + '-' + it.next(routeiterator)
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route
            

# ==============================
# Funciones de consulta
# ==============================


def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], initialStation)
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


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


def createCicleUnderTime(grafo, vertice, tiempo1, tiempo2):
    rutas_aprovadas = lt.newList(datastructure='ARRAY_LIST')
    lista_ciclos = scc_vertice(grafo, vertice)
    for ciclo in lista_ciclos:
        lista = lt.getElement(lista_ciclos, vertice)
        valido = scc_valido(lista, vertice, tiempo1, tiempo2)
        lt.addFirst(rutas_aprovadas, valido)
    return rutas_aprovadas


# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['tripduration'] == '':
        service['tripduration'] = 0
    if lastservice['tripduration'] == '':
        lastservice['tripduration'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['end station id'] + '-'
    name = name + service['end station name']
    return name
  
def estrictamente_conectados(graph,v1,v2):
    retorno=scc.KosarajuSCC(graph)
    retorno2=scc.stronglyConnected(retorno,v1,v1)
    recorrido=retorno["idscc"]["table"]["elements"]
    contador=0
    for elemento in recorrido:
        for elemento2 in recorrido:
            if elemento["key"]!=None and elemento2["key"]!=None:
                conectados=scc.stronglyConnected(retorno,elemento["key"],elemento2["key"])
                if conectados== True:
                    contador+=1
    return print(retorno2,contador)


def conectados_total(grafo):
    retorno=scc.KosarajuSCC(grafo)
    recorrido=retorno["idscc"]["table"]["elements"]
    contador=0
    for elemento in recorrido:
        for elemento2 in recorrido:
            if elemento["key"]!=None and elemento2["key"]!=None:
                conectados=scc.stronglyConnected(retorno,elemento["key"],elemento2["key"])
                if conectados== True:
                    contador+=1

    return contador
# ==============================
# Funciones de Comparacion
# ==============================


def compareStopIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def compareroutes(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])



def estrictamente_conectados(graph,v1,v2):
    retorno=scc.KosarajuSCC(graph)
    retorno2=scc.stronglyConnected(retorno,v1,v1)
    total=conectados_total
    return print(retorno2,conectados_total)

def conectados_total(grafo):
    retorno=scc.KosarajuSCC(grafo)
    recorrido=retorno["idscc"]["table"]["elements"]
    contador=0
    for elemento in recorrido:
        for elemento2 in recorrido:
            if elemento["key"]!=None and elemento2["key"]!=None:
                conectados=scc.stronglyConnected(retorno,elemento["key"],elemento2["key"])
                if conectados== True:
                    contador+=1

    return contador

def requerimiento3(grafo):
    lista=gr.vertices(grafo)
    primero=lista["first"]
    primero_llegan=gr.indegree(grafo,primero["info"])
    primero_salen=gr.outdegree(grafo,primero["info"])
    estacion_llegan=primero["info"]
    estacion_salen=primero["info"]
    suma_primero=primero_llegan+primero_salen
    estacion_menos=primero["info"]
    llegan=primero_llegan
    salen=primero_salen
    siguiente=primero["next"]
    while siguiente != None:
        actual_llegan=gr.indegree(grafo,siguiente["info"])
        actual_salen=gr.outdegree(grafo,siguiente["info"])
        suma_actual=actual_llegan+actual_salen
        if actual_llegan>llegan:
            llegan=actual_llegan
            estacion_llegan=siguiente["info"]
        if actual_salen>salen:
            salen=actual_salen
            estacion_salen=siguiente["info"]
        if suma_actual<suma_primero:
            suma_primero=suma_actual
            estacion_menos=siguiente["info"]
        siguiente=siguiente["next"]
    top_1_llegan=estacion_llegan
    top_1_salen=estacion_salen
    top_1_menos=estacion_menos
    llegan=primero_llegan
    salen=primero_salen
    suma_primero=primero_llegan+primero_salen
    siguiente=primero["next"]
    while siguiente != None:
        actual_llegan=gr.indegree(grafo,siguiente["info"])
        actual_salen=gr.outdegree(grafo,siguiente["info"])
        suma_actual=actual_llegan+actual_salen
        if actual_llegan>llegan and siguiente["info"]!=top_1_llegan:
            llegan=actual_llegan
            estacion_llegan=siguiente["info"]
        if actual_salen>salen and siguiente["info"]!=top_1_salen:
            salen=actual_salen
            estacion_salen=siguiente["info"]
        if suma_actual<suma_primero and siguiente["info"]!=top_1_menos:
            suma_primero=suma_actual
            estacion_menos=siguiente["info"]
        siguiente=siguiente["next"]
    top_2_llegan=estacion_llegan
    top_2_salen=estacion_salen
    top_2_menos=estacion_menos
    llegan=primero_llegan
    salen=primero_salen
    suma_primero=primero_llegan+primero_salen
    siguiente=primero["next"]
    while siguiente != None:
        actual_llegan=gr.indegree(grafo,siguiente["info"])
        actual_salen=gr.outdegree(grafo,siguiente["info"])
        suma_actual=actual_llegan+actual_salen
        if actual_llegan>llegan and siguiente["info"]!=top_1_llegan and siguiente["info"]!=top_2_llegan:
            llegan=actual_llegan
            estacion_llegan=siguiente["info"]
        if actual_salen>salen and siguiente["info"]!=top_1_salen and siguiente["info"]!=top_2_salen:
            salen=actual_salen
            estacion_salen=siguiente["info"]
        if suma_actual<suma_primero and siguiente["info"]!=top_1_menos and siguiente["info"]!=top_2_menos:
            suma_primero=suma_actual
            estacion_menos=siguiente["info"]
        siguiente=siguiente["next"]
    top_3_llegan=estacion_llegan
    top_3_salen=estacion_salen
    top_3_menos=estacion_menos 
    retorno_1="[Las estaciones top de llegada son "+top_1_llegan+", "+top_2_llegan+", "+top_3_llegan+" ]"
    retorno_2="[Las estaciones top de salida son "+top_1_salen+", "+top_2_salen+", "+top_3_salen+" ]"
    retorno_3="[Las estaciones menos utilizadas son "+top_1_menos+", "+top_2_menos+", "+top_3_menos+" ]"
    return print(retorno_1,retorno_2,retorno_3)

from math import sin, cos, sqrt, atan2, radians

def distancia(grafo,lat1,lon1,lat2,lon2,analyzer):
    lista=gr.vertices(grafo)
    primero=lista["first"]
    estacion1=primero["info"]
    R = 6373.0
    print(analyzer["stops"])
    lat_primero=radians(analyzer["stops"][estacion1]["start station latitude"])
    lon_primero=radians(analyzer["stops"][estacion1]["start station longitude"])

    dlon_primero = lon_primero - lon1
    dlat_primero = lat_primero - lat1
    a_primero = sin(dlat_primero / 2)**2 + cos(lat1) * cos(lat_primero) * sin(dlon_primero / 2)**2
    c_primero = 2 * atan2(sqrt(a_primero), sqrt(1 - a_primero))
    distancia_1 = R * c_primero

    dlon_primero2 = lon_primero - lon2
    dlat_primero2 = lat_primero - lat2
    a_primero2 = sin(dlat_primero2 / 2)**2 + cos(lat2) * cos(lat_primero) * sin(dlon_primero2 / 2)**2
    c_primero2 = 2 * atan2(sqrt(a_primero2), sqrt(1 - a_primero2))
    distancia_2 = R * c_primero2

    cercana=distancia_1
    cercana_nombre=estacion1
    destino=distancia_2
    destino_nombre=estacion1
    siguiente=primero["next"]

    while next!=None:
        lat_actual=radians(analyzer["stops"][siguiente["info"]]["start station latitude"])
        lon_actual=radians(analyzer["stops"][siguiente["info"]]["start station longitude"])
        dlon1 = lon_actual - lon1
        dlat1 = lat_actual - lat1
        a1 = sin(dlat1 / 2)**2 + cos(lat1) * cos(lat_actual) * sin(dlon1 / 2)**2
        c1 = 2 * atan2(sqrt(a1), sqrt(1 - a1))
        distance_actual1 = R * c1
        if distance_actual1<cercana:
            cercana=distance_actual1
            cercana_nombre=siguiente["info"]
        dlon2 = lon_actual - lon2
        dlat2 = lat_actual - lat2
        a2 = sin(dlat2 / 2)**2 + cos(lat2) * cos(lat_actual) * sin(dlon2 / 2)**2
        c2 = 2 * atan2(sqrt(a2), sqrt(1 - a2))
        distance_actual2 = R * c2
        if distance_actual2<destino:
            destino=distance_actual2
            destino_nombre=siguiente["info"]
        siguiente=siguiente["next"]

    busqueda=dfs.DepthFirstSearch(grafo,cercana_nombre)
    pila=dfs.pathTo(busqueda,destino_nombre)
    retorno="Inicio: "+cercana_nombre+" "+"Destino: "+destino_nombre+" "
    return print(retorno, pila)

