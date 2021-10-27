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
from DISClib.Algorithms.Sorting import mergesort as ms
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
                'Sightings_citylab':None,
                'Sightings_per_city': None,
                'Sightings_per_duration':None,
                'Sightings_per_date': None,
                }

    analyzer['ufos_list'] = lt.newList('ARRAY_LIST')
    #analyzer['Sightings_citylab'] = om.newMap('RTB',
    #                                         comparefunction = compareCityLab)
    analyzer['Sightings_per_city'] = mp.newMap(numelements = 100,
                                                maptype='PROBBING',
                                                loadfactor=0.5,
                                                comparefunction=compareCity)
    analyzer['Sightings_per_duration'] = om.newMap('RBT',
                                                   comparefunction = compareduration)
    analyzer['Sightings_per_date'] = om.newMap('RBT',
                                                comparefunction = comparedates)
    return analyzer

# Funciones para agregar informacion al catalogo
def addAvistamiento(analyzer, avistamiento):

    lt.addLast(analyzer['ufos_list'], avistamiento)
    #updateCityIndexlab(analyzer['Sightings_citylab'], avistamiento)
    updateCityIndex(analyzer['Sightings_per_city'], avistamiento)
    updateDurationIndex(analyzer['Sightings_per_duration'], avistamiento)
    updateDateIndex(analyzer['Sightings_per_date'], avistamiento)
    return analyzer

def updateCityIndexlab(map,avistamiento):
    city = avistamiento['city']
    
    entry = om.get(map, city)
    if entry is None:
        cityentry = newCityEntrylab(city, avistamiento)
        om.put(map, city, cityentry)
    else:
        cityentry = me.getValue(entry) 
    lt.addLast(cityentry['Sightslst'],avistamiento)
    return map

def updateCityIndex(map, avistamiento):
    city = avistamiento['city']
    
    entry = mp.get(map, city)
    if entry is None:
        cityentry = newCityEntry(city)
        mp.put(map, city, cityentry)

    else:
        cityentry = me.getValue(entry)

    addDateIndex(cityentry, avistamiento)
    return map

def addDateIndex(cityentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    date = datetime.datetime.strptime(avistamiento['datetime'], '%Y-%m-%d %H:%M:%S')
  
    date_index = cityentry['DateSightsIndex']

    entry = om.get(date_index, date)

    if entry is None:
        datentry = newDateEntry(date)
        lt.addLast(datentry['Sightslst'],avistamiento)
        om.put(date_index,date,datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry['Sightslst'], avistamiento)

    return cityentry

def updateDurationIndex(map, avistamiento):
    duration = avistamiento['duration (seconds)'].split('.')

    entry = om.get(map, int(duration[0]))

    if entry is None:
        durationentry = newDurationEntrylab(int(duration[0]))
        om.put(map, int(duration[0]), durationentry)
    else:
        durationentry = me.getValue(entry) 
    lt.addLast(durationentry['Sightslst'],avistamiento)
    return map

def sortDurationIndex(analyzer):

    duration_omap = analyzer['Sightings_per_duration']

    duration_keys = om.keySet(duration_omap)

    for key in lt.iterator(duration_keys):
        duration_entry = om.get(duration_omap, key)
        sights_list = me.getValue(duration_entry)
        sortduration(sights_list['Sightslst'])

def updateDateIndex(map, avistamiento):

    date = datetime.datetime.strptime(avistamiento['datetime'], '%Y-%m-%d %H:%M:%S')

    entry = om.get(map,date.date())

    if entry is None:
        datentry = newDateEntryreq4(date)
        lt.addLast(datentry['Sightslst'],avistamiento)
        om.put(map,date.date(),datentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry['Sightslst'], avistamiento)

    return map
    
# Funciones para creacion de datos

def newCityEntrylab(city, avistamiento):
    entry = {'City': city, 'Sightslst': None}

    entry['Sightslst'] = lt.newList('ARRAT_LIST', cmpfunction = cmpdateslab)

    return entry


def newCityEntry(city):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'City': city, 'DateSightsIndex': None}
    entry['DateSightsIndex'] = om.newMap('RTB',
                                         comparefunction = omapcmpDate)
    return entry
    
def newDateEntry(date):
    entry = {'Date': date, 'Sightslst': None}

    entry['Sightslst'] = lt.newList('ARRAY_LIST', cmpfunction = cmphour)

    return entry

