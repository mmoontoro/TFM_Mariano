# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:28:29 2021

@author: Mariano
"""
import pandas as pd
from my_functions import geo
from collections import Counter

# FUNCTIONS
def df_overview(df_sites):
    n_800 = df_sites[df_sites.cells800 > 0].shape[0]
    n_900 = df_sites[df_sites.cells900 > 0].shape[0]
    n_1800 = df_sites[df_sites.cells1800 > 0].shape[0]
    n_2100 = df_sites[df_sites.cells2100 > 0].shape[0]
    n_2600 = df_sites[df_sites.cells2600 > 0].shape[0]
    
    n_800_1 = df_sites[df_sites.cells800 == 1].shape[0]
    n_900_1 = df_sites[df_sites.cells900 == 1].shape[0]
    n_1800_1 = df_sites[df_sites.cells1800 == 1].shape[0]
    n_2100_1 = df_sites[df_sites.cells2100 == 1].shape[0]
    n_2600_1 = df_sites[df_sites.cells2600 == 1].shape[0]
    
    n_800_2 = df_sites[df_sites.cells800 == 2].shape[0]
    n_900_2 = df_sites[df_sites.cells900 == 2].shape[0]
    n_1800_2 = df_sites[df_sites.cells1800 == 2].shape[0]
    n_2100_2 = df_sites[df_sites.cells2100 == 2].shape[0]
    n_2600_2 = df_sites[df_sites.cells2600 == 2].shape[0]
    
    n_800_3 = df_sites[df_sites.cells800 == 3].shape[0]
    n_900_3 = df_sites[df_sites.cells900 == 3].shape[0]
    n_1800_3 = df_sites[df_sites.cells1800 == 3].shape[0]
    n_2100_3 = df_sites[df_sites.cells2100 == 3].shape[0]
    n_2600_3 = df_sites[df_sites.cells2600 == 3].shape[0]
    
    n_800_4 = df_sites[df_sites.cells800 > 3].shape[0]
    n_900_4 = df_sites[df_sites.cells900 > 3].shape[0]
    n_1800_4 = df_sites[df_sites.cells1800 > 3].shape[0]
    n_2100_4 = df_sites[df_sites.cells2100 > 3].shape[0]
    n_2600_4 = df_sites[df_sites.cells2600 > 3].shape[0]   
    print("Estaciones con 800MHz")
    print(    "-1: "+str(round(n_800_1/n_800,2))+\
              " -2: "+str(round(n_800_2/n_800,2))+\
              " -3: "+str(round(n_800_3/n_800, 2))+\
              " -4: "+str(round(n_800_4/n_800, 2)))
    print("----------------------")
    print("Estaciones con 1800MHz")
    print(    "-1: "+str(round(n_1800_1/n_1800,2))+\
              " -2: "+str(round(n_1800_2/n_1800,2))+\
              " -3: "+str(round(n_1800_3/n_1800, 2))+\
              " -4: "+str(round(n_1800_4/n_1800, 2)))
    print("----------------------")
    print("Estaciones con 2100MHz")
    print(    "-1: "+str(round(n_2100_1/n_2100,2))+\
              " -2: "+str(round(n_2100_2/n_2100,2))+\
              " -3: "+str(round(n_2100_3/n_2100, 2))+\
              " -4: "+str(round(n_2100_4/n_2100, 2)))    
    print("----------------------")
    print("Estaciones con 2600MHz")
    print(    "-1: "+str(round(n_2600_1/n_2600,2))+\
              " -2: "+str(round(n_2600_2/n_2600,2))+\
              " -3: "+str(round(n_2600_3/n_2600, 2))+\
              " -4: "+str(round(n_2600_4/n_2600, 2)))
    print("----------------------")
    print("Estaciones con 900MHz")
    print(    "-1: "+str(round(n_900_1/n_900,2))+\
              " -2: "+str(round(n_900_2/n_900,2))+\
              " -3: "+str(round(n_900_3/n_900, 2))+\
              " -4: "+str(round(n_900_4/n_900, 2)))
        
        
def capacity_calc(df_ini):
    print("-----------------------------------")
    print("Start Capacity Calculation")
    df_sites = df_ini.copy()
    #BW 800 900 1800 2100 2600 unkown
    bw_1 = [10, 10, 20, 15, 20, 10]
    bw_3 = [10, 10, 20, 15, 20, 10]
    bw_4 = [0,  0,  15, 15, 0,  10]
    bw_7 = [10, 15, 20, 15, 20, 10]
    df_sites['capacity'] = 0
    df_sites['cap_type'] = "_"
    
    for index, s in df_sites.iterrows():
        if s.net == 1:
            bw = bw_1
        elif s.net == 3:
            bw = bw_3
        elif s.net == 4:
            bw = bw_4
        elif s.net == 7:
            bw = bw_7
        cap = s.cells800 * bw[0] + s.cells900 * bw[1] + \
              s.cells1800 * bw[2] + s.cells2100 * bw[3] + \
              s.cells2600 * bw[4] + s.cells0 * bw[5]
        df_sites.loc[df_sites.index == index, 'capacity'] = cap
    thres_l = df_sites.capacity.quantile(1/3)
    thres_h = df_sites.capacity.quantile(2/3)
    
    for index, s in df_sites.iterrows():
        if s.capacity <= thres_l:
            df_sites.loc[df_sites.index == index, 'cap_type'] = "low"
        elif s.capacity >= thres_h:
            df_sites.loc[df_sites.index == index, 'cap_type'] = "high"
        else:
            df_sites.loc[df_sites.index == index, 'cap_type'] = "medium"

    print("End Capacity Calculation")
    print("-----------------------------------")
    return df_sites