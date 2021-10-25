"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los avistamientos
    Se crean indices (Maps).

    Retorna el analizador inicializado.
    """
    analyzer = {'ufos_list': None,
                'Sightings_city': None
                }

    analyzer['ufos_list'] = lt.newList('ARRAY_LIST')
    analyzer['Sightings_per_city'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareCity)
    return analyzer

# Funciones para agregar informacion al catalogo
def addAvistamiento(analyzer, avistamiento):

    lt.addLast(analyzer['ufos_list'], avistamiento)
    updateCityIndex(analyzer['Sightings_per_city'], avistamiento)
    return analyzer

def updateCityIndex(map, avistamiento):
    city = avistamiento['city']
    
    entry = om.get(map, city)
    if entry is None:
        cityentry = newCityEntry(avistamiento)
        om.put(map, city, cityentry)
    else:
        cityentry = me.getValue(entry)
    addCityIndex(cityentry, avistamiento)
    return map

def addCityIndex(cityentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = cityentry['lstSights']
    lt.addLast(lst, avistamiento)
    """
    cityIndex = cityentry['CityIndex']
    cityentry = mp.get(cityIndex, avistamiento['city'])
    if (cityentry is None):
        entry = newCityEntry(avistamiento['city'], avistamiento)
        lt.addLast(entry['lstSights'], avistamiento)
        mp.put(offenseIndex, avistamiento['OFFENSE_CODE_GROUP'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], avistamiento)
    return cityentry
    """
# Funciones para creacion de datos

def newCityEntry(avistamiento):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'CityIndex': None, 'lstSights': None}
    entry['CityIndex'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareOffenses)
    entry['lstSights'] = lt.newList('SINGLE_LINKED', compareCities)
    return entry
    

# Funciones de consulta
def SightSize(analyzer):
    """
    Numero de avistamientos leidos
    """
    return lt.size(analyzer['ufos_list'])




# Funciones utilizadas para comparar elementos dentro de una lista
def compareCity(city1, city2):
    """
    Compara dos ciudades 
    """
    if (city1 == city1):
        return 0
    elif (city1 > city1):
        return 1
    else:
        return -1


# Funciones de ordenamiento
