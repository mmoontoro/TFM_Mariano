# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:49:10 2021

@author: Mariano
"""
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from shapely.ops import nearest_points

import geopandas as gpd
from shapely.geometry import Point
from datetime import datetime

def nearest_total(df_sector, df_sites):
    '''
    Calcula la distancia desde cada nodo de un sector economico dado, hasta 
    la estaciones y celdas mas cercanas. Asigna esta informacion de distancias 
    al dataframe del sector economico. Devuelve este nuevo dataframe que ahora 
    contiene informacion sobre la conectividad movil de cada uno de sus nodos.
    
    Apartado TFM: "3.3.2 Caracterización de la conectividad movil"

    Parameters
    ----------
    df_sector : dataframe
        nodos de un sector economico.
    df_sites : dataframe
        estaciones.

    Returns
    -------
    df : dataframe
        nodos del sector economico con nuevas columnas con la informacion de
        distancia a las estaciones y celdas mas cercanas.

    '''
    print("-----------------------------------")
    print("Start find nearest cells")
    startTime = datetime.now()
    print(startTime)
    df = df_sector.copy()
    df_sites_800 = df_sites[df_sites.cells800 > 0]
    df_sites_900 = df_sites[df_sites.cells900 > 0]
    df_sites_1800 = df_sites[df_sites.cells1800 > 0]
    df_sites_2100 = df_sites[df_sites.cells2100 > 0]
    df_sites_2600 = df_sites[df_sites.cells2600 > 0]
    df_sites_medium = df_sites[df_sites.cap_type == "medium"]
    df_sites_high = df_sites[df_sites.cap_type == "high"]
    df_sites_low = df_sites[df_sites.cap_type == "low"]
    
    df['nst_low'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_low), axis=1)
    print("    Nearest low capacity site completed")
    df['nst_medium'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_medium), axis=1)
    print("    Nearest medium capacity site completed")
    df['nst_high'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_high), axis=1)
    print("    Nearest high capacity site completed")
    
    df['nst_site'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites), axis=1)
    print("    Nearest site completed")
    
    df['nst_800'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_800), axis=1)
    print("    Nearest 800 cells completed")
    df['nst_900'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_900), axis=1)
    print("    Nearest 900 cells completed")
    df['nst_1800'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_1800), axis=1)
    print("    Nearest 1800 cells completed")
    df['nst_2100'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_2100), axis=1)
    print("    Nearest 2100 cells completed")
    df['nst_2600'] = \
        df.apply(lambda row: nearest(row.geometry, df_sites_2600), axis=1)
    print("    Nearest 2600 cells completed")
    endtime = datetime.now()
    print(endtime)
    print("End find nearest cells")
    print("-----------------------------------")
    return df

def nearest(point, df):
    '''
    Calcula la distancia en kilometros desde un punto dado, a otro punto (el 
    punto mas cercano al primero de entre todos los puntos de un dataframe 
    dado).


    Apartado TFM: "3.3.2 Caracterización de la conectividad movil"

    Parameters
    ----------
    point : point
        punto.
    df : dataframe
        dataframe de puntos, de entre los cuales encontraremos el mas cercano.

    Returns
    -------
    dist_km : float
        distancia en km desde el punto al punto mas cercano del dataframe.

    '''
    pts = df.geometry.unary_union
    nearest = df.geometry == nearest_points(point, pts)[1]
    lat_site = df[nearest].geometry.values[0].y
    lon_site = df[nearest].geometry.values[0].x
    dist_km = distance_calc(lat_site, lon_site, point.y, point.x)
    return dist_km

def create_map_pop(muni_ini, pop_ini):
    '''
    Crea un geodataframe de los poligonos de todos los municipios, añadiendo 
    informacion de la poblacion de cada municipio.
    
    Apartado TFM: "3.1.7 Asignacion de información geográfica"
    Apartado TFM: "3.2.7 Asignacion de información geográfica"

    Parameters
    ----------
    muni_ini : geodataframe
        poligonos de todos los municipios de españa sin datos de poblacion.
    pop_ini : dataframe
        datos de poblacion por municipio en españa.

    Returns
    -------
    muni_pop : geodataframe
        poligonos de todos los municipios de españa con datos de poblacion.

    '''
    print("-----------------------------------")
    print("Start create map")
    startTime = datetime.now()
    print(startTime)
    muni = muni_ini[['CLAU2','NPRO','NMUN','NCA','geometry']]
    muni['codMun'] = muni['CLAU2']
    muni.rename({'NPRO':'provincia','NMUN':'municipio','NCA':'comunidadA'},\
                axis=1, inplace=True)
    muni.codMun = muni.codMun.astype(int)
    muni = muni.to_crs(epsg=4326)
    muni = muni.dissolve(by='CLAU2')
    
    pop = pop_ini.rename({'Código INE 2010 Municipio':'codMun','POB':'pob'},axis=1)
    pop = pop[['codMun','pob']]
    muni_pop = muni.merge(pop, on=["codMun"])
    no_pop = muni[~muni.codMun.isin(muni_pop.codMun)]
    print("Municipalties without population data: ")
    print(no_pop.municipio)
    no_pop['pob'] = 0
    muni_pop = muni_pop.append(no_pop)
    endtime = datetime.now()
    print(endtime)
    print("End create map")
    print("-----------------------------------")
    return muni_pop

def addMuniProvComA(df_ini, muni_pob):
    '''
    Asigna informacion geografica a un dataframe. Solo asigna tal informacion 
    a aquellos puntos que se encuentran dentro del poligono de algun municipio,
    el resto de puntos quedan sin informacion geografica.
    
    
    Apartado TFM: "3.1.7 Asignacion de información geográfica"
    Apartado TFM: "3.2.7 Asignacion de información geográfica"

    Parameters
    ----------
    df_ini : dataframe
        dataframe sin informacion geografica.
    muni_pob : geodataframe
        poligonos de todos los municipios de españa.

    Returns
    -------
    df_muni : geodataframe
        dataframe con informacion geografica, pero puede haber filas 
        incompletas por no estar dentro de ningun municipio.

    '''
    startTime = datetime.now()
    print(startTime)
    print("Start add Muni Prov and ComA")
    if 'site_lat' in df_ini.columns:
        geometry = [Point(xy) for xy in zip(df_ini.site_lon, df_ini.site_lat)]
    else:
        geometry = [Point(xy) for xy in zip(df_ini.lon, df_ini.lat)]
    df_muni = df_ini.copy()
    df_muni = gpd.GeoDataFrame(df_muni, crs="EPSG:4326", geometry=geometry)
    
    df_muni['municipio'] = "_"
    df_muni['provincia'] = "_"
    df_muni['comunidadA'] = "_"
    df_muni['codMun'] = 0
    df_muni['pob'] = 0
    i = 1
    for index, m in muni_pob.iterrows():
        mask = df_muni.within(m.geometry)
        if mask.value_counts().size > 1:
            codMun = m.codMun
            df_muni.loc[mask, 'pob'] = m.pob
            df_muni.loc[mask, 'municipio'] = m.municipio
            df_muni.loc[mask, 'codMun'] = int(codMun)
            df_muni.loc[mask, 'provincia'] = m.provincia
            df_muni.loc[mask, 'comunidadA'] = m.comunidadA
        print("    "+str(i)+" municipalities completed")
        i = i + 1
    endTime = datetime.now()
    print("Duration of method: "+str(endTime-startTime))
    print("End add Muni Prov and ComA")
    return df_muni

def tag_comA(gdf_ini, muni_pob):
    '''
    Asigna a cada punto de un geodataframe la comunidad autonoma más cercana 
    a ese punto.
    
    Apartado TFM: "3.1.7 Asignacion de información geográfica"
    Apartado TFM: "3.2.7 Asignacion de información geográfica"

    Parameters
    ----------
    gdf_ini : geodataframe
        dataframe con informacion geografica incompleta en algunas filas.
    muni_pob : geodataframe
        poligonos de todos los municipios de españa.

    Returns
    -------
    gdf : geodataframe
        dataframe con informacion geografica completa en la columna de 
        comunidades autonomas.

    '''
    print("Start tagging comunidadA")
    comA = muni_pob[['comunidadA','geometry']]
    comA = comA.dissolve(by='comunidadA')
    comA = comA.to_crs(epsg=3035)
    comA = comA.reset_index()
    
    gdf = gdf_ini.copy()
    gdf = gdf.to_crs(epsg=3035)
    gdf_aux = gdf.reset_index()
    gdf_1 = gdf[gdf.comunidadA == "_"]
    if gdf_1.shape[0] == 0:
        print("All elements already tagged with the comA")
        return gdf_ini
    n_CA = comA.shape[0]
    point = gdf_aux.head(n_CA).geometry

    for j in gdf_1.index:
        for i in range(0, n_CA):
            point.iloc[i] = gdf_1.loc[gdf_1.index == j].iloc[0].geometry
        dist = point.distance(comA)
        gdf.loc[gdf.index == j, 'comunidadA'] = \
            comA.iloc[dist.idxmin()].comunidadA
            
    gdf = gdf.to_crs(epsg=4326)
    print("End tagging comunidadA")
    return gdf

def tag_prov(gdf_ini, muni_pob):
    '''
    Asigna a cada punto de un geodataframe la provincia más cercana a ese punto.
    
    Apartado TFM: "3.1.7 Asignacion de información geográfica"
    Apartado TFM: "3.2.7 Asignacion de información geográfica"

    Parameters
    ----------
    gdf_ini : geodataframe
        dataframe con informacion geografica incompleta en algunas filas.
    muni_pob : geodataframe
        poligonos de todos los municipios de españa.

    Returns
    -------
    gdf : geodataframe
        dataframe con informacion geografica completa en la columna de 
        provincias.

    '''
    print("Start tagging provincia")
    prov = muni_pob[['provincia','geometry']]
    prov = prov.dissolve(by='provincia')
    prov = prov.to_crs(epsg=3035)
    prov = prov.reset_index()
    
    gdf = gdf_ini.copy()
    gdf = gdf.to_crs(epsg=3035)
    gdf_aux = gdf.reset_index()
    gdf_1 = gdf[gdf.provincia == "_"]
    if gdf_1.shape[0] == 0:
         print("All elements already tagged with the province")
         return gdf_ini
    n_prov = prov.shape[0]
    point = gdf_aux.head(n_prov).geometry

    for j in gdf_1.index:
        for i in range(0, n_prov):
            point.iloc[i] = gdf_1.loc[gdf_1.index == j].iloc[0].geometry
        dist = point.distance(prov)
        gdf.loc[gdf.index == j, 'provincia'] = \
            prov.iloc[dist.idxmin()].provincia
            
    gdf = gdf.to_crs(epsg=4326)
    print("End tagging provincia")
    return gdf

def distance_calc(lat1, lon1, lat2, lon2):
    '''
    Calcula la distancia en kilometros entre dos puntos dados.
    
    Apartado TFM: N/A

    Parameters
    ----------
    lat1 : float
        latitud del punto 1.
    lon1 : float
        longitud del punto 1.
    lat2 : float
        latitud del punto 2.
    lon2 : float
        longitud del punto 2.

    Returns
    -------
    distance : float
        distancia entre dos puntos.

    '''
    # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c    
    # in km
    return distance

def df_overview(df, title):
    '''
    Imprime una vision global sobre la informacion geografica de un dataframe.
    
    Apartado TFM: "3.2.8 Estimacion de la precision de los datos"

    Parameters
    ----------
    df : geodataframe
        dataframe del cual queremos tener una vision global de su informacion 
        geografica.
    title : string
        titulo que identifica al geodataframe.

    Returns
    -------
    None.

    '''
    print("------------------------------------------------")
    print("Start " +title+ " overview")
    print("---------------------Total----------------------")
    print("DF size:               " + str(df.shape[0]))
    print("No Provincia:          " + str(df[df.provincia == "_"].shape[0]))
    print("No Comunidad Autonoma: " + str(df[df.comunidadA == "_"].shape[0]))
    print("-------------------Provincias-------------------")
    print(str(df.provincia.value_counts()))
    print("--------------Comunidad Autonoma----------------")
    print(str(df.comunidadA.value_counts()))
   
    print("End overview ")
    print("-----------------------------------")