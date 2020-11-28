
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
from DISClib.Algorithms.Graphs import scc as scc
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
                    'paths': None,
                    "diccionario": None
                    }

        analyzer['stops'] = m.newMap(numelements=1,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds)

        analyzer["diccionario"]={}
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
    latitud_inicio=trip["start station latitude"]
    longitud_inicio=trip["start station longitude"]
    latitud_final=trip["end station latitude"]
    longitud_final=trip["end station longitude"]
    nombre_inicio=trip["start station name"]
    nombre_final=trip["end station name"]
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration)

    if origin not in citibike["diccionario"]:
        citibike["diccionario"][origin]={"latitud":latitud_inicio,"longitud":longitud_inicio,"nombre":nombre_inicio}
    if destination not in citibike["diccionario"]:
        citibike["diccionario"][destination]={"latitud":latitud_final,"longitud":longitud_final,"nombre":nombre_final}
    if m.contains(citibike["stops"],origin)==False:
        mapa=m.newMap(numelements=1,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        m.put(mapa,"latitud",latitud_inicio)
        m.put(mapa,"longitud",longitud_inicio)
        m.put(mapa,"nombre",nombre_inicio)
        m.put(citibike["stops"],origin,mapa)

    if m.contains(citibike["stops"],destination)==False:
        mapa=m.newMap(numelements=1,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        m.put(mapa,"latitud",latitud_final)
        m.put(mapa,"longitud",longitud_final)
        m.put(mapa,"nombre",nombre_final)
        m.put(citibike["stops"],destination,mapa)   
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
    #Arraylst que alberga las rutas con un tiempo en el rango
    lista_rutas = lt.newList(datastructure='ARRAYLIST')
    #Scc del vertice
    scc_vertice = scc.KosarajuUnicoSCC(grafo, vertice)
    #Lista de los ciclos del Scc
    ciclos = DepthFirstSearchCicles(scc_vertice, vertice)
    #Recorrido de cada ciclo presente en el Scc del vertice
    posicion = m.size(ciclos)
    
    while posicion >= 0:
        
        posicion -= 1
        costo = 0
        camino = lt.newList(datastructure='ARRAYLIST')
        #Llave valor de la ruta
        info_ruta = m.get(ciclos, posicion)
        #Mapa de vertices que componen la ruta
        visitados = info_ruta['value']
        impreso = m.valueSet(visitados)
        lt.addFirst(camino, impreso)
        iterador_impreso = it.newIterator(impreso)

        while it.hasNext(iterador_impreso):
            vertice = it.next(iterador_impreso)
            valor_arco = m.get(grafo, vertice)
            numerico = valor_arco['value']
            costo += int(numerico['weight']) + 20

            if tiempo1 <= costo <= tiempo2:
                lt.addFirst(lista_rutas,camino)

    return lista_rutas


def findCircularRoutesNumber(grafo, vertice, tiempo1, tiempo2):
    return lt.size(createCicleUnderTime(grafo, vertice, tiempo1, tiempo2))

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

def requerimiento3(grafo,analyzer):
    diccionario=analyzer["diccionario"]
    a=0
    lista1=[]
    lista2=[]
    lista3=[]
    lista_final_llegadas=[]
    lista_final_salidas=[]
    lista_final_menos=[]
    dict_entradas={}
    dict_salidas={}
    dict_menos={}
    lista=gr.vertices(grafo)
    primero=lista["first"]
    primero_llegan=gr.indegree(grafo,primero["info"])
    primero_salen=gr.outdegree(grafo,primero["info"])
    estacion_llegan=primero["info"]
    estacion_salen=primero["info"]
    estacion_menos=primero["info"]
    siguiente=primero["next"]

    while siguiente != None:
        actual_llegan=gr.indegree(grafo,siguiente["info"])
        actual_salen=gr.outdegree(grafo,siguiente["info"])
        suma_actual=actual_llegan+actual_salen
        dict_entradas[siguiente["info"]]=dict_entradas.get(siguiente["info"],0)+actual_llegan
        dict_salidas[siguiente["info"]]=dict_salidas.get(siguiente["info"],0)+actual_salen
        dict_menos[siguiente["info"]]=dict_menos.get(siguiente["info"],0)+suma_actual
        siguiente=siguiente["next"]


    while a<3:
        top1=""
        top2=""
        top3=""
        mayor_entrada=0
        mayor_salida=0
        menor_uso=99999
        for nodo in dict_entradas:
            if dict_entradas[nodo]>mayor_entrada and nodo not in lista1:
                mayor_entrada=dict_entradas[nodo]
                top1=nodo
        lista1.append(top1)
        for nodo in dict_salidas:
            if dict_salidas[nodo]>mayor_salida and nodo not in lista2:
                mayor_entrada=dict_salidas[nodo]
                top2=nodo
        lista2.append(top2)
        for nodo in dict_menos:
            if dict_menos[nodo]<menor_uso and nodo not in lista3:
                menor_uso=dict_menos[nodo]
                top3=nodo
        lista3.append(top3)
        a+=1
    
    for elemento in lista1:
        lista_final_llegadas.append(diccionario[str(elemento)]["nombre"])
    for elemento in lista2:
        lista_final_salidas.append(diccionario[str(elemento)]["nombre"])
    for elemento in lista3:
        lista_final_menos.append(diccionario[str(elemento)]["nombre"])

    retorno1= "Las estaciones top de llegada son: "+str(lista_final_llegadas)
    retorno2= "Las estaciones top de salida son: "+str(lista_final_salidas)
    retorno3= "Las estaciones top de menos son: "+str(lista_final_menos)
    final=retorno1+retorno2+retorno3
    return print(final)

from math import sin, cos, sqrt, atan2, radians

def distancia(grafo,lat1,lon1,lat2,lon2,analyzer):
    lista=gr.vertices(grafo)
    primero=lista["first"]
    estacion1=str(primero["info"])
    R = 6373.0
    lat_primero=radians(float(analyzer["diccionario"][estacion1]["latitud"]))
    lon_primero=radians(float(analyzer["diccionario"][estacion1]["longitud"]))

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
    cercana_final=estacion1
    destino=distancia_2
    destino_nombre=estacion1
    destino_final=estacion1
    siguiente=primero["next"]

    while siguiente!=None:
        estacion_actual=str(siguiente["info"])
        lat_actual=radians(float(analyzer["diccionario"][estacion_actual]["latitud"]))
        lon_actual=radians(float(analyzer["diccionario"][estacion_actual]["longitud"]))
        dlon1 = lon_actual - lon1
        dlat1 = lat_actual - lat1
        a1 = sin(dlat1 / 2)**2 + cos(lat1) * cos(lat_actual) * sin(dlon1 / 2)**2
        c1 = 2 * atan2(sqrt(a1), sqrt(1 - a1))
        distance_actual1 = R * c1
        if distance_actual1<cercana:
            cercana=distance_actual1
            cercana_nombre=siguiente["info"]
            cercana_final=analyzer["diccionario"][estacion_actual]["nombre"]
        dlon2 = lon_actual - lon2
        dlat2 = lat_actual - lat2
        a2 = sin(dlat2 / 2)**2 + cos(lat2) * cos(lat_actual) * sin(dlon2 / 2)**2
        c2 = 2 * atan2(sqrt(a2), sqrt(1 - a2))
        distance_actual2 = R * c2
        if distance_actual2<destino:
            destino=distance_actual2
            destino_nombre=siguiente["info"]
            destino_final=analyzer["diccionario"][estacion_actual]["nombre"]
        siguiente=siguiente["next"]

    busqueda=djk.Dijkstra(grafo,cercana_nombre)
    duracion=djk.distTo(busqueda,destino_nombre)
    pila=djk.pathTo(busqueda,destino_nombre)
    retorno="Inicio: " +cercana_final+ " " +"Destino: " +destino_final+ " " +"Duración: "+str(duracion)
    return print(retorno, pila)
