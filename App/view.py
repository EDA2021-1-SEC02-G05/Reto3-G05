"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
assert cf



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar el catálogo")
    print("2- Cargar datos al catálogo")
    #print('3- Altura y elementos del arbol (lab 8)')
    print('3- Contar los avistamientos en una ciudad (Req-1)')
    print('4- Contar los avistamientos por duración (Req-2)')
    print('5- Contar avistamientos por Hora/Minutos del día (Req-3)')
    print('6- Contar los avistamientos en un rango de fechas (Req-4)')
    print('7- Contar los avistamientos de una Zona Geográfica (Req-5)')
    print('8- Representación gráfica del requerimiento 5 (Bono)')
    print('0- Exit')

catalog = None

def printReq1(analyzer, avistamientos, city):
    size_total = mp.size(analyzer['Sightings_per_city'])
    size_city = lt.size(avistamientos)
    print('El total de ciudades donde se han reportado avistamientos es de: ' + str(size_total)+'\n')
    print('En la ciudad ' + city + ' se reportaron en total '+ str(size_city)+ ' avistamientos.\n')
    print('Los primeros 3 y últimos 3 avistamientos en la ciudad son: \n')

    if size_city > 6:

        first3 = lt.subList(avistamientos,1,3)
        last3 = lt.subList(avistamientos,size_city - 2,3)

        for avis in lt.iterator(first3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')
        
        for avis in lt.iterator(last3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')
    else:
        for avis in lt.iterator(avistamientos):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

def printReq2( lim_inf, lim_sup,duracionlst, mayordur, mayordur_size):
    size = lt.size(duracionlst)
    print('Se encontraron ' + str(size) + ' avistamientos con duraciones entre: '+ str(lim_inf) + '-'+str(lim_sup) + ' s.\n')

    print('La mayor duración reportada fue de: ' + str(mayordur) + ' s y en esta se reportaron ' + str(mayordur_size) + ' avistamientos.\n')

    print('Los primeros 3 y ultimos 3 avistamientos en el rango de duración solicitado son: \n')

    if size > 6:

        first3 = lt.subList(duracionlst,1,3)
        last3 = lt.subList(duracionlst,size - 2,3)

        for avis in lt.iterator(first3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')
        
        for avis in lt.iterator(last3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

    else:
        for avis in lt.iterator(duracionlst):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

def printReq3(timelst,oldest_time,oldest_size, lim_inf,lim_sup):
    
    size = lt.size(timelst)

    print('Se encontraron ' + str(size) + ' avistamientos ocurridos en fechas entre: '+ str(lim_inf) + ' y '+str(lim_sup) + '\n')

    print('La hora más antigua reportada de un avistamiento es ' + str(oldest_time) + ' y se encontraron ' + str(oldest_size) + ' avistamientos con esta hora.\n')

    print('Los primeros 3 y ultimos 3 avistamientos en el rango de fechas solicitadas son: \n')

    if size > 6:

        first3 = lt.subList(timelst,1,3)
        last3 = lt.subList(timelst,size - 2,3)

        for avis in lt.iterator(first3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')
        
        for avis in lt.iterator(last3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

    else:
        for avis in lt.iterator(timelst):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')


def printReq4(datelst,oldest_date,oldest_size, lim_inf,lim_sup):
    size = lt.size(datelst)

    print('Se encontraron ' + str(size) + ' avistamientos ocurridos en fechas entre: '+ str(lim_inf) + ' y '+str(lim_sup) + '\n')

    print('La fecha más antigua reportada de un avistamiento es ' + str(oldest_date) + ' y se encontraron ' + str(oldest_size) + ' avistamientos con esta fecha.\n')

    print('Los primeros 3 y ultimos 3 avistamientos en el rango de fechas solicitadas son: \n')

    if size > 6:

        first3 = lt.subList(datelst,1,3)
        last3 = lt.subList(datelst,size - 2,3)

        for avis in lt.iterator(first3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')
        
        for avis in lt.iterator(last3):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

    else:
        for avis in lt.iterator(datelst):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + '\n')

def printReq5(respuesta, lim_longitudmin, lim_longitudmax, lim_latitudmin,lim_latitudmax ):

    size = lt.size(respuesta)

    print('Se encontraron ' + str(size) + ' avistamientos con una longitud entre ' + str(lim_longitudmin) + ' y ' + str(lim_longitudmax) + ' y con una latitud entre ' + str(lim_latitudmin) + ' y ' + str(lim_latitudmax) + '\n')
    print('A conitnuación se muestran los primeros 5 y últimos 5 avistamientos en el rango: \n')

    if size > 10 :

        first5 = lt.subList(respuesta,1,5)
        last5 = lt.subList(respuesta,size - 4,5)

        for avis in lt.iterator(first5):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + ', Latitud: ' + str(round(float(avis['latitude']),3)) + ', Longitud: ' + str(round(float(avis['longitude']),3)) +'\n')
        
        for avis in lt.iterator(last5):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + ', Latitud: ' + str(round(float(avis['latitude']),3)) + ', Longitud: ' + str(round(float(avis['longitude']), 3)) +'\n')

    else:
        for avis in lt.iterator(respuesta):
            print('Fecha y hora: ' + avis['datetime'] + ', Ciudad: ' + avis['city'] + ', País: ' + avis['country'] + ', Duración en segundos: ' + avis['duration (seconds)'] + ', Forma del objeto: ' + avis['shape'] + ', Latitud: ' + str(round(float(avis['latitude']), 3)) + ', Longitud: ' + str(round(float(avis['longitude']), 3)) +'\n')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        
        analyzer = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(analyzer)

        size = lt.size(analyzer['ufos_list'])

        print('El total de avistamiento cargados es de: '+ str(size))
        print('\nLos primeros y últimos 5 avistamientos con su información correspondiente son: ')

        first5 = lt.subList(analyzer['ufos_list'],1,5)
        last5 = lt.subList(analyzer['ufos_list'], size - 4 ,5)

        for sighting in lt.iterator(first5):
            print(sighting)

        print('\n-------------------------------------------------------\n')

        for sighting in lt.iterator(last5):
            print(sighting)

    elif int(inputs[0]) == 3:
        """
        LAB 8
        
        elements = om.size(analyzer['Sightings_citylab'])
        height = om.height(analyzer['Sightings_citylab'])
        

        print('Número de elementos en el arbol: ' + str(elements))
        print('Altura del arbol: ' + str(height))
        """
        city = (input('Nombre de la ciudad a consultar: ')).lower()

        avistamientos = controller.getCitySights(analyzer,city)

        printReq1(analyzer, avistamientos, city)
    
    elif int(inputs[0]) == 4:

        lim_inf = float(input('Menor duración en segundos a consultar: '))
        lim_sup = float(input('Mayor duración en segundos a consultar: '))

        duracion = controller.getDurationSights(analyzer,lim_inf,lim_sup)

        printReq2( lim_inf, lim_sup,duracion[0], duracion[1], duracion[2])

    elif int(inputs[0]) == 5:
        lim_inf = input('limite inferior del rango a consultar (HH:MM:SS): ')
        lim_sup = input('limite superior del rango a consultar (HH:MM:SS): ')

        respuesta = controller.getreq3(analyzer,lim_inf,lim_sup)

        printReq3(respuesta[0],respuesta[1], respuesta[2], lim_inf,lim_sup)


    elif int(inputs[0]) == 6:

        lim_inf = input('limite inferior del rango a consultar (AAAA-MM-DD): ')
        lim_sup = input('limite superior del rango a consultar (AAAA-MM-DD): ')

        rango = controller.getSightsinRange(analyzer, lim_inf, lim_sup)

        printReq4(rango[0],rango[1], rango[2], lim_inf,lim_sup)

    elif int(inputs[0]) == 7:

        lim_longitudmin = float(input('límite mínimo de longitud: '))
        lim_longitudmax= float(input('límite máximo de longitud: '))

        lim_latitudmin = float(input('límite mínimo de latitud:  '))
        lim_latitudmax = float(input('límite máximo de latitud:  '))

        respuesta = controller.getSightsLocation(analyzer, lim_longitudmin, lim_longitudmax, lim_latitudmin, lim_latitudmax)

        printReq5(respuesta, lim_longitudmin, lim_longitudmax, lim_latitudmin,lim_latitudmax )


    elif int(inputs[0]) == 8:

        controller.getMapLocation(respuesta, lim_longitudmin,lim_longitudmax, lim_latitudmin,lim_latitudmax)

    else:
        sys.exit(0)
sys.exit(0)
