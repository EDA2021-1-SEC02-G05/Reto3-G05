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

def printReq2(analyzer, lim_inf, lim_sup,duracionlst, mayordur, mayordur_size):
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
        """
        elements = om.size(analyzer['Sightings_citylab'])
        height = om.height(analyzer['Sightings_citylab'])
        

        print('Número de elementos en el arbol: ' + str(elements))
        print('Altura del arbol: ' + str(height))
        
        city = (input('Nombre de la ciudad a consultar: ')).lower()

        avistamientos = controller.getCitySights(analyzer,city)

        printReq1(analyzer, avistamientos, city)
    
    elif int(inputs[0]) == 4:

        lim_inf = int(input('Menor duración en segundos a consultar: '))
        lim_sup = int(input('Mayor duración en segundos a consultar: '))

        duracion = controller.getDurationSights(analyzer,lim_inf,lim_sup)

        printReq2(analyzer, lim_inf, lim_sup,duracion[0], duracion[1], duracion[2])

    elif int(inputs[0]) == 5:
        papa = 2


    elif int(inputs[0]) == 6:

        lim_inf = 3

        




    else:
        sys.exit(0)
sys.exit(0)
