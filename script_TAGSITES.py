# -*- coding: utf-8 -*-
"""
Created on Wed May 26 17:24:40 2021

@author: Mariano Montoro Mendoza

Script dedicado a asignar la informacion de capacidad a cada estacion.

Lo que se ejecuta en este script esta descrito en el apartado 
"3.2.6 Calculo de la capacidad de las estaciones" del documento de mi 
Trabajo Fin de Master (TFM). 

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
from my_functions import sit
from datetime import datetime

#%% 3.2.6 - Añadimos informacion de la capacidad en cada estación

df_sites = pd.read_csv("output/SITES_BAND.csv")

sit.df_overview(df_sites)
print("")

startTime = datetime.now()
print(startTime)

df_sites_capacity = sit.capacity_calc(df_sites)

endTime = datetime.now()
print(endTime)

df_sites_capacity.to_csv('output/SITES_CAPACITY.csv', index = False)