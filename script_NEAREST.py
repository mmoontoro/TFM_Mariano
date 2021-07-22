# -*- coding: utf-8 -*-
"""
Created on Mon May 24 18:58:26 2021

@author: Mariano Montoro Mendoza

Script dedicado a la ejecucion de la caracterizacion de la conectividad 
movil por sector economico. Para la ejecucion de la metodología se utilizan
los datos de los sectores economicos y de la infraestructura de red movil, que 
han sido obtenidos en otros scripts.

Lo que se ejecuta en este script esta descrito en el apartado 
"3.3 Caracterizacion de la conectividad movil por sector economico" 
del documento de mi Trabajo Fin de Master (TFM).

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
from my_functions import osm, geo, dis
import geopandas as gpd

#%% 3.1 y 3.2 - Mapa con todos los sectores economicos y todas las estaciones
df_tourism = pd.read_csv("output/tourism_full.csv")
df_health = pd.read_csv("output/health_full.csv")
df_agrifood = pd.read_csv("output/agrifood_full.csv")
df_commerce = pd.read_csv("output/commerce_full.csv")
df_mobility = pd.read_csv("output/mobility_full.csv")
df_sites = pd.read_csv("output/SITES_CAPACITY.csv")

df_sites_adjusted = osm.adjust_sites_df_net(df_sites)
list_plot = [df_health, df_tourism, df_agrifood, df_commerce, df_mobility]

df = df_sites_adjusted.append(list_plot, ignore_index=True)
dis.plot_final(df, "Full")

#%% 3.3.1 - Cargamos los dataframes para la caracterizacion de la conectividad
# Dataframes incompletos para agilizar la caracterizacion
df_sites = gpd.read_file("output/SITES_CAPACITY.shp")

df_agrifood = gpd.read_file("output/agrifood.shp")
df_mobility = gpd.read_file("output/mobility.shp")

#%% 3.3.2 - Caracterizacion de la conectividad, sector Agroalimentario
# Dataframes incompletos para agilizar la caracterizacion
df_agrifood_nearest = geo.nearest_total(df_agrifood, df_sites)
df_agrifood_nearest.to_file('output/agrifood_nearest.shp', index = False)

#%% 3.3.2 - Caracterizacion de la conectividad, sector Movilidad
# Dataframes incompletos para agilizar la caracterizacion
df_mobility_nearest = geo.nearest_total(df_mobility, df_sites)
df_mobility_nearest.to_file('output/mobility_nearest.shp', index = False)

#%% 3.3.2 - Comprobamos las distancias de la caracterizacion en un mapa
df_mobility_nearest = gpd.read_file("output/mobility_nearest.shp")
df_agrifood_nearest = gpd.read_file("output/agrifood_nearest.shp")

for index, row in df_mobility_nearest.iterrows():
    df_mobility_nearest.loc[df_mobility_nearest.index == index, 'hover'] = \
        str(row.nst_site) + " - " + str(row.nst_800) + " - " + \
        str(row.nst_1800) + " - " + str(row.nst_2100) + " - " + \
        str(row.nst_2600) + " - " + str(row.nst_900)
for index, row in df_agrifood_nearest.iterrows():
    df_agrifood_nearest.loc[df_agrifood_nearest.index == index, 'hover'] = \
        str(row.nst_site) + " - " + str(row.nst_800) + " - " + \
        str(row.nst_1800) + " - " + str(row.nst_2100) + " - " + \
        str(row.nst_2600) + " - " + str(row.nst_900)
 
list_plot = [df_agrifood_nearest, df_mobility_nearest]                 
df_plot = df_sites.append(list_plot, ignore_index=True)
dis.plot_final(df_plot, "Test")

#%% 3.3.1 - Cargamos los dataframes para la caracterizacion de la conectividad
# Dataframes completos
df_tourism = gpd.read_file("output/tourism_full.shp")
df_health = gpd.read_file("output/health_full.shp")
df_commerce = gpd.read_file("output/commerce_full.shp")
#df_agrifood = gpd.read_file("output/agrifood_full.shp")
#df_mobility = gpd.read_file("output/mobility_full.shp")
df_sites = gpd.read_file("output/SITES_CAPACITY.shp")

#%% 3.3.2 - Caracterizacion de la conectividad, sector Turismo
# Dataframes completos
df_t = df_tourism[df_tourism.pob > 0]
df_t_nearest = geo.nearest_total(df_t, df_sites)
df_t_nearest.to_file('output/tourism_full_nearest.shp', index = False)

#%% 3.3.2 - Caracterizacion de la conectividad, sector Salud
# Dataframes completos
df_health_nearest = geo.nearest_total(df_health, df_sites)
df_health_nearest.to_file('output/health_full_nearest.shp', index = False)

#%% 3.3.2 - Caracterizacion de la conectividad, sector Comercio
# Dataframes completos
df_commerce_nearest = geo.nearest_total(df_commerce, df_sites)
df_commerce_nearest.to_file('output/commerce_full_nearest.shp', index = False)

#%% 3.3.2 - Caracterizacion de la conectividad, sector Agroalimentario
# Dataframes completos. Esta seccion no se ejecuta porque tarda demasiado
df_agrifood_nearest = geo.nearest_total(df_agrifood, df_sites)
df_agrifood_nearest.to_file('output/agrifood_full_nearest.shp', index = False)

#%% 3.3.2 - Caracterizacion de la conectividad, sector Movilidad
# Dataframes completos. Esta seccion no se ejecuta porque tarda demasiado
df_mobility_nearest = geo.nearest_total(df_mobility, df_sites)
df_mobility_nearest.to_file('output/mobility_full_nearest.shp', index = False)
