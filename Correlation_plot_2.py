# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:26:10 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
'pijo@plan.aau.dk


"""



'''Execute the whole script to export the heatmaps for correlations as SI 1.7.

'''


#range geometry to be specified according to our final choice for the temperature module
import os

currentfolder=os.getcwd()


import csv
import numpy as np
import matplotlib as mpl


import matplotlib.pyplot as plt


import itertools
import requests 
import numpy as np
import random
import decimal
import pandas as pd

from math import*
from random import *
from itertools import *
from mpl_toolkits import mplot3d

import seaborn as sns


# Correlation 

#Granada
Granada_thermonight = pd.read_excel("results_table_df_Gra_thermo.xlsx",index_col=0)
Granada_Nothermonight = pd.read_excel("results_table_df_Gra_Nothermo.xlsx",index_col=0)

#Aalborg
Aalborg_thermonight = pd.read_excel("results_table_df_Aal_thermo.xlsx",index_col=0)
Aalborg_Nothermonight = pd.read_excel("results_table_df_Aal_Nothermo.xlsx",index_col=0)


totaltable=pd.concat([Granada_thermonight,Granada_Nothermonight,Aalborg_thermonight,Aalborg_Nothermonight],axis=0)










####Granada No thermonight
list(Granada_Nothermonight.columns)
table_for_corr_Granada_Nothermonight=Granada_Nothermonight[['hconv',
                                                            'biomassconcentration',
                                                            'tubediameter',
                                                            'gapbetweentubes',
                                                            'horizontaldistance',
                                                            'flowrate',
                                                            'Heating kWh PBR',
                                                            'Cooling kWh PBR',
                                                            'Electricity mixing kWh PBR',
                                                            'GWP100',
                                                            'WDP',
                                                            'TETPinf',
                                                            'FEP',
                                                            'Volumetric productivity kg.L-2.d-1',
                                                            'exchange area m2',
                                                            'tube length m',
                                                            'PBR volume m3']]



cor_Granada_Nothermonight=table_for_corr_Granada_Nothermonight.corr()
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(cor_Granada_Nothermonight, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap, Granada, No thermoregulation at night', fontdict={'fontsize':18}, pad=12);

plt.savefig('heatmap,Granada,No thermoregulation at night.png', dpi=500, bbox_inches='tight')
 













####Granada Thermonight
list(Granada_thermonight.columns)
table_for_corr_Granada_thermonight=Granada_thermonight[['hconv',
                                                            'biomassconcentration',
                                                            'tubediameter',
                                                            'gapbetweentubes',
                                                            'horizontaldistance',
                                                            'flowrate',
                                                            'Heating kWh PBR',
                                                            'Cooling kWh PBR',
                                                            'Electricity mixing kWh PBR',
                                                            'GWP100',
                                                            'WDP',
                                                            'TETPinf',
                                                            'FEP',
                                                            'Volumetric productivity kg.L-2.d-1',
                                                            'exchange area m2',
                                                            'tube length m',
                                                            'PBR volume m3']]



cor_Granada_thermonight=table_for_corr_Granada_thermonight.corr()
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(cor_Granada_thermonight, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap, Granada, Thermoregulation at night', fontdict={'fontsize':18}, pad=12);

plt.savefig('heatmap,Granada, Thermoregulation at night.png', dpi=300, bbox_inches='tight')
 

 

####Aalborg Thermonight
list(Granada_thermonight.columns)
table_for_corr_Aalborg_thermonight=Aalborg_thermonight[['hconv',
                                                            'biomassconcentration',
                                                            'tubediameter',
                                                            'gapbetweentubes',
                                                            'horizontaldistance',
                                                            'flowrate',
                                                            'Heating kWh PBR',
                                                            'Cooling kWh PBR',
                                                            'Electricity mixing kWh PBR',
                                                            'GWP100',
                                                            'WDP',
                                                            'TETPinf',
                                                            'FEP',
                                                            'Volumetric productivity kg.L-2.d-1',
                                                            'exchange area m2',
                                                            'tube length m',
                                                            'PBR volume m3']]




cor_Aalborg_thermonight=table_for_corr_Aalborg_thermonight.corr()
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(cor_Aalborg_thermonight, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap, Aalborg, Thermoregulation at night', fontdict={'fontsize':18}, pad=12);

plt.savefig('heatmap,Aalborg, Thermoregulation at night.png', dpi=300, bbox_inches='tight')
 


####Aalborg NoThermonight
list(Aalborg_Nothermonight.columns)

table_for_corr_Aalborg_Nothermonight=Aalborg_Nothermonight[['hconv',
                                                            'biomassconcentration',
                                                            'tubediameter',
                                                            'gapbetweentubes',
                                                            'horizontaldistance',
                                                            'flowrate',
                                                            'Heating kWh PBR',
                                                            'Cooling kWh PBR',
                                                            'Electricity mixing kWh PBR',
                                                            'GWP100',
                                                            'WDP',
                                                            'TETPinf',
                                                            'FEP',
                                                            'Volumetric productivity kg.L-2.d-1',
                                                            'exchange area m2',
                                                            'tube length m',
                                                            'PBR volume m3']]


cor_Aalborg_Nothermonight=table_for_corr_Aalborg_Nothermonight.corr()
plt.figure(figsize=(16, 6))
heatmap = sns.heatmap(cor_Aalborg_Nothermonight, vmin=-1, vmax=1, annot=True, cmap='BrBG')
heatmap.set_title('Correlation Heatmap, Aalborg, NoThermoregulation at night', fontdict={'fontsize':18}, pad=12);

plt.savefig('heatmap,Aalborg, NoThermoregulation at night.png', dpi=300, bbox_inches='tight')
 


