# -*- coding: utf-8 -*-
"""
Created on Mon May 24 18:58:26 2021

@author: Mariano
"""

import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)
import pandas as pd
from my_functions import osm, geo, dis
import geopandas as gpd


#%% Plot muestra
df_tourism = pd.read_csv("output/tourism.csv")
df_health = pd.read_csv("output/health.csv")
df_agrifood = pd.read_csv("output/agrifood.csv")
df_commerce = pd.read_csv("output/commerce.csv")
df_mobility = pd.read_csv("output/mobility.csv")
df_sites = pd.read_csv("output/SITES_CAPACITY.csv")

df_sites_adjusted = osm.adjust_sites_df_cap(df_sites)
list_plot = [df_health, df_tourism, df_agrifood, df_commerce, df_mobility]

df = df_sites_adjusted.append(list_plot, ignore_index=True)
dis.plot_final(df, "Muestra")

#%% Plot full
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

#%% Load all shapefiles for nearest
df_sites = gpd.read_file("output/SITES_CAPACITY.shp")

df_health = gpd.read_file("output/health.shp")
df_tourism = gpd.read_file("output/tourism.shp")
df_agrifood = gpd.read_file("output/agrifood.shp")
df_mobility = gpd.read_file("output/mobility.shp")
df_commerce = gpd.read_file("output/commerce.shp")

#%% Distance to closest site Health 
df_health_nearest = geo.nearest_total(df_health, df_sites)
df_health_nearest.to_file('output/health_nearest.shp', index = False)

#%% Distance to closest site Tourism
df_tourism_nearest = geo.nearest_total(df_tourism, df_sites)
df_tourism_nearest.to_file('output/tourism_nearest.shp', index = False)

#%% Distance to closest site Agrifood
df_agrifood_nearest = geo.nearest_total(df_agrifood, df_sites)
df_agrifood_nearest.to_file('output/agrifood_nearest.shp', index = False)

#%% Distance to closest site Commerce
df_commerce_nearest = geo.nearest_total(df_commerce, df_sites)
df_commerce_nearest.to_file('output/commerce_nearest.shp', index = False)

#%% Distance to closest site Mobility
df_mobility_nearest = geo.nearest_total(df_mobility, df_sites)
df_mobility_nearest.to_file('output/mobility_nearest.shp', index = False)

#%% Plot test
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

#%% Distance to closest site Tourism FULL
df_sites = gpd.read_file("output/SITES_CAPACITY.shp")

df_t = gpd.read_file("output/tourism_full.shp")
df_t = df_t[df_t.pob > 0]
df_t_nearest = geo.nearest_total(df_t, df_sites)
df_t_nearest.to_file('output/tourism_full_nearest.shp', index = False)

#%% Load all shapefiles for nearest FULL
df_tourism = gpd.read_file("output/tourism_full.shp")
df_health = gpd.read_file("output/health_full.shp")
df_commerce = gpd.read_file("output/commerce_full.shp")
df_agrifood = gpd.read_file("output/agrifood_full.shp")
df_mobility = gpd.read_file("output/mobility_full.shp")
df_sites = gpd.read_file("output/SITES_CAPACITY.shp")

#%% Distance to closest site Health FULL
df_health_nearest = geo.nearest_total(df_health, df_sites)
df_health_nearest.to_file('output/health_full_nearest.shp', index = False)

#%% Distance to closest site Commerce FULL
df_commerce_nearest = geo.nearest_total(df_commerce, df_sites)
df_commerce_nearest.to_file('output/commerce_full_nearest.shp', index = False)

#%% Distance to closest site Agrifood FULL
df_agrifood_nearest = geo.nearest_total(df_agrifood, df_sites)
df_agrifood_nearest.to_file('output/agrifood_full_nearest.shp', index = False)

#%% Distance to closest site Mobility FULL
df_mobility_nearest = geo.nearest_total(df_mobility, df_sites)
df_mobility_nearest.to_file('output/mobility_full_nearest.shp', index = False)