def newDurationEntrylab(duration):
    entry = {'Duration': duration, 'Sightslst':None}

    entry['Sightslst'] = lt.newList('ARRAY_LIST')

    return entry

def newDateEntryreq4(date):

    entry = {'Date': date, 'Sightslst': None}

    entry['Sightslst'] = lt.newList('ARRAY_LIST')

    return entry


# Funciones de consulta

def getCitySights (analyzer, city):
    avistamientoslst = lt.newList('ARRAY_LIST', cmpfunction = cmphour)

    cityentry = mp.get(analyzer['Sightings_per_city'],city)
    city_dateindex = me.getValue(cityentry) 
    city_date_keys = om.keySet(city_dateindex['DateSightsIndex'])

    for date in lt.iterator(city_date_keys):
        datetry = om.get(city_dateindex['DateSightsIndex'], date)
        date_value = me.getValue(datetry)

        for avistamiento in lt.iterator(date_value['Sightslst']):
            lt.addLast(avistamientoslst,avistamiento)

    return avistamientoslst

def getDurationSights(analyzer,lim_inf, lim_sup):

    durationlst = lt.newList('ARRAY_LIST')

    duration_omap = analyzer['Sightings_per_duration']
    duration_max = om.maxKey(duration_omap)
    duration_max_entry = om.get(duration_omap,duration_max )
    duration_max_value = me.getValue(duration_max_entry)
    duration_max_size = lt.size(duration_max_value['Sightslst'])
    duration_rangevalues = om.values(duration_omap, lim_inf, lim_sup) 

    for value in lt.iterator(duration_rangevalues):
        for avis in lt.iterator(value['Sightslst']):
            lt.addLast(durationlst,avis)


    return durationlst, duration_max, duration_max_size

def getSightsinRange(analyzer, lim_inf, lim_sup):
    #lim_inf_split = (lim_inf).split('-')
    #(int(lim_inf_split[0]),int(lim_inf_split[1]),int(lim_inf_split[2]))
    lim_inf_f = (datetime.datetime.strptime(lim_inf,'%Y-%m-%d')).date()
    lim_sup_f = (datetime.datetime.strptime(lim_sup,'%Y-%m-%d')).date()
    rangelst = lt.newList('ARRAY_LIST')

    date_omap = analyzer['Sightings_per_date']
    date_oldest = om.minKey(date_omap)
    date_oldest_entry = om.get(date_omap,date_oldest)
    date_oldest_value = me.getValue(date_oldest_entry)
    date_oldest_size = lt.size(date_oldest_value['Sightslst'])
    date_inrange = om.values(date_omap,lim_inf_f,lim_sup_f)

    #habrá que organizar por hora tbn?

    for date in lt.iterator(date_inrange):
        for avis in lt.iterator(date['Sightslst']):
            lt.addLast(rangelst,avis)

    return rangelst, date_oldest, date_oldest_size
# Funciones utilizadas para comparar elementos dentro de una lista

def compareCityLab(city1, city2):
    """
    Compara dos ciudades 
    """
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1

def compareCity(city1, entry):
    """
    Compara dos ciudades 
    """
    city2entry = me.getKey(entry)
    if (city1 == city2entry):
        return 0
    elif (city1 > city2entry):
        return 1
    else:
        return -1

def compareduration(duration1,duration2):
    if (duration1 == duration2):
        return 0
    elif (duration1 > duration2):
        return 1
    else:
        return -1

def comparedates(date1,date2):

    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def cmpdateslab (date1,date2):
    
    """
    Compara dos fechas
    """
    
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def cmphour (hour1,hour2):

    date1 = datetime.datetime.strptime(hour1['datetime'], '%Y-%m-%d %H:%M:%S')
    date2 = datetime.datetime.strptime(hour2['datetime'], '%Y-%m-%d %H:%M:%S')

    hour1_num = date1.time()
    hour2_num = date2.time()

    return hour1_num < hour2_num

def omapcmpDate (date1,date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def cmpdur(avis1, avis2):

    return (avis1['city'] +'-'+ avis1['country']) < (avis2['city'] +'-'+ avis2['country'])

# Funciones de ordenamiento

def sortduration(list):

    ms.sort(list, cmpdur)