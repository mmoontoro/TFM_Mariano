# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 12:30:45 2021

@author: Mariano
"""
import requests
import json
import pandas as pd
import time
import json
import sys

# FUNCTIONS
def get_tag(layer, tag, key):
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