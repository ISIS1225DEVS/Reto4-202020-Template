
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
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import edge as ed
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dfs as dfs
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

        analyzer['stops'] = m.newMap(numelements=10,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14,
                                              comparefunction=compareStopIds)
        analyzer['birth year']= m.newMap(numelements=10,
                                     maptype='PROBING',
                                     comparefunction=compareStopIds)
        analyzer["nombres"]={}
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
    if trip['start station id']!=trip['end station id']:
        origin = trip['start station id']
        destination = trip['end station id']
        duration = int(trip['tripduration'])
        addStation(citibike, origin)
        addStation(citibike, destination)
        addConnection(citibike, origin, destination, duration)
        citibike[trip['start station id']]=trip['start station name']
        citibike[trip['end station id']]=trip["end station name"]
        if int(trip["birth year"])>2010:
            if m.contains(citibike["birth year"],"0-10")==True:
                lista=me.getValue(m.get(citibike["birth year"],"0-10"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"0-10",lista)
                
                
               
            else:
                m.put(citibike["birth year"],"0-10",{trip['start station id']:trip["start station name"]})
                m.put(citibike["birth year"],"0-10",{trip['end station id']:trip["end station name"]})
        elif int(trip["birth year"])>2000:
            if m.contains(citibike["birth year"],"10-20")==True:
                lista=me.getValue(m.get(citibike["birth year"],"10-20"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"10-20",lista)
                
                
                
            else:
                m.put(citibike["birth year"],"10-20",{trip['start station id']:trip["start station name"]})
                m.put(citibike["birth year"],"10-20",{trip['end station id']:trip["end station name"]})
        elif int(trip["birth year"])>1990:
            if m.contains(citibike["birth year"],"20-30")==True:
                lista=me.getValue(m.get(citibike["birth year"],"20-30"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"20-30",lista)
 
                
            else:
                m.put(citibike["birth year"],"20-30",{trip['start station id']:trip["start station name"]})
                m.put(citibike["birth year"],"20-30",{trip['end station id']:trip["end station name"]})
                
        elif int(trip["birth year"])>1980:
            if m.contains(citibike["birth year"],"30-40")==True:
                lista=me.getValue(m.get(citibike["birth year"],"30-40"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"30-40",lista)
         
                
            else:
                m.put(citibike["birth year"],"30-40",{trip['start station id']:trip["start station name"]})
                m.put(citibike["birth year"],"30-40",{trip['end station id']:trip["end station name"]})
        elif int(trip["birth year"])>1970:
            if m.contains(citibike["birth year"],"40-50")==True:
                lista=me.getValue(m.get(citibike["birth year"],"40-50"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"40-50",lista)
         
            else:
                m.put(citibike["birth year"],"40-50",{trip['start station id']:trip["start station name"]})
                m.put(citibike["birth year"],"40-50",{trip['end station id']:trip["end station name"]})
        elif int(trip["birth year"])>1960:
            if m.contains(citibike["birth year"],"50-60")==True:
                lista=me.getValue(m.get(citibike["birth year"],"50-60"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"50-60",lista)
            else:
               m.put(citibike["birth year"],"50-60",{trip['start station id']:trip["start station name"]})
               m.put(citibike["birth year"],"50-60",{trip['end station id']:trip["end station name"]})
        else:
            if m.contains(citibike["birth year"],"mas de 60")==True:
                
                lista=me.getValue(m.get(citibike["birth year"],"mas de 60"))
                lista[trip['start station id']]=trip["start station name"]
                lista[trip['end station id']]=trip["end station name"]
                m.put(citibike["birth year"],"mas de 60",lista)
            else:
               m.put(citibike["birth year"],"mas de 60",{trip['start station id']:trip["start station name"]})
               m.put(citibike["birth year"],"mas de 60",{trip['end station id']:trip["end station name"]})



        
    return citibike


def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['connections'], stationid):
            gr.insertVertex(citibike ['connections'], stationid)

    return citibike


def addConnection(citibike, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones. Si el arci existe se actualiza su peso con el promedio
    """
    edge = gr.getEdge(citibike['connections'], origin, destination)
    if edge is None:
        gr.addEdge(citibike['connections'], origin, destination, duration)
    else:
        ed.updateAverageWeight(edge,duration)

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


def createCicleUnderTime(grafo, vertice, tiempo1, tiempo2=0):
    lista = lt.newList()
    tiempo = max(tiempo1, tiempo2)
    ciclos = None
    for ruta in ciclo:
        costo = ciclo[ruta][weihgt] = (gr.numVertices(ciclo[ruta])-1) * 20
        if costo <= tiempo:
            lt.addFirst(lista, ciclo[ruta])
    return lista


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





def rutas_por_min(estacion,time,grafo,caminos):
    """se intento cambiar la estrucutra de dfs pero no se logro mayor cosa que un diccionario con llaves el id de las estaciones y los valores son las estaciones adyacentes
    mas sin embargo no sirvio de mucho para dar una forma de lista para dar un camino hacia una ubicacion.
    
    se intento implementar esta funcion que daba una lista de lista sin embargo el analisis de esta estructura se volvio muy dificil de organizar """
    adjlst= gr.adjacents(grafo["connections"],estacion)
    adjslstiter = it.newIterator(adjlst)
    while (it.hasNext(adjslstiter)):
        x=it.next(adjslstiter)
        a=gr.getEdge(grafo["connections"],estacion,x)
        b=ed.weight(a)
        print(time>=b)
        if a != None:
            tiempo=ed.weight(a)
            
            if time>=b:
                lista=[estacion,b,x]
                tiempo=time-tiempo
                lista.append(rutas_por_min(estacion,tiempo,grafo,lista))
                caminos.append(lista)
    return caminos
    

def organizar(dicionario,estacion,lista):
    return(lista)






    
        

def rango_edades(grafo,edad):
    mayor_salida=0
    mayor_entrada=0
    nombre_salida=None
    nombre_entrada=None
    idsalida=0
    identrada=0
    
    paso=me.getValue(m.get(grafo["birth year"],edad))
    for x in paso.keys():
        if gr.outdegree(grafo["connections"],x)>mayor_salida:
            mayor_salida=gr.outdegree(grafo["connections"],x)
            idsalida=x
            nombre_salida=paso[x]
        if gr.indegree(grafo["connections"],x)>mayor_entrada:
            mayor_entrada=gr.indegree(grafo["connections"],x)
            identrada=x
            nombre_entrada=paso[x]
    if idsalida==identrada:
        for x in paso.keys():
            if gr.indegree(grafo["connections"],x)>mayor_entrada and idsalida != identrada:
                mayor_entrada=gr.indegree(grafo["connections"],x)
                identrada=x
                nombre_entrada=paso[x]
    
    
    recorrido=djk.Dijkstra(grafo["connections"],idsalida)
    if djk.hasPathTo(recorrido,identrada):
        camino=djk.pathTo(recorrido,identrada)
    respuesta={"partida":nombre_salida,"final":nombre_entrada,"ruta":camino}
    return(respuesta)

    


        

    







        
   

        


                        

                



            
        
    
            



        


            






