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
import folium
from IPython.display import display
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
                'Sightings_per_time': None,
                'Sightings_per_date': None,
                'Sightings_per_location':None,
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
    analyzer['Sightings_per_time'] = om.newMap('RBT',
                                                comparefunction = comparetime)
    analyzer['Sightings_per_date'] = om.newMap('RBT',
                                                comparefunction = comparedates)
    analyzer['Sightings_per_location'] = om.newMap('RBT',
                                                comparefunction = comparelatitudes)
                            
    return analyzer

# Funciones para agregar informacion al catalogo
def addAvistamiento(analyzer, avistamiento):

    lt.addLast(analyzer['ufos_list'], avistamiento)
    #updateCityIndexlab(analyzer['Sightings_citylab'], avistamiento)
    updateCityIndex(analyzer['Sightings_per_city'], avistamiento)
    updateDurationIndex(analyzer['Sightings_per_duration'], avistamiento)
    updateTimeIndex(analyzer['Sightings_per_time'], avistamiento)
    updateDateIndex(analyzer['Sightings_per_date'], avistamiento)
    updateLatitudIndex(analyzer['Sightings_per_location'], avistamiento)

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
    duration = float(avistamiento['duration (seconds)'])

    entry = om.get(map, duration)

    if entry is None:
        durationentry = newDurationEntrylab(duration)
        om.put(map, duration, durationentry)
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
###
def updateTimeIndex(map, avistamiento):

    date = datetime.datetime.strptime(avistamiento['datetime'], '%Y-%m-%d %H:%M:%S')
    #time = datetime.time(int(date.hour), int(date.minute))
    
    time= date.time()
    
    entry = om.get(map,time)

    if entry is None:
        timentry = newTimeEntry(time)
        lt.addLast(timentry['Sightslst'],avistamiento)
        om.put(map,time,timentry)
    else:
        datentry = me.getValue(entry)
        lt.addLast(datentry['Sightslst'], avistamiento)

    return map

def sortTimeIndex(analyzer):
    time_omap = analyzer['Sightings_per_time']

    time_keys = om.keySet(time_omap)

    for key in lt.iterator(time_keys):
        time_entry = om.get(time_omap, key)
        sights_list = me.getValue(time_entry)
        sortdate(sights_list['Sightslst'])
        

def sortTimeIndex2(analyzer):
    time_omap = analyzer['Sightings_per_time']

    time_keys = om.keySet(time_omap)

    for key in lt.iterator(time_keys):
        time_entry = om.get(time_omap, key)
        sights_list = me.getValue(time_entry)
        
        sortreq3(sights_list['Sightslst'])

####
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

def sortDateIndex(analyzer):
    date_omap = analyzer['Sightings_per_date']

    date_keys = om.keySet(date_omap)

    for key in lt.iterator(date_keys):
        date_entry = om.get(date_omap, key)
        sights_list = me.getValue(date_entry)
        sortdate(sights_list['Sightslst'])

def updateLatitudIndex(map, avistamiento):
    latitud = round(float(avistamiento['latitude']), 2)
    
    entry = om.get(map, latitud)
    if entry is None:
        latitudentry = newlatitudEntry(latitud)
        om.put(map, latitud, latitudentry)

    else:
        latitudentry = me.getValue(entry)

    addLongitudIndex(latitudentry, avistamiento)

    return map

def addLongitudIndex(latitudentry, avistamiento):

    longitud = round(float(avistamiento['longitude']), 2)
    latitud_index = latitudentry['LongitudeTree']

    entry = om.get(latitud_index, longitud)

    if entry is None:
        longitudentry = newLongitudEntry(longitud)
        lt.addLast(longitudentry['Sightslst'],avistamiento)
        om.put(latitud_index,longitud,longitudentry)
    else:
        longitudentry = me.getValue(entry)
        lt.addLast(longitudentry['Sightslst'], avistamiento)

    return latitudentry

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

def newTimeEntry(time):

    entry = {'Time': time, 'Sightslst': None}

    entry['Sightslst'] = lt.newList('ARRAY_LIST')

    return entry

def newDateEntryreq4(date):

    entry = {'Date': date, 'Sightslst': None}

    entry['Sightslst'] = lt.newList('ARRAY_LIST')

    return entry

def newlatitudEntry(latitud):

    entry = {'Latitude': latitud, 'LongitudeTree': None}

    entry['LongitudeTree'] = om.newMap('RBT',
                                    comparefunction = comparelongitudes)

    return entry

def newLongitudEntry(longitud):

    entry = {'Longitud': longitud, 'Sightslst': None}

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

def getreq3(analyzer, lim_inf, lim_sup):

    date1 = datetime.datetime.strptime(lim_inf, '%H:%M:%S')
    date2 = datetime.datetime.strptime(lim_sup, '%H:%M:%S')

    hour1 = date1.time()
    hour2= date2.time()

    rangelst = lt.newList('ARRAY_LIST', cmpfunction = cmphour)

    time_omap = analyzer['Sightings_per_time']
    
    time_oldest = om.maxKey(time_omap)
    time_oldest_entry = om.get(time_omap,time_oldest)
    time_oldest_value = me.getValue(time_oldest_entry)
    time_oldest_size = lt.size(time_oldest_value['Sightslst'])
    
    time_inrange = om.values(time_omap,hour1,hour2)


    for time in lt.iterator(time_inrange):
        for avis in lt.iterator(time['Sightslst']):
            lt.addLast(rangelst,avis)


    return rangelst, time_oldest, time_oldest_size
# Funciones utilizadas para comparar elementos dentro de una lista

def getSightsinRange(analyzer, lim_inf, lim_sup):

    lim_inf_f = (datetime.datetime.strptime(lim_inf,'%Y-%m-%d')).date()
    lim_sup_f = (datetime.datetime.strptime(lim_sup,'%Y-%m-%d')).date()
    rangelst = lt.newList('ARRAY_LIST')

    date_omap = analyzer['Sightings_per_date']
    date_oldest = om.minKey(date_omap)
    date_oldest_entry = om.get(date_omap,date_oldest)
    date_oldest_value = me.getValue(date_oldest_entry)
    date_oldest_size = lt.size(date_oldest_value['Sightslst'])
    date_inrange = om.values(date_omap,lim_inf_f,lim_sup_f)


    for date in lt.iterator(date_inrange):
        for avis in lt.iterator(date['Sightslst']):
            lt.addLast(rangelst,avis)

    return rangelst, date_oldest, date_oldest_size

def getSightsLocation(analyzer, lim_longitudmin, lim_longitudmax, lim_latitudmin, lim_latitudmax):

    rangelst = lt.newList('ARRAY_LIST')

    latitude_tree = analyzer['Sightings_per_location']

    latitud_inrange = om.values(latitude_tree, lim_latitudmin, lim_latitudmax) 

    for latitud in lt.iterator(latitud_inrange):

        longitude_tree = latitud['LongitudeTree']

        longitud_inrange = om.values(longitude_tree,lim_longitudmin, lim_longitudmax )

        for longitud in lt.iterator(longitud_inrange):
            for avis in lt.iterator(longitud['Sightslst']):
                lt.addLast(rangelst,avis)


    return rangelst

def getMapLocation(respuesta, lim_longitudmin,lim_longitudmax, lim_latitudmin,lim_latitudmax):

    longitud_promedio = (float(lim_longitudmax) + float(lim_longitudmin))/2

    latitud_promedio = (float(lim_latitudmax) + float(lim_latitudmin))/2

    map = folium.Map(location=[latitud_promedio, longitud_promedio], tiles = 'Stamen Terrain', zoom_start=4)

    folium.Rectangle([(lim_latitudmin,lim_longitudmax),(lim_latitudmax,lim_longitudmin)],
                        fill = True,
                        fill_color = 'pink',
                        color = 'pink'
                        ).add_to(map)

    city_lst = []
    country_lst = []
    dt_lst = []
    dur_lst = []
    shp_lst = []
    lat_lst = []
    lon_lst = []

    for avis in lt.iterator(respuesta):
        city_lst.append(avis['city'])
        dt_lst.append(avis['datetime'])
        dur_lst.append(avis['duration (seconds)'])
        shp_lst.append(avis['shape'])
        lat_lst.append(float(avis['latitude']))
        lon_lst.append(float(avis['longitude']))
        country_lst.append(avis['country'])

    for dt, city, country , dur, shp, lat, lon in zip(dt_lst, city_lst,country_lst, dur_lst, shp_lst,lat_lst,lon_lst):

        loc = [lat,lon]
        data = 'Fecha y hora: ' + dt + ' , Ciudad: ' + city +' , País: '+ country+ ' , Duración en segundos: ' +dur + ' , Forma del objeto: ' + shp

        folium.Marker(
            location = loc,
            popup = folium.Popup(data,max_width=450),
            icon = folium.Icon(color = 'green', icon_color= 'yellow', icon = 'eye-open', prefix = 'glyphicon')
            ).add_to(map)

    map.save(outfile='mapa.html')

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
    if (float(duration1) == float(duration2)):
        return 0
    elif (float(duration1) > float(duration2)):
        return 1
    else:
        return -1

def comparetime(time1,time2):

    if (time1 == time2):
        return 0
    elif (time1 > time2):
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

def cmpfecha (hour1,hour2):

    date1 = datetime.datetime.strptime(hour1['datetime'], '%Y-%m-%d %H:%M:%S')
    date2 = datetime.datetime.strptime(hour2['datetime'], '%Y-%m-%d %H:%M:%S')

    hour1_num = date1.date()
    hour2_num = date2.date()

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

def comparelongitudes(long1, long2):
    if (float(long1) == float(long2)):
        return 0
    elif (float(long1) > float(long2)):
        return 1
    else:
        return -1

def comparelatitudes(lat1, lat2):

    if (float(lat1) == float(lat2)):
        return 0
    elif (float(lat1) > float(lat2)):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def sortduration(list):

    ms.sort(list, cmpdur)

def sortdate(list):
    
    ms.sort(list, cmphour)

def sortreq3(list):

    ms.sort(list, cmpfecha)
    