# -*- coding: utf-8 -*-
"""
Created on Tue May 11 12:21:48 2021

@author: Mariano
"""

import os
tfm_dir = "D://Dropbox/Escritorio/TFM/Workspace_spyder/" 
os.chdir(tfm_dir)
import pandas as pd
from my_functions import osm, geo, dis
import geopandas as gpd

import numpy as np
import math
import matplotlib.pyplot as plt

#%%
cols = ["nst_site", "nst_low", "nst_medium", "nst_high"]
list_colors_cols = ['black', 'red', 'lime', 'blue']
    
#%%
cols = ["nst_site", "nst_800", "nst_1800", "nst_2100", "nst_2600"]
list_colors_cols = ['black', 'red', 'green', 'lightgreen', 'aqua']

#%%

dict_cities1 = {\
'Valencia': 7e5, 'Sevilla': 750e3, 'Palma': 4e5,\
'Valladolid': 3e5, 'Santander': 182e3, 'Las Palmas': 370e3,\
'Bilbao': 354e3, 'Gijón': 300e3, 'Barcelona': 2e6,\
'Murcia': 550e3, 'Pamplona': 198e3, 'Madrid': 3e6,\
'Zaragoza': 650e3, 'Vigo': 350e3, \
'Badajoz': 148e3, 'Albacete': 150e3, 'Logroño': 152e3}

dict_cities2 = {\
'Alicante': 334e3, 'Málaga': 500e3, 'Calvià': 51e3,\
'Burgos': 170e3,'Torrelavega': 55e3, 'Tenerife': 222e3,\
'Vitoria': 235e3, 'Oviedo': 200e3, 'Hospitalet': 257e3,\
'Cartagena': 211e3, 'Tudela': 34e3, 'Alcalá de Henares': 204e3,\
'Huesca': 52e3, 'A Coruña': 220e3,\
'Cáceres': 70e3, 'Talavera': 70e3,'Calahorra': 24e3}

list_colors_com = ['green', 'lightgreen', 'greenyellow', 'yellow',\
               'gold', 'darkorange', 'bisque','turquoise','teal', 'blue',\
               'indigo','magenta', 'deeppink', 'sienna', 'red', 'brown',\
               'silver', 'grey','black']
    
list_sectors = ["Comercio", "Salud", "Movilidad", "Turismo", "Agroalimentario"]
dict_colors_sec = {"Comercio": 'y', "Salud": 'g', "Movilidad": 'grey', \
                "Turismo": 'b', "Agroalimentario": 'r'}
    
df_h = gpd.read_file("output/health_full_nearest.shp")
df_t = gpd.read_file("output/tourism_full_nearest.shp")
df_a = gpd.read_file("output/agrifood_nearest.shp")
df_c = gpd.read_file("output/commerce_full_nearest.shp")
df_m = gpd.read_file("output/mobility_nearest.shp")
dict_sectors = {"Comercio": df_c, "Salud": df_h, "Movilidad": df_m, \
                "Turismo": df_t, "Agroalimentario": df_a}
list_df = [df_c, df_h, df_m, df_t, df_a]

df_t = gpd.read_file("output/tourism_full_nearest.shp")
for col in cols:
    df_t[col] = df_t[col] * 1000
df_t = df_t[df_t.pob > 0]

#%% Grafos 1


#%% 1.1 Turismo POR COLUMNA (1 figuras)
plt.close('all')

c = 0
for col in cols:
    df_t.plot(kind='scatter',x=col,y='pob',color=list_colors_cols[c], s=7)
    
    plt.grid()
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Metros", size=15)
    plt.ylabel("Habitantes del Municipio", size=15)
    plt.title("Turismo: " + col, size=17)
    
    plt.annotate("2", (2, 15))
    plt.annotate("5", (5, 15))
    plt.annotate("20", (19, 15))
    plt.annotate("50", (48, 15))
    plt.annotate("200", (190, 15))
    plt.annotate("500", (460, 15))
    plt.annotate("2 k", (1800, 15))
    plt.annotate("5 k", (4500, 15))
    plt.annotate("20 k", (18000, 15))
    plt.annotate("50 k", (45000, 15))
    plt.annotate("Madrid", (2, 3145844))
    plt.annotate("Barcelona", (1.5, 1511437))
    plt.xlim(1, 200000)
    plt.ylim(10, 6000000)
    c= c +1
    
plt.figure(0)

for i in range(1, len(cols)):
    plt.scatter(df_t[cols[i]], df_t['pob'], \
                color=list_colors_cols[i], label = cols[i], s=9) 
plt.grid()
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Metros", size=15)
plt.ylabel("Habitantes del Municipio", size=15)
plt.title("Turismo", size = 17)

plt.annotate("2", (2, 15))
plt.annotate("5", (5, 15))
plt.annotate("20", (19, 15))
plt.annotate("50", (48, 15))
plt.annotate("200", (190, 15))
plt.annotate("500", (460, 15))
plt.annotate("2 k", (1800, 15))
plt.annotate("5 k", (4500, 15))
plt.annotate("20 k", (18000, 15))
plt.annotate("50 k", (45000, 15))
plt.annotate("Madrid", (2, 3145844))
plt.annotate("Barcelona", (1.5, 1511437))
plt.xlim(1, 200000)
plt.ylim(10, 6000000)
plt.legend(fontsize = 15)

#%% 1.2. Turismo POR COM AUT (n_cols figuras)
plt.close('all')

list_com = []
for com in df_t.comunidadA.unique():
    list_com.append(com)

for n_fig in range(1, len(cols)):
    plt.figure(n_fig)
    for i in range(len(list_com)):
        df = df_t.loc[df_t['comunidadA'] == list_com[i]]
        plt.scatter(df[cols[n_fig]], df['pob'], \
                    color=list_colors_com[i], label = list_com[i], s=7)
        
    plt.grid()
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Metros", size=15)
    plt.ylabel("Habitantes del Municipio", size=15)
    plt.title("Turismo: " + cols[n_fig], size = 17)
    
    plt.annotate("2", (2, 15))
    plt.annotate("5", (5, 15))
    plt.annotate("20", (19, 15))
    plt.annotate("50", (48, 15))
    plt.annotate("200", (190, 15))
    plt.annotate("500", (460, 15))
    plt.annotate("2 k", (1800, 15))
    plt.annotate("5 k", (4500, 15))
    plt.annotate("20 k", (18000, 15))
    plt.annotate("50 k", (45000, 15))
    plt.annotate("Madrid", (2, 3145844))
    plt.annotate("Barcelona", (1.7, 1511437))
    plt.xlim(1, 200000)
    plt.ylim(10, 6000000)
    plt.legend(fontsize = 15)
    
#%% 1.3. Turismo POR COLUMNA
# PRESENTADO POR COM AUT (17 figuras)
plt.close('all')

city1_iter = iter(dict_cities1.keys())
pop1_iter = iter(dict_cities1.values())
city2_iter = iter(dict_cities2.keys())
pop2_iter = iter(dict_cities2.values())

list_com = []
for com in df_t.comunidadA.unique():
    if (com != "Ceuta") and (com != "Melilla"):
        list_com.append(com)

for i in range(len(list_com)):
    plt.figure(i)
    df = df_t.loc[df_t['comunidadA'] == list_com[i]]
    for j in range(1, len(cols)):
        plt.scatter(df[cols[j]], df['pob'], \
                    color=list_colors_cols[j], label = cols[j])
            
    plt.grid()
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Metros", size=15)
    plt.ylabel("Habitantes del Municipio", size=15)
    plt.title("Turismo: " + list_com[i], size = 17)
    
    plt.annotate("2", (2, 15))
    plt.annotate("5", (5, 15))
    plt.annotate("20", (19, 15))
    plt.annotate("50", (48, 15))
    plt.annotate("200", (190, 15))
    plt.annotate("500", (460, 15))
    plt.annotate("2 k", (1800, 15))
    plt.annotate("5 k", (4500, 15))
    plt.annotate("20 k", (18000, 15))
    plt.annotate("50 k", (45000, 15))
    plt.annotate(next(city1_iter), (2, next(pop1_iter)), size = 15)
    plt.annotate(next(city2_iter), (2, next(pop2_iter)), size = 15)
    plt.xlim(1, 200000)
    plt.ylim(10, 6000000)
    plt.legend(fontsize = 15)


