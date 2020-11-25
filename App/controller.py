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

import os
import config as cf
from App import model
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citibike, filename)
    return citibike

def loadFile(citibike, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
    return citibike

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def ejecutarreq3 (citibike):
    retorno = model.req3(citibike)
    a = []
    b = []
    c = []
    for j in retorno[0]:
        a.append('La estación '+ str(j['key']) + ' con '+ str(j['value']) + ' llegadas')
    for j in retorno[1]:
        b.append('La estación '+ str(j['key']) + ' con '+ str(j['value']) + ' salidas')
    for j in retorno[2]:
        c.append('La estación '+ str(j['key']) + ' con '+ str(j['value']) + ' llegadas y salidas')
    
    print ('Las Estaciones con más llegadas son: ', a)
    print ('Las Estaciones con más salidas son: ', b)
    print ('Las Estaciones con menos llegadas y salidas son: ', c)
    
def ejecutarreq5 (citibike, edad):
    retorno = model.req5(citibike, edad)
    print ('La estación de la que más sale gente del grupo de edad es la: ', retorno[0])
    print ('La estación a la que más llega gente del grupo de edad es la: ', retorno[1])
    print ('La ruta entre esas estaciones es: ', retorno[2])
    

def ejecutarreq6 (citibike, lat1, lon1, lat2, lon2):
    retorno = model.req6(citibike, lat1, lon1, lat2, lon2)
    print ('La estación más cercana al punto de salida es la: ', retorno[0])
    print ('La estación más cercana al destino es la: ', retorno[1])
    print ('La ruta entre estas estaciones es: ', retorno[2])
    

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def numSCC(analyzer):
    return model.numSCC(analyzer)