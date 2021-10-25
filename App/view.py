﻿"""
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
    print("2- ")
    print('3- Contar los avistamientos en una ciudad')
    print('4- Contar los avistamientos por duración')
    print('5- Contar avistamientos por Hora/Minutos del día')
    print('6- Contar los avistamientos en un rango de fechas')
    print('7- Contar los avistamientos de una Zona Geográfica')



catalog = None

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


    else:
        sys.exit(0)
sys.exit(0)