#%% Grafos 2


#%% 2.1. Acumulativas POR SECTOR
# PRESENTADO POR COLUMNAS (n_cols figuras)
plt.close('all')
x_axis = [0.01,0.015,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,\
          0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,\
          1,1.5,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,\
          20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
y_axis = []
x_axis_m = [element * 1000 for element in x_axis]

for n_fig in range(len(cols)):
    for sector in dict_sectors:
        df = dict_sectors[sector]
        y_axis = []
        for x in x_axis:
            y = df[df[cols[n_fig]] < x][cols[n_fig]].shape[0]
            y = y / df.shape[0] * 100
            y_axis.append(y)
        plt.figure(n_fig)
        plt.plot(x_axis_m, y_axis, color=dict_colors_sec[sector], label = sector)
    plt.xscale("log")
    plt.legend(fontsize = 15)
    plt.xlabel("Metros", size=15)
    plt.ylabel("Porcentaje de nodos del sector económico", size=15)
    plt.title(cols[n_fig][4:], size = 17)
    plt.xlim(50, 50000)
    plt.grid()
    plt.annotate("200 m", (190, -2))
    plt.annotate("500 m", (460, -2))
    plt.annotate("2.000 m", (1900, -2))
    plt.annotate("5.000 m", (4600, -2))
    
#%% 2.2. Acumulativas POR SECTOR
# PRESENTADO POR COLUMNA y POR COM AUT (n_cols x 19 figuras)
for i in range(len(list_df)):
    df = list_df[i]
    df = df[df.groupby('comunidadA')\
            ['comunidadA'].transform('count').ge(50)]
    list_df[i] = df
   
list_com = []
for com in df_h.comunidadA.unique():
    list_com.append(com)

plt.close('all')
x_axis = [0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50]
x_axis_m = [element * 1000 for element in x_axis]
y_axis = []

n_fig = 0
for col in cols:
    for c in range(len(list_com)):
        plt.figure(n_fig)
        dict_temp = dict_sectors.copy()
        s = 0
        for sector in dict_temp:
            dict_temp[sector] = list_df[s].loc[list_df[s]['comunidadA']\
                                                    == list_com[c]]
            s = s + 1
            df = dict_temp[sector]
            if df.shape[0] != 0:
                y_axis = []
                for x in x_axis:
                    y = df[df[col] < x][col].shape[0]
                    y = y / df.shape[0] * 100
                    y_axis.append(y)
                plt.plot(x_axis_m, y_axis, color=dict_colors_sec[sector], label = sector)
        plt.xscale("log")
        plt.legend(fontsize = 15)
        plt.xlabel("Metros", size = 15)
        plt.ylabel("Porcentaje de nodos del sector económico", size = 15)
        plt.title(list_com[c] + ": " + col, size = 17)
        plt.xlim(50, 50000)
        plt.grid()
        plt.annotate("200 m", (190, -2))
        plt.annotate("500 m", (460, -2))
        plt.annotate("2.000 m", (1900, -2))
        plt.annotate("5.000 m", (4600, -2))
        n_fig = n_fig + 1
    
#%% 2.3. Acumulativas POR COM AUT
# PRESENTADO POR SECTOR y COLUMNA (n_cols x n_sectors figuras)
plt.close('all')
x_axis = [0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50]
x_axis = [0.01,0.015,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,\
          0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,\
          1,1.5,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,\
          20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
x_axis_m = [element * 1000 for element in x_axis]
y_axis = []

for i in range(len(list_df)):
    df = list_df[i]
    df = df[df.groupby('comunidadA')\
            ['comunidadA'].transform('count').ge(100)]
    list_df[i] = df
   
list_com = []
for com in df_h.comunidadA.unique():
    list_com.append(com)

n_fig = 0
for col in cols:
    for s in range(len(list_df)):
        list_com_ord = []
        list_com_used = []
        y_axis = []
        idx = []
        for i in range(len(list_com)):
            df = list_df[s].loc[list_df[s]['comunidadA']\
                                        == list_com[i]]
            if df.shape[0] != 0:         
                y = df[df[col] < 1][col].shape[0]
                y = y / df.shape[0] * 100
                y_axis.append(y)
                list_com_used.append(list_com[i])
        y_axis = np.array(y_axis)
        idx = np.argsort(-y_axis)
        
        for i in idx:
            list_com_ord.append(list_com_used[i])
    
        plt.figure(n_fig)
        for i in range(len(list_com_ord)):
            df = list_df[s].loc[list_df[s]['comunidadA']\
                                        == list_com_ord[i]]
            y_axis = []
            for x in x_axis:
                y = df[df[col] < x][col].shape[0]
                y = y / df.shape[0] * 100
                y_axis.append(y)
            plt.plot(x_axis_m, y_axis, color=list_colors_com[i], label = list_com_ord[i])
    
        plt.xscale("log")
        plt.legend(fontsize = 15)
        plt.xlabel("Metros", size = 15)
        plt.ylabel("Porcentaje de nodos del sector económico", size = 15)
        plt.title(list_sectors[s] + ": " + str(col), size = 17)
        plt.xlim(50, 50000)
        plt.grid()
        plt.annotate("200 m", (190, -2))
        plt.annotate("500 m", (460, -2))
        plt.annotate("2.000 m", (1900, -2))
        plt.annotate("5.000 m", (4600, -2))
        n_fig = n_fig + 1
    
#%% 2.4. Acumulativas POR COLUMNA
# PRESENTADO POR SECTOR (n_sectors figuras)
plt.close('all')
x_axis = [0.01,0.015,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,\
          0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,\
          1,1.5,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,\
          20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
y_axis = []
x_axis_m = [element * 1000 for element in x_axis]

n_fig = 0
for sector in dict_sectors:
    df = dict_sectors[sector]
    c = 0
    for col in cols:
        y_axis = []
        for x in x_axis:
            y = df[df[col] < x][col].shape[0]
            y = y / df.shape[0] * 100
            y_axis.append(y)
        plt.figure(n_fig)
        plt.plot(x_axis_m, y_axis, \
                 color=list_colors_cols[c], label = col)
        c = c + 1    
    
    plt.xscale("log")
    plt.legend(fontsize = 15)
    plt.xlabel("Metros", size=15)
    plt.ylabel("Porcentaje de nodos del sector económico", size=15)
    plt.title(sector, size = 17)
    plt.xlim(50, 50000)
    plt.grid()
    plt.annotate("200 m", (190, -2))
    plt.annotate("500 m", (460, -2))
    plt.annotate("2.000 m", (1900, -2))
    plt.annotate("5.000 m", (4600, -2))
    n_fig = n_fig + 1

#%% Stats




#%% Extraer histograma por rangos
bins = [0,0.5,2,5,11,35,165]
df_stats = pd.DataFrame(columns = bins[1:])

row = 0
for df in list_df:
    count, div = np.histogram(df.nst_site, bins = bins)
    perc = []
    for num in count/df.shape[0]*100:
        perc.append(round(num, 2))
    df_stats.loc[row] = perc
    row = row + 1
print(df_stats)
df_stats.to_excel('output/hist_site.xlsx', index = False)

#%% Extraer percentiles
perc = [.3, .4, .5, .6,.65,.7,.75,.8,.85,.9,.95,.97,.98, 1]
cols = [element * 100 for element in perc]
df_stats = pd.DataFrame(columns = cols)

row = 0
for df in list_df:
    list_perc_sector = []
    for p in perc:
        list_perc_sector.append(df.nst_2600.quantile(p))
    df_stats.loc[row] = list_perc_sector
    row = row + 1
print(df_stats)
df_stats.to_excel('output/perct_2600.xlsx', index = False)

