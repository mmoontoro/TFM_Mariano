# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:56:09 2021

@author: Mariano
"""
import pandas as pd
import plotly.express as px
import plotly.offline as off

def plot(df, column_color, title):
    '''
    Muestra en un mapa los datos de un dataframe, utilizando las columnas 
    site_lat y site_lon para definir la posicion geografica de cada punto en 
    el mapa.
    
    Apartado TFM: "3.2.9 Resumen de Infraestructura de red movil"

    Parameters
    ----------
    df : dataframe
        datos a imprimir en el mapa.
    column_color : string
        columna para agregar los datos en la representacion grafica.
    title : TYPE
        titulo que identifica al plot.

    Returns
    -------
    None.

    '''
    print("----------------------------")
    print("Start Plot " + title)
    print("Total: "+str(df.shape[0]))

    #To use a column as text, convert the column to str
    #df.samples = df.samples.astype(str)
    fig = px.scatter_mapbox(df,lat="site_lat",lon="site_lon",\
                            hover_name="enbid",\
                            color=df[column_color].astype(object),\
                            labels={'color': column_color})
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.6,
                       mapbox_center={"lat": 39.9843, "lon": -8 }) 
    fig.update_layout(margin={"r":0.1,"t":30,"l":0.1,"b":0.1   })
    fig.update_layout(title={'text': 'Points: ' + str(df.shape[0]),
                             'x':0.5,'y':0.99,'xanchor':'center',\
                                 'yanchor':'top'})
    off.plot(fig, auto_open = True, filename=title + '.html')
    print("End Plot " + title)

def plot_clustering(df_cells, df_sites, column_color, title):
    '''
    Muestra en un mapa las celdas de una estacion y el centro de dicha 
    estacion, que es la media de las posiciones de sus celdas.
    
    Apartado TFM: "3.2.5 Mejora de posicion de las estaciones"

    Parameters
    ----------
    df_cells : dataframe
        celdas de la estacion o estaciones a representar.
    df_sites : dataframe
        estacion o estaciones a representar.
    column_color : string (dataframe column)
        columna para agregar los datos en la representacion grafica..
    title : string
        titulo que identifica al plot.

    Returns
    -------
    None.

    '''
    print("----------------------------")
    print("Start Plot " + title)
    print("Total: "+str(df_cells.shape[0]))
    
    dfc = df_cells[['net','enbid','area','cell','lat','lon',\
                    'errorKm']]
    dfc['type'] = 'cell'
    dfc['errorKm'] = dfc['errorKm'].round(1).astype(str)
    dfc['net-enbid'] = dfc.net.astype(str)+' - '+dfc.enbid.astype(str) 
    dfc['hover'] = dfc.net.astype(str)+' - '+dfc.enbid.astype(str) 
      
    dfs = df_sites[['net','enbid','area','n_cells',\
                    'site_lat','site_lon','errorKm_mean']]
    dfs = dfs.rename(columns={"site_lat": "lat", "site_lon": "lon",\
                        "n_cells": "cell", "errorKm_mean": "errorKm"})
    dfs['net-enbid'] = dfs.net.astype(str)+' - '+dfs.enbid.astype(str) 
    dfs['hover'] = dfs['net-enbid'] + ':  Center of ' + \
                        dfs['cell'].round(1).astype(str)+ ' cells'
    dfs['errorKm'] = dfs['errorKm'].round(1).astype(str) + ' as mean' 
    dfs['type'] = 'site'

    df = dfs.append(dfc, ignore_index=True)
    
    #To use a column as text, convert the column to str
    df.cell = df.cell.astype(str)
    df.errorKm = df.errorKm.astype(str)
    
    
    fig = px.scatter_mapbox(df,lat="lat",lon="lon",\
                            hover_name="hover", text="errorKm",\
                            color=df[column_color].astype(object),\
                            labels={'color': column_color})
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.6,
                       mapbox_center={"lat": 39.9843, "lon": -8 }) 
    fig.update_layout(margin={"r":0.1,"t":30,"l":0.1,"b":0.1   })
    fig.update_layout(title={'text': 'Points: ' + str(df.shape[0]),
                             'x':0.5,'y':0.99,'xanchor':'center',\
                                 'yanchor':'top'})
    off.plot(fig, auto_open = True, filename=title + '.html')
    print("End Plot " + title)
    
def plot_final(df, title):
    '''
    Representa en un mismo mapa las estaciones y los nodos de los sectores 
    economicos. Para que esto sea asi, el dataframe de entrada debe estar 
    preparado para esto.
    
    Apartado TFM: "3.2.9 Resumen de la infraestructura de red movil"
    Apartado TFM: "3.1 Sectores priorizados por el Plan España Digital 2025"

    Parameters
    ----------
    df : dataframe
        dataframe de estaciones y nodos de los sectores economicos a mezclar,
        se trata de un dataframe especialmente preparado para la representacion
        grafica en un mapa ya que solo contiene la informacion que va a ser 
        representada.
    title : string
        titulo que identifica al plot.

    Returns
    -------
    None.

    '''
    print("Start " + title)
    print("    "+str(df.shape[0])+" nodes to plot")
    #To use a column as text, convert the column to str
    df.hover = df.hover.astype(str)
    df.name = df.name.astype(str)
    fig = px.scatter_mapbox(df,lat="lat",lon="lon",text="name",\
                            hover_name="hover",color=df['layer'].astype(object),\
                            labels={'color':'layer'})
    
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.6,
                       mapbox_center={"lat": 39.9843, "lon": -8 }) 
    fig.update_layout(margin={"r":0.1,"t":30,"l":0.1,"b":0.1   })
    fig.update_layout(title={'text': ' Points: ' + str(df.shape[0]),
                             'x':0.5,'y':0.99,'xanchor':'center','yanchor':'top'})
    
    off.plot(fig, auto_open = True, filename=title+'.html')
    print("End ")