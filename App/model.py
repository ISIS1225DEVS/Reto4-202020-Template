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
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
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
        analyzer = {
                    'trips': None,
                    'connections': None,
                    'EstacionesXid': None,
                    'components': None,
                    'years': None,
                    'coordinates': None 
                    
                    }

        analyzer['trips'] = m.newMap(numelements=14000,
                                     maptype='CHAINING',
                                     comparefunction=compareStations)
        analyzer['EstacionesXid'] = m.newMap(numelements=14000,
                                     maptype='CHAINING',
                                     comparefunction=compareBikeid)
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStations)
        analyzer['years'] = m.newMap(numelements=14000,
                                     maptype='CHAINING',
                                     comparefunction=compareDates)
        analyzer['coordinates'] = m.newMap(numelements=1000,
                                comparefunction=compareStations)
        
        return analyzer
 except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al grafo
def addTrip(analyzer, trip):
    """
Añade un viaje al grafo 
    """
    origin = trip['start station id']
    destination = trip['end station id']
    nombreEstacionOrigen= trip['start station name']
    nombreEstacionDestino= trip['end station name']
    m.put(analyzer['EstacionesXid'], origin, nombreEstacionOrigen)
    m.put(analyzer['EstacionesXid'], destination, nombreEstacionDestino)
    duration = int(trip['tripduration'])
    addStation(analyzer, origin)
    addStation(analyzer, destination)
    addConnection(analyzer, origin, destination, duration)

def addStation(analyzer, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not  gr.containsVertex(analyzer ['connections'], stationid):
            gr.insertVertex(analyzer ['connections'], stationid)
    return analyzer

def addConnection(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    promedio=None
    edge = gr.getEdge(analyzer ['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, duration)
    elif edge is not None and promedio is None:
        numero_viajes=1
        promedio=int(edge["weight"])
        promedio =(promedio*numero_viajes + duration)/(numero_viajes + 1)
        numero_viajes += 1
        edge["weight"]=promedio
    else:
        promedio=int(edge["weight"])
        promedio =(promedio*numero_viajes + duration)/(numero_viajes + 1)
        numero_viajes += 1
        edge["weight"]=promedio
    return analyzer

def addCoordinates(analyzer, trip):
    """
    Para el req 6
    """
    entry = analyzer['coordinates']
    stationStart = (trip['start station latitude'], trip['start station longitude'], 0)
    stationEnd = (trip['end station latitude'], trip['end station longitude'], 1)

    e1 = m.get(entry, trip['start station id'])
    if e1 is None:
        m.put(entry, trip['start station id'], stationStart)

    e2 = m.get(entry, trip['end station id'])
    if e2 is None:
        m.put(entry, trip['end station id'], stationEnd)

    return analyzer 


# ==============================
# Funciones de consulta
# ==============================

def numSCC(analyzer):
    sc = scc.KosarajuSCC(analyzer["connections"])
    return scc.connectedComponents(sc)
    
def sameCC(analyzer, station1, station2):
    sc = scc.KosarajuSCC(analyzer["connections"])
    return scc.stronglyConnected(sc, station1, station2)


def totalVertex(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def totalEdges(grafo):
    """
    Retorna todos los arcos del grafo
    """
    return gr.edges(grafo)

def totalVertices(grafo):
    """
    Retorna todos los vertices del grafo
    """
    return gr.vertices(grafo)

def arcosXvertex(grafo,word):
    """
    Retorna arcos del vertice
    """
    a=gr.indegree(grafo,word)
    b=gr.outdegree(grafo,word)
    return a+b

def salenviajes(grafo,word):
    """
    numero de arcos que salen del vertex (word)
    """
    return gr.outdegree(grafo,word)

def entranviajes(grafo,word):
    """
    numero de arcos que entran al vertex (word)
    """
    return gr.indegree(grafo,word)

# ==============================
# REQUERIMIENTOS
# ==============================

def RutasCirculares(analyzer, vertice, limiteInicial, limiteFinal): #REQUERIMIENTO 2
    peso=0
    
    rutas_circulares_total=  lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None) #agrupar todas las rutas cicrulares
    
    dijkstraIda= djk.Dijkstra(analyzer['connections'], vertice)
    vertices=gr.vertices(analyzer['connections'])

    iter2= it.newIterator(vertices)
    while it.hasNext(iter2):
        datos_rutas= lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None) # info todas las rutas cicrulares
        ruta_circular= lt.newList(datastructure='SINGLE_LINKED', cmpfunction=None) #lista de nombres de estaciones en la ruta circular
        vertice2= it.next(iter2)
        caminos_ida= djk.pathTo(dijkstraIda, vertice2) #grafo conocer vertices
        dijkstraVenida= djk.Dijkstra(analyzer['connections'], vertice2)
        caminos_venida= djk.pathTo(dijkstraVenida, vertice)
        if not caminos_venida or not caminos_ida:
            continue
        while not stack.isEmpty(caminos_ida):
            dato=stack.pop(caminos_ida)
            lt.addLast(ruta_circular, dato)
    
        while not stack.isEmpty(caminos_venida):
            dato=stack.pop(caminos_venida)
            lt.addLast(ruta_circular, dato)
    
    # lt.addLast(rutas_circulares_total, ruta_circular)

        iter=it.newIterator(ruta_circular)
        while it.hasNext(iter):
            arco= it.next(iter)
            duracion=arco['weight']
            if (int(limiteInicial)<duracion and duracion<int(limiteFinal)):
                estacion1=m.get(analyzer['EstacionesXid'], arco['vertexA'])
                estacion2=m.get(analyzer['EstacionesXid'], arco['vertexB'])
                lt.addLast(datos_rutas, {"estacion1": estacion1, "estacion2":estacion2, "duracion":duracion})
            
        lt.addLast(rutas_circulares_total, datos_rutas)

    return (rutas_circulares_total)
# def RutaInteresTuristico(analyzer, posInicialT, posFinalT, posInicialL, posFinalL): #REQUERIMIENTO 6
   




# ==============================
# Funciones de Comparacion
# ==============================
def compareStations(stat, keyvalue):
    """
    Compara dos estaciones
    """
    code = keyvalue['key']
    if (stat == code):
        return 0
    elif (stat > code):
        return 1
    else:
        return -1

def compareBikeid(bike, keyvaluebike):
    """
    Compara dos bikeids
    """
    bikecode = keyvaluebike['key']
    if (bike == bikecode):
        return 0
    elif (bike > bikecode):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    date20=me.getKey(date2)
    #print(date1)
    #print(date2)
    if (date1 == date20):
        return 0
    elif (date1 > date20):
        return 1
    else:
        return -1