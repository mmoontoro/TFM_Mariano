# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 13:56:49 2021

@author: Mariano Montoro Mendoza

Script dedicado a asignar la informacion geografica a cada estacion. Esta 
información geografica consiste en el municipio donde se encuentra la estacion, 
la poblacion de ese municipio, la provincia y la comunidad autonoma. La fuente 
de esta informacion es el INE.

Lo que se ejecuta en este script esta descrito en el apartado 
"3.2.7 Asignacion de informacion geografica" y "3.2.8 Estimacion de la 
precision de los datos" del documento de mi Trabajo Fin de Master (TFM). 

Titulo: "Caracterizacion sectorial de la conectividad movil 
en España mediante datos abiertos".
Autor: Mariano Montoro Mendoza.
Tutora: Zoraida Frías Barroso.
Cotutor: Luis Mendo Tomás.
Fecha de lectura: 14 de julio de 2021.

"""

import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)
import pandas as pd
from my_functions import geo, dis
import geopandas as gpd
import plotly.express as px
import plotly.offline as off

#%% 3.2.7 - Creacion de una rejilla de municipios desde los datos Oficiales
# Tiempo estimado de ejecucion: 30 s

muni_ini = gpd.read_file(tfm_dir + \
            "seccionado_2020/SECC_CE_20200101.shp")
pop_ini = pd.read_excel("input/catastro_prov.xls")

muni_pop = geo.create_map_pop(muni_ini, pop_ini)

muni_pop.to_file("output/REJILLA.shp")

#%% 3.2.7 - Primera asignacion de informacion geografica a las estaciones
# Tiempo estimado de ejecucion: 1 h

muni_pob = gpd.read_file("output/REJILLA.shp")

df_sites_1 = pd.read_csv('output/SITES_BAND.csv')
df_sites_2 = geo.addMuniProvComA(df_sites_1, muni_pob)
df_sites_2.to_file('output/SITES_MUN_1.shp', index = False)

#%% 3.2.7 - Resultados de la primera asignacion

gdf_1 = gpd.read_file('output/SITES_MUN_1.shp')
gdf_1 = gdf_1[['codMun','pob','provincia','comunidadA','geometry','municipio']]
gdf_1 = gdf_1[gdf_1.comunidadA == "_"]
gdf_1['index'] = gdf_1.index

muni_pob = gpd.read_file("output/REJILLA.shp")
gdf_2 = muni_pob[(muni_pob.comunidadA == "Extremadura")|
                 (muni_pob.comunidadA == "Comunidad de Madrid")|
                 (muni_pob.comunidadA == "Castilla-La Mancha")]

ax = muni_pob.plot(column = "comunidadA", k = 9,\
                cmap = "Dark2", legend = True,\
                alpha = 0.65, linewidth = 0.9, figsize = (60, 40))
gdf_1.plot(ax=ax, marker='o', color='black', markersize=10)

#%% 3.2.7 - Segunda asignacion de informacion geografica a las estaciones
# Tiempo estimado de ejecucion: 6 min
muni_pob = gpd.read_file("output/REJILLA.shp")
df_sites_2 = gpd.read_file('output/SITES_MUN_1.shp')
df_sites_3 = geo.tag_comA(df_sites_2, muni_pob)
df_sites_4 = geo.tag_prov(df_sites_3, muni_pob)
df_sites_4.to_file('output/SITES_MUN_2.shp', index = False)

#%% 3.2.7 - Resultados de la segunda asignacion

gdf_1 = gpd.read_file('output/SITES_MUN_2.shp')
gdf_1 = gdf_1[['codMun','pob','provincia','comunidadA','geometry','municipio']]

gdf_1['index'] = gdf_1.index

muni_pob = gpd.read_file("output/REJILLA.shp")

ax = muni_pob.plot(column = "comunidadA", k = 9,\
                cmap = "Dark2", legend = True,\
                alpha = 0.65, linewidth = 0.9, figsize = (60, 40))
gdf_1.plot(ax=ax, marker='o', color='black', markersize=10)


#%% 3.2.7 - Resultados de la informacion geografica

df_sites_2 = gpd.read_file('output/SITES_MUN_1.shp')
#plot_total(df, color, title)
dis.plot(df_sites_2, 'comunidadA', "Sites incomplete")

df_sites_4 = gpd.read_file('output/SITES_MUN_2.shp')
#plot_total(df, color, title)
dis.plot(df_sites_4, 'comunidadA', "Sites complete")

#%% 3.2.8 - Overview de los datos por comunidad autonoma y provincia

df_sites_2 = gpd.read_file('output/SITES_MUN_1.shp')

df_sites_4 = gpd.read_file('output/SITES_MUN_2.shp')

geo.df_overview(df_sites_2, "Primera Asignacion Sites")

geo.df_overview(df_sites_4, "Segunda Asignacion Sites")

#%% 3.2.7 - Asignacion de informacion geografica a las estaciones (completo)

muni_pob = gpd.read_file("output/REJILLA.shp")
df_sites_1 = pd.read_csv('output/SITES_CAPACITY.csv')
df_sites_2 = geo.addMuniProvComA(df_sites_1, muni_pob)
df_sites_3 = geo.tag_comA(df_sites_2, muni_pob)
df_sites_4 = geo.tag_prov(df_sites_3, muni_pob)
df_sites_4.to_file('output/SITES_CAPACITY.shp', index = False)

#%% 2.10 - Mapa de provincias
muni_pob = gpd.read_file("output/REJILLA.shp")

comA = muni_pob[['provincia','geometry']]
comA = comA.dissolve(by='provincia')
comA = comA.reset_index()
comA.plot(column = "provincia", k = 9,\
                cmap = "Dark2", legend = False,\
                alpha = 0.65, linewidth = 0.9, figsize = (60, 40))

#%% 2.10 - Mapa de comunidades autonomas

muni_pob = gpd.read_file("output/REJILLA.shp")

comA = muni_pob[['comunidadA','geometry']]
comA = comA.dissolve(by='comunidadA')
comA = comA.reset_index()
comA.plot(column = "comunidadA", k = 9,\
                cmap = "Dark2", legend = True,\
                alpha = 0.65, linewidth = 0.9, figsize = (60, 40))
    
#%% Ejemplo de un plot con Choropleth
muni_pob = gpd.read_file("output/REJILLA.shp")
gdf_2 = muni_pob[(muni_pob.comunidadA == "Extremadura")|
                 (muni_pob.comunidadA == "Comunidad de Madrid")|
                 (muni_pob.comunidadA == "Castilla-La Mancha")]

gdf = gdf_2

fig = px.choropleth_mapbox(gdf, geojson=gdf.geometry,
                   locations=gdf.index, color="comunidadA")
fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3.6,
                   mapbox_center={"lat": 39.9843, "lon": -8 }) 
fig.update_layout(margin={"r":0.1,"t":30,"l":0.1,"b":0.1   })
fig.update_layout(title={'text': 'Geometries: ' + str(gdf.shape[0]),
                         'x':0.5,'y':0.99,'xanchor':'center',\
                             'yanchor':'top'})
off.plot(fig, auto_open = True, filename='polygons.html')

