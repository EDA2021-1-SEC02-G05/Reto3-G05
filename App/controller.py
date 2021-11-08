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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de avistamientos

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    avisfile = cf.data_dir + '/UFOS/UFOS-utf8-large.csv'
    input_file = csv.DictReader(open(avisfile, encoding="utf-8"),
                                delimiter=",")
    for avistamiento in input_file:
        model.addAvistamiento(analyzer, avistamiento)
    sortDurationIndex(analyzer)
    sortDateIndex(analyzer)
    sortTimeIndex(analyzer)
    sortTimeIndex2(analyzer)
    return analyzer


# Funciones de ordenamiento
def sortDurationIndex(analyzer):

    return model.sortDurationIndex(analyzer)

def sortDateIndex(analyzer):

    return model.sortDateIndex(analyzer)

def sortTimeIndex(analyzer):

    return model.sortTimeIndex(analyzer)

def sortTimeIndex2(analyzer):

    return model.sortTimeIndex2(analyzer)

# Funciones de consulta sobre el catálogo
def getCitySights (analyzer, city):

    return model.getCitySights(analyzer, city)

def getDurationSights(analyzer,lim_inf, lim_sup):

    return model.getDurationSights(analyzer, lim_inf, lim_sup)

def getreq3(analyzer, lim_inf, lim_sup):
    
    return model.getreq3(analyzer, lim_inf, lim_sup)

def getSightsinRange(analyzer, lim_inf, lim_sup):

    return model.getSightsinRange(analyzer, lim_inf, lim_sup)

def getSightsLocation(analyzer, lim_longitudmin, lim_longitudmax, lim_latitudmin, lim_latitudmax):

    return model.getSightsLocation(analyzer, lim_longitudmin, lim_longitudmax, lim_latitudmin, lim_latitudmax)

def getMapLocation(respuesta, lim_longitudmin,lim_longitudmax, lim_latitudmin,lim_latitudmax):

    return model.getMapLocation(respuesta, lim_longitudmin,lim_longitudmax, lim_latitudmin,lim_latitudmax)
