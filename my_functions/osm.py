# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:30:45 2021

@author: Mariano
"""
import requests
import json
import pandas as pd
import time
import sys

def get_tag(layer, tag, key):
    '''
    Realiza queries a OpenStreetMap y almacena los datos en un dataframe. Los 
    nodos los almacena como puntos y las areas las almacena como puntos tambien 
    (siendo el centro del area la posicion de ese punto).
    
    Apartado TFM: "3.1.6 Almacenamiento de los datos"

    Parameters
    ----------
    layer : string
        sector economico.
    tag : string
        etiqueta de OpenStreetMap.
    key : string
        valor de la etiqueta de OpenStreetMap de los nodos y areas que vamos 
        a descargar de OpenStreetMap.

    Returns
    -------
    df : dataframe
        nodos y ways del sector economico que hemos descargado de OSM.
    data_node : dict
        todos los datos que nos ha proporcionado la query de nodos de OSM.
    data_way : dict
        todos los datos que nos ha proporcionado la query de ways de OSM.

    '''
    
    print("Start get " + tag +": " + key)
    df = pd.DataFrame(columns = ['id','lon','lat','layer','hover','name'])
    id_row = 0
    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = '''
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    (node["''' + tag + '''"="'''+key+'''"](area);
    );
    out center;
    '''
    print(overpass_query)
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data_node = response.json()

        for element in data_node['elements']:
            if element['type'] == 'node':
                lon = element['lon']
                lat = element['lat']
            elif 'center' in element:
                lon = element['center']['lon']
                lat = element['center']['lat']
            try:
                name = element['tags']['name']
            except:
                name = ''
            osm_id = element['id']
            hover = element['tags'][tag]
            df.loc[id_row] = [osm_id, lon, lat, layer, hover, name]
            id_row = id_row + 1

    except:
        print("    Get "+key + " FAILED:")
        print(sys.exc_info()[0])
    
    time.sleep(10)

    overpass_query = '''
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    (way["'''+tag+'''"="'''+key+'''"](area);
    );
    out center;
    '''
    print(overpass_query)
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data_way = response.json()

        for element in data_way['elements']:
            if element['type'] == 'node':
                lon = element['lon']
                lat = element['lat']
            elif 'center' in element:
                lon = element['center']['lon']
                lat = element['center']['lat']
            try:
                name = element['tags']['name']
            except:
                name = ''
            osm_id = element['id']
            hover = element['tags'][tag]
            df.loc[id_row] = [osm_id, lon, lat, layer, hover, name]
            id_row = id_row + 1

    except:
        print("    Get "+key + " FAILED:")
        print(sys.exc_info()[0])
        
    print("End get "+tag+": " + key)
    return df, data_node, data_way
    
def get_node(layer, tag, key):
    '''
    Realiza queries a OpenStreetMap y almacena los datos en un dataframe.
    
    Apartado TFM: "3.1.6 Almacenamiento de los datos"

    Parameters
    ----------
    layer : string
        sector economico.
    tag : string
        etiqueta de OpenStreetMap.
    key : string
        valor de la etiqueta de OpenStreetMap de los nodos que vamos
        a descargar de OpenStreetMap.

    Returns
    -------
    df : dataframe
        nodos del sector economico que hemos descargado de OSM.
    data : dict
        todos los datos que nos ha proporcionado la query de nodos de OSM.

    '''
    
    print("Start get " + tag +": " + key)
    df = pd.DataFrame(columns = ['id','lon','lat','layer','hover','name'])
    id_row = 0
    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = '''
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    (node["''' + tag + '''"="'''+key+'''"](area);
    );
    out center;
    '''
    print(overpass_query)
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        for element in data['elements']:
            if element['type'] == 'node':
                lon = element['lon']
                lat = element['lat']
            elif 'center' in element:
                lon = element['center']['lon']
                lat = element['center']['lat']
            try:
                name = element['tags']['name']
            except:
                name = ''
            osm_id = element['id']
            hover = element['tags'][tag]
            df.loc[id_row] = [osm_id, lon, lat, layer, hover, name]
            id_row = id_row + 1

    except:
        print("    Get "+key + " FAILED:")
        print(sys.exc_info()[0])
        
    print("End get "+tag+": " + key)
    return df, data

def get_way_as_point(layer, tag, key):
    '''
    Realiza queries a OpenStreetMap y almacena los datos en un dataframe. las 
    areas las almacena como puntos (siendo el centro del area la posicion de 
    ese punto).
    
    Apartado TFM: "3.1.6 Almacenamiento de los datos"

    Parameters
    ----------
    layer : string
        sector economico.
    tag : string
        etiqueta de OpenStreetMap.
    key : string
        valor de la etiqueta de OpenStreetMap de los ways que vamos
        a descargar de OpenStreetMap.

    Returns
    -------
    df : dataframe
        nodos del sector economico que hemos descargado de OSM..
    data : dict
        todos los datos que nos ha proporcionado la query de ways de OSM.

    '''
    
    print("Start get " + tag +": " + key)
    df = pd.DataFrame(columns = ['id','lon','lat','layer','hover','name'])
    id_row = 0
    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = '''
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    (way["''' + tag + '''"="'''+key+'''"](area);
    );
    out center;
    '''
    print(overpass_query)
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        for element in data['elements']:
            if element['type'] == 'node':
                lon = element['lon']
                lat = element['lat']
            elif 'center' in element:
                lon = element['center']['lon']
                lat = element['center']['lat']
            try:
                name = element['tags']['name']
            except:
                name = ''
            osm_id = element['id']
            hover = element['tags'][tag]
            df.loc[id_row] = [osm_id, lon, lat, layer, hover, name]
            id_row = id_row + 1

    except:
        print("    Get "+key + " FAILED:")
        print(sys.exc_info()[0])
        
    print("End get "+tag+": " + key)
    return df, data

def get_area(layer, tag, key):
    '''
    Realiza queries a OpenStreetMap y almacena los datos en un dataframe. Las 
    areas las almacena como puntos (siendo el centro del area la posicion de 
    ese punto).
    
    Apartado TFM: "3.1.6 Almacenamiento de los datos"

    Parameters
    ----------
    layer : string
        sector economico.
    tag : string
        etiqueta de OpenStreetMap.
    key : string
        valor de la etiqueta de OpenStreetMap de las areas que vamos
        a descargar de OpenStreetMap.

    Returns
    -------
    df : dataframe
        nodos del sector economico que hemos descargado de OSM.
    data : dict
        todos los datos que nos ha proporcionado la query de areas de OSM.

    '''
    
    print("Start get " + tag +": " + key)
    df = pd.DataFrame(columns = ['id','lon','lat','layer','hover','name'])
    id_row = 0
    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = '''
    [out:json];
    area["ISO3166-1"="ES"][admin_level=2];
    (area["''' + tag + '''"="'''+key+'''"](area);
    );
    out center;
    '''
    print(overpass_query)
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        for element in data['elements']:
            if element['type'] == 'node':
                lon = element['lon']
                lat = element['lat']
            elif 'center' in element:
                lon = element['center']['lon']
                lat = element['center']['lat']
            try:
                name = element['tags']['name']
            except:
                name = ''
            osm_id = element['id']
            hover = element['tags'][tag]
            df.loc[id_row] = [osm_id, lon, lat, layer, hover, name]
            id_row = id_row + 1

    except:
        print("    Get "+key + " FAILED:")
        print(sys.exc_info()[0])
        
    print("End get "+tag+": " + key)
    return df, data

def adjust_sites_df_net(df_ini):
    '''
    Modifica las columnas del dataframe de estaciones para representarlas 
    graficamente en un mapa, donde se pueda resaltar las diferentes posiciones 
    de las estaciones segun el operador de red.
    
    Apartado TFM: "3.2.9 Resumen de Infraestructura de red movil"

    Parameters
    ----------
    df_ini : dataframe
        estaciones de entrada.

    Returns
    -------
    df : dataframe
        estaciones con las columnas modificadas para ser representadas en un 
        mapa.

    '''
    
    df = df_ini.copy()
        
    df = df[['enbid', 'site_lat', 'site_lon', 'net', 'n_cells', 'name']]
    df.loc[df.net==1, 'net'] = "Vodafone"
    df.loc[df.net==7, 'net'] = "Movistar"
    df.loc[df.net==3, 'net'] = "Orange"
    df.loc[df.net == 4, 'net'] = "Yoigo"
    df.n_cells = df.enbid.astype(str) + ": " \
                + df.n_cells.astype(str) + " cells"
    
    df.rename(columns={'enbid':'id','site_lat':'lat','site_lon':'lon',\
                       'net':'layer','n_cells':'hover'},\
              inplace=True)
    return df

def adjust_sites_df_cap(df_ini):
    '''
    Modifica las columnas del dataframe de estaciones para representarlas 
    graficamente en un mapa, donde se pueda resaltar las diferentes posiciones 
    de las estaciones segun su capacidad.
    
    Apartado TFM: "3.2.6 Calculo de la capcidad de las estaciones"

    Parameters
    ----------
    df_ini : dataframe
        estaciones de entrada.

    Returns
    -------
    df : dataframe
        estaciones con las columnas modificadas para ser representadas en un 
        mapa.

    '''
    
    df = df_ini.copy()
        
    df = df[['enbid', 'site_lat', 'site_lon', 'cap_type', 'n_cells', 'name']]
    df.loc[df.cap_type=='low', 'cap_type'] = "Low"
    df.loc[df.cap_type=='medium', 'cap_type'] = "Medium"
    df.loc[df.cap_type=='high', 'cap_type'] = "High"

    df.n_cells = df.enbid.astype(str) + ": " \
                + df.n_cells.astype(str) + " cells"
    
    df.rename(columns={'enbid':'id','site_lat':'lat','site_lon':'lon',\
                       'cap_type':'layer','n_cells':'hover'},\
              inplace=True)
    return df