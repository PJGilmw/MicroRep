# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 11:41:03 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
pijo@plan.aau.dk

"""

'''
Script which calls the final function and runs the simulations to 
generate the tables from which the figures of the paper are plotted.
It performs the uncertainty propagation and sensitivity analysis for :
    
    - Aalborg without Thermoregulation at night
    - Aalborg with Thermoregulation at night
    - Granada without Thermoregulation at night
    - Granada with Thermoregulation at night

For each scenario, it exports excel files for all scenarios in the "Code" folder. 
These files are ready to be read by the R plotting script




INSTRUCTIONS :
    
    -Choose the size of the sample for uncertainty propagation with the lines below
    -Execute the whole script without modification and wait .

'''


'''Choose the size of the generated sample

Original size of the FAST sample : 1500 ( 6 * 1500 = 9000 iterations)

Total expected time for size = 1500 (4*9000 iterations) : 11h - 16h 

Limit background activities and  connect the battery to power supply to limit computing time

You can set a smaller size for faster results.
'''



# Must be >64 
Size_sample = 65  # > 64










##############



import datetime
from time import *
import requests
import pickle
import cProfile
from scipy.integrate import odeint
import numpy as np
import os
import pandas as pd
import decimal
from random import *
import pstats
from itertools import *
from math import*
import csv
import copy

import bw2data
import bw2io
from bw2data.parameters import *
import brightway2 as bw


from SALib.test_functions import Ishigami
import math
from SALib.sample import saltelli
from SALib.sample import fast_sampler
from SALib.analyze import sobol
from SALib.analyze import fast
import SALib

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d

import Cultivation_simul_Night_Harvest_1 as cultsimul
import Functions_for_physical_and_biological_calculations_1 as functions
import Main_simulations_functions_1 as mainfunc



currentfolder = os.getcwd()








# Managing Brightway projects and databases

# Loading the right project

bw.projects.set_current('Microalgae_Sim') 


bw.databases

# Loading Ecoinvent
Ecoinvent = bw.Database('ecoinvent 3.6 conseq')


# Loading foreground database

MICAH = bw.Database('Microalgae_foreground')

# Loading biosphere

biosph = bw.Database('biosphere3')




# Names of IA methods

methods_selected = ([
     ('ReCiPe Midpoint (H) V1.13', 'terrestrial ecotoxicity', 'TETPinf'),
     ('ReCiPe Midpoint (H) V1.13', 'climate change', 'GWP100'),
     ('ReCiPe Midpoint (H) V1.13', 'freshwater eutrophication', 'FEP'),
     ('ReCiPe Midpoint (H) V1.13', 'water depletion', 'WDP')])


# Accessory functions

def createFolder(directory):
    '''Creates a folder/directory with the path given as input'''
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def export_pickle(var, name_var):
    '''Saves a pickle in the working driectory and
    saves the object in input across python sessions'''

    with open(name_var+'.pkl', 'wb') as pickle_file:
        pickle.dump(var, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)




# Loading necessary activites from the database to use them as inputs to the functions

for act in MICAH:
    # The original wastewater treatment activity
    if act['name'] == 'treatment of wastewater, average, capacity 1E9l/year PBR':
        wastewater = MICAH.get(act['code'])
        
for act in MICAH:
    # The original Molecule production activity
    if act['name'] == 'Molecule production PBR':
        # print('oik')
        Molprod = MICAH.get(act['code'])   






''' Initialization '''



# Calculating the Impacts for 1 unit of each of the tehcnosphere inputs 
# to the molecule production

list_foreground_technosphere_inputs_FU = []

list_foreground_technosphere_inputs_names = []

for exc in list(Molprod.exchanges()):

        if exc['type']!='production':
            
            exchange1 = MICAH.get(exc['input'][1])  
            
            name_exchange = exchange1['name']  
            
            list_foreground_technosphere_inputs_names.append(name_exchange)
        
            list_foreground_technosphere_inputs_FU.append({exchange1 : 1})
    

my_calculation_setup = {'inv': list_foreground_technosphere_inputs_FU, 'ia': methods_selected}

bw.calculation_setups['mono_technosphere_inputs'] = my_calculation_setup



# Calculating the impacts for all chosen methods

mlca_techno = bw.MultiLCA('mono_technosphere_inputs')  

res = mlca_techno.results

dict_mono_technosphere_lcas = { name : results for (name, results) in zip(list_foreground_technosphere_inputs_names,res) }




# Wastewater treatment activity is broken down to technoshpere inputs and biosphere outputs
# Technosphere inputs per cubic meter of wastewater constant for any microalga
# Biosphere outputs depend on the composition of the waste water and are then 
# calculated after the cultivation simulation



#Technosphere of wastewater treatment


list_wastewater_technosphere_inputs_FU = []

list_wastewater_technosphere_inputs_names = []

for exc in list(wastewater.exchanges()): # original activity

        if exc['type']=='technosphere':
            
            exchange1 = Ecoinvent.get(exc['input'][1])  # Full name
            
            name_exchange = exchange1['name']  # Name
            
            list_wastewater_technosphere_inputs_names.append(name_exchange)
        
            list_wastewater_technosphere_inputs_FU.append({exchange1 : exc['amount']})
    


my_calculation_setup = {'inv': list_wastewater_technosphere_inputs_FU, 'ia': methods_selected}

bw.calculation_setups['mono_technosphere_wastewater_inputs'] = my_calculation_setup

mlca_waste_water_techno = bw.MultiLCA('mono_technosphere_wastewater_inputs')  


# Impact for the technosphere inputs  for 1 cubic meter of  to waste water 

res_wastewater_technospere = mlca_waste_water_techno.results


dict_mono_technosphere_wastewater_lcas = { name : results for (name, results) in zip(list_wastewater_technosphere_inputs_names,res_wastewater_technospere) }


# Sum the impacts for all technosphere inputs to the treatment of 1 cubic meter
                                                                                            
list_sum_impacts_technosphere_waste_water = []

for meth_index in range(len(methods_selected)):
    
    sum_impact = sum([dict_mono_technosphere_wastewater_lcas[flow][meth_index] for flow in dict_mono_technosphere_wastewater_lcas ])
    
    list_sum_impacts_technosphere_waste_water.append(sum_impact)
    
    
# Update the dictionnary with the impacts associated to the technosphere inputs to 1 cubic meter of wastewater treatment.  

dict_mono_technosphere_lcas['Wastewater treatment PBR'] = list_sum_impacts_technosphere_waste_water         


 

# dict_mono_technosphere_lcas now contains the impact for 1 unit of each process of the LCI 
# except for the direct biosphere flows from wasterwater treatment which will be added for each LCI calculation.
                                               




# Initializing the LCI dictionnary

# Each flow has the same name of the corresponding activity 
# in the original database

LCIdict = {'market for ammonium sulfate, as N PBR': 0,  
           'market for calcium nitrate PBR': 0,
           'P source production PBR': 0,
           'Hydrogen peroxyde PBR': 0,
           'K source production PBR': 0,
           'Land PBR': 0,
           'Glass PBR': 0,
           'Hypochlorite PBR': 0,
           'Microalgae CO2 PBR': 0,
           'Heating kWh PBR': 0,
           'Cooling kWh PBR': 0,
           'Electricity centrifuge kWh PBR': 0,
           'Electricity mixing kWh PBR': 0,
           'Electricity pumping kWh PBR': 0,
           'Electricity drying kWh PBR': 0,
           'Electricity cell disruption kWh PBR': 0,
           'Electricity cell disruption kWh PBR': 0,
           'Electricity aeration kWh PBR':0,
           'Feed energy PBR': 0,
           'Feed protein PBR': 0,
           'LT Fishmeal PBR': 0,
           'Rapeseed oil PBR': 0,
           'Wheat PBR': 0,
           'Wheat gluten PBR': 0,
           'Fish oil PBR': 0,
           'Soyabean meal PBR': 0,
           'Poultry meal PBR': 0,
           'Hemoglobin meal PBR': 0,
           'Electricity cell disruption kWh PBR': 0,
           'Co solvent Extraction PBR': 0,
           'Extraction electricity kWh PBR': 0,
           'Mg source production PBR': 0,
           'Wastewater treatment PBR': 0,
           'Water Cleaning PBR': 0,
           'Water(Cultivation) PBR': 0,
           'CO2 direct emissions PBR': 0}


# Assigning each process to a a broader category for contribution analysis

# Names of categories

categories_contribution = ['Thermoregulation',
                           'Direct land occupation',
                           'Post harvest processing',
                           'Harvesting',
                           'Culture mixing',
                           'Water Pumping',
                           'Substitution by co-products',
                           'Use of glass',
                           'Nutrients consumption',
                           'CO2 consumption',
                           'Water consumption and treatment',
                           'Cleaning']

len(categories_contribution)

# List of processes to assign to categories (same order)

processes_in_categories = [['Cooling kWh PBR', 'Heating kWh PBR'],
                           ['Land PBR'],
                           ['Co solvent Extraction PBR', 'Extraction electricity kWh PBR',
                               'Electricity cell disruption kWh PBR', 'Electricity drying kWh PBR'],
                           ['Electricity centrifuge kWh PBR'],
                           ['Electricity mixing kWh PBR'],
                           ['Electricity pumping kWh PBR'],
                           ['Feed energy PBR', 'Feed protein PBR', 'Fish oil PBR', 'Hemoglobin meal PBR', 'LT Fishmeal PBR',
                               'Poultry meal PBR', 'Rapeseed oil PBR', 'Soyabean meal PBR', 'Wheat gluten PBR', 'Wheat PBR'],
                           ['Glass PBR'],
                           ['market for ammonium sulfate, as N PBR', 'market for calcium nitrate PBR', 'P source production PBR',
                             'K source production PBR', ],
                           ['Microalgae CO2 PBR','CO2 direct emissions PBR'],
                           ['Water(Cultivation) PBR','Wastewater treatment PBR'],
                           ['Hypochlorite PBR', 'Hydrogen peroxyde PBR','Water Cleaning PBR']]



# Uploading the necessary csv files

# Fish feed composition

fishfeed_table = pd.read_csv("Feed_composition.csv", sep=";",
                             header=0, encoding='unicode_escape', engine='python')

# Cleaning

fishfeed_table = fishfeed_table[0:8][[
    'Ingredient', 'kg.kg feed-1', 'Lipid', 'Protein', 'Carb', 'Ash', 'Water']]

# Elemental composition of macronutrients

elemental_contents = pd.read_csv("elemental_contents.csv",
                                 sep=";",
                                 header=0,
                                 encoding='unicode_escape',
                                 engine='python')

# Cleaning

elemental_contents = elemental_contents.iloc[:, 1:]







# Primary Parameters dictionnaries

# Description of the parameters are given in the appendix.
# Here values can be changed for parameters with unique values (no distributions)
# Values with distributions will be overwritten.

#Biological parameters


Biodict = {'rhoalgae': 1070, # kg.m-3
           'lipid_af_dw': 0.3,   # .
           'ash_dw': 0.05,  # .
           'MJ_kglip': 36.3,  # MJ.kg-1
           'MJ_kgcarb': 17.3,  # MJ.kg-1
           'MJ_kgprot': 23.9,  # MJ.kg-1
           'PAR': 0.45,  # .
           'losspigmentantenna': 0.21,  # .
           'quantumyield': 8,  # molphotons.moloxygen-1
           'lossvoltagejump': 1-1267/1384,  # .
           'losstoATPNADPH': 1-590/1267,  # .
           'losstohexose': 1-469/590,  # .
           'lossrespiration': 0.20,  # .
           'bioact_fraction_molec': 0.1,  # .
           'prob_no3': 1,   # .
           'Topt': 25,  # °C
           'T_plateau': 10,  # °C
           'dcell': 5*10**-6,  # m
           'incorporation_rate': 0.10,  # .
           'nutrient_utilisation': 0.9, # .
           'co2_utilisation': 0.85,  # .
           'phospholipid_fraction': 0.20  # .

           }

# Physical parameters

Physicdict = {'hconv': 6.6189,  # W.m−2 .K−1
              'Cp': 4.186,  # kJ.(kg.K)-1
              'rhomedium': 1000,  # kg.m-3
              'rhowater': 1000,  # kg.m-3
              'Cw': 2256}  # kJ.kg-1



#Geographic parameters

#  Granada 37.189, -3.572
#  Aalborg 57.109, 10.193


Locationdict = {'lat': 37.189, #°
                'long': -3.572, #°
                'Twell': 10,  # °C
                'depth_well': 10,  # m
                'azimuthfrontal': 90} # °


#Techno-operational parameters

Tech_opdict = {'height': 1.5,  # m
                   'tubediameter': 0.03,  # m
                   'gapbetweentubes': 0.01,  # m
                   'horizontaldistance': 0.2,  # m
                   'length_of_PBRunit': 30,    # m
                   'width_of_PBR_unit': 30,   # m
                   'biomassconcentration': 1.4,  # kg.m-3
                   'flowrate': 0.38,     # m.s-1
                   'centrifugation_efficiency': 0.98,  # .
                   'pumpefficiency': 0.90,  # .
                   'slurry_concentration': 0.15,  # .
                   'water_after_drying': 0.05,  # gwater.g dbio-1
                   'recyclingrateaftercentrifuge': 0.3, # gwater.g dbio-1
                   'rhosuspension': 1015,  # kg.m-3 
                   'roughness': 0.0000015,  # m
                   'cleaningvolumeVSfacilityvolume': 4,  # .
                   'concentration_hypo': 2*10**-3,  # kg.m-3
                   'concentration_hydro': 30,  # kg.m-3
                   'boilerefficiency': 0.75,  # .
                   'glass_life_expectancy': 50, # years
                   
                   # A value of 1 for Thermoregulation at night
                   'prob_night_monitoring': 0,
                   'extraction': 'yes',

                    # A value of 0 to use the fish feed substitution
                   'prob_market_subst_animal_feed': 0  # .

                   }


# Parameters distribution directories 

# Exact same parameters dictionnaries the normal ones but instead of one value,
# each parameter is assigned a list containing  :
   # [Distribution,min,max,mode,sd]

# Distribution :
#   - 'unique' if no distribution. The value indicated indicated in
#     the normal dictionnary will be considered.
#   - 'unif' for uniform, uses min and max
#   - 'triangl, uses mim max and mode with mode as a fracion of max-min

#

# Biological parameters

Biodict_distributions = {'rhoalgae': ['unique', [0, 1020, 1250, 0, 0]], 
                           
                         'lipid_af_dw': ['unique', [0, 0.3, 0.72, 0.10, 0]],
                         
                         'ash_dw': ['unique', [0, 0.01, 0.10, 0.10, 0]],
                         
                         'MJ_kglip': ['unique', [36.3, 0, 0, 0, 0]],
                       
                         'MJ_kgcarb': ['unique', [17.3, 0, 0, 0, 0]],
                        
                         'MJ_kgprot': ['unique', [23.9, 0, 0, 0, 0]],
                         'PAR': ['unique', [0.45, 0, 0, 0, 0]],
                        
                         'losspigmentantenna': ['unique', [0, 0.16, 0.24, 0, 0]],
                        
                         'quantumyield': ['unique', [0.45, 8, 11, 0, 0]],
                         
                         'lossvoltagejump': ['unique', [1-1267/1384, 0, 0, 0, 0]],
                       
                         'losstoATPNADPH': ['unique', [1-590/1267, 0, 0, 0, 0]],
                 
                         'losstohexose': ['unique', [1-469/590, 0, 0, 0, 0]],
                      
                         'lossrespiration': ['unique', [0, 0.16, 0.24, 0, 0]],
                    
                         'bioact_fraction_molec': ['unique', [0, 0.01, 0.8, 0, 0]],
                         
                         'prob_no3': ['unique', [0, 0, 1, 0, 0]],
                         
                         'Topt': ['unique', [0, 15, 35, 25, 0]],
                         
                         'T_plateau': ['unique', [0, 5, 10, 0, 0]],
                      
                         'dcell': ['unique', [0, 0.000001, 0.000005, 0.000005, 0]],
                
                         'incorporation_rate': ['unique', [0, 0.01, 0.15, 0, 0]],

                         'nutrient_utilisation': ['unique', [0, 0.75, 0.90, 0, 0]],
             
                         'co2_utilisation': ['unique', [0, 0.5, 0.95, 0.9, 0]],
            
                         'phospholipid_fraction': ['unique', [0, 0.1, 0.6, 0, 0]]

                         }
# Physical parameters

Physicdict_distributions = {
    'hconv': ['unif', [0, 5, 10, 0, 0]],
    
    'Cp': ['unique', [4.186, 0, 0, 0, 0]],
     
    'rhomedium': ['unique', [1000, 0, 0, 0, 0]],
    
    'rhowater': ['unique', [1000, 0, 0, 0, 0]],
    
    'Cw': ['unique', [2256, 0, 0, 0, 0]]}

Locationdict_distributions = {'lat': ['unique', [43.695, 0, 0, 0, 0]],
                              
                              'long': ['unique', [1.922, 0, 0, 0, 0]],
                              
                              'Twell': ['unique', [0, 5, 25, 0, 0]],
                              
                              'depth_well': ['unique', [0, 5, 25, 0, 0]],
                              
                              'azimuthfrontal': ['unique', [90, 0, 0, 0, 0]]}

Tech_opdict_distributions = {'height': ['unique', [1.5, 0, 0, 0, 0]],   
                              
                                 'tubediameter': ['unif', [0, 0.03, 0.1, 0, 0]],
                                 
                                 'gapbetweentubes': ['unif', [0, 0.01, 0.1, 0, 0]],
                                 
                                 'horizontaldistance': ['unif', [0, 0.2, 0.8, 0, 0]],
                                 
                                 'length_of_PBRunit': ['unique', [20, 10, 35, 0, 0]], 
                                 
                                 'width_of_PBR_unit': ['unique', [20, 3, 10, 0, 0]], 
                                 
                                 'biomassconcentration': ['unif', [0, 1, 7, 0, 0]], 
                                 
                                 'flowrate': ['unif', [0, 0.2, 1, 0, 0]],
                                 
                                 'centrifugation_efficiency': ['unique', [0.98, 0, 0, 0, 0]], 
                                 
                                 'pumpefficiency': ['unique', [0.9, 0, 0, 0, 0]], 
                                                                  
                                 'slurry_concentration': ['unique', [0, 0.10, 0.20, 0, 0]], 
                                 
                                 'water_after_drying': ['unique', [0, 0.02, 0.07, 0, 0]], 
                                 
                                 'recyclingrateaftercentrifuge': ['unique', [0, 0.2, 0.4, 0, 0]],
                                 
                                 'rhosuspension': ['unique', [0, 1000, 1200, 0, 0]], 
                                 
                                 'roughness': ['unique', [0.0000015, 0, 0, 0, 0]], 
                                 
                                 'cleaningvolumeVSfacilityvolume': ['unique', [0, 2, 6, 0, 0]], 
                                 
                                 'concentration_hypo': ['unique', [2*10**-3, 0, 0, 0, 0]], 
                                 
                                 'concentration_hydro': ['unique', [30, 0, 0, 0, 0]], 
                                 
                                 'glass_life_expectancy': ['unique', [50, 0, 0, 0, 0]], 

                                 'boilerefficiency': ['unique', [0.75, 0, 0, 0, 0]],  
                                 
                                 'prob_night_monitoring': ['unique', [0, 0, 1, 0, 0]], 
                                 
                                 'extraction': ['binary', ['yes', 0, 0, 0, 0]],

                                 'prob_market_subst_animal_feed': ['unique', [0, 0, 1, 0, 0]],
                                 }



















''' Simulating'''



###
#Simulating for Aalborg without thermoregulation at night
###


#  Granada 37.189, -3.572
#  Aalborg 57.109, 10.193

# We just modify the location and the thermoregulation in the dictionnaries with primary parameters


Locationdict = {'lat': 57.109, #°
                'long': 10.193, #°
                'Twell': 10,  # °C
                'depth_well': 10,  # m
                'azimuthfrontal': 90} # °

Tech_opdict = {'height': 1.5,  # m
                   'tubediameter': 0.03,  # m
                   'gapbetweentubes': 0.01,  # m
                   'horizontaldistance': 0.2,  # m
                   'length_of_PBRunit': 30,    # m
                   'width_of_PBR_unit': 30,   # m
                   'biomassconcentration': 1.4,  # kg.m-3
                   'flowrate': 0.38,     # m.s-1
                   'centrifugation_efficiency': 0.98,
                   'pumpefficiency': 0.90,
                   'slurry_concentration': 0.15,
                   'water_after_drying': 0.05,
                   'recyclingrateaftercentrifuge': 0.3,
                   'rhosuspension': 1015,  # kg.m-3 
                   'roughness': 0.0000015,  # m
                   'cleaningvolumeVSfacilityvolume': 4,
                   'concentration_hypo': 2*10**-3,  # kg.m-3
                   'concentration_hydro': 30,  # kg.m-3
                   'boilerefficiency': 0.75,
                   'glass_life_expectancy': 50,
                   
                   # A value of 1 for Thermoregulation at night
                   # A value of 0 for No  Thermoregulation at night
                   
                   'prob_night_monitoring': 0,
                   
                   'extraction': 'yes',

                    # A value of 0 to use the fish feed substitution
                   'prob_market_subst_animal_feed': 0

                   }


a = time()  # For indication

res_Aal_Nothermo = mainfunc.final_function_simulations(dict_mono_technosphere_lcas,
                                 Tech_opdict,  # To modify at the beginning
                                 Biodict,  # To modify at the beginning
                                 Locationdict,  # To modify at the beginning
                                 Physicdict,  # To modify at the beginning
                                 Tech_opdict_distributions,  # To modify at the beginning
                                 Biodict_distributions,  # To modify at the beginning
                                 Locationdict_distributions,  # To modify at the beginning
                                 Physicdict_distributions,  # To modify at the beginning
                                 LCIdict,  # Do not modify
                                 Size_sample,  # Sample size
                                 [4, 5, 6, 7, 8, 9],  # Paper value
                                 0.3,  # Paper value
                                 elemental_contents,  # To modify in the csv
                                 fishfeed_table,  # To modify in the csv
                                 methods_selected,  # To modify at the beginning
                                 categories_contribution,  # To modify at the beginning
                                 processes_in_categories,  # To modify at the beginning
                                 'FAST', # Type of sensitivity analysis and stochastic samples 
                                 )  



b = time()-a  # For indication
print('Total time :',b)


# Export the results for plotting

# Output of final_function_simulations :
    
# return (sample,  0
#         problem_sobol_FAST,  1
#         results_table_df,  2
#         results_table,   3
#         results_sobol_fast,  4
#         list_tables_contribution_df_melted,  5
#         list_tables_contribution_abs_df_melted,   6
#         all_methods_contribution_abs_df_melted,  7
#         list_tables_contribution_df,  8
#         list_opti_perfo,   9
#         result_LCI_rescaled,  10
#         sensi_multi_melt,   11
#         desc_stat_results,   12
#         total_desc_stat_contri_df) 13


# Contributions

all_methods_contribution_df_melted_Aal_Nothermo = res_Aal_Nothermo[7]


all_methods_contribution_df_melted_Aal_Nothermo.to_csv('all_methods_contribution_df_melted_Aal_Nothermo.csv', sep=';', encoding='utf-8')



# Results of all simulations with LCIA results

results_table_df_Aal_Nothermo =  res_Aal_Nothermo[2]


results_table_df_Aal_Nothermo.to_excel('results_table_df_Aal_Nothermo.xlsx',
                          sheet_name='Sheet1',
                          na_rep='',
                          float_format=None,
                          columns=None,
                          header=True,
                          index=True,
                          index_label=None,
                          startrow=0,
                          startcol=0,
                          engine=None,
                          merge_cells=True,
                          encoding=None,
                          inf_rep='inf', 
                          verbose=True, 
                          freeze_panes=None, 
                          storage_options=None)



# Sensitivity

sensi_multi_melt_Aal_Nothermo = res_Aal_Nothermo[11]




sensi_multi_melt_Aal_Nothermo.to_excel('sensi_multi_melt_Aal_Nothermo.xlsx', 
              sheet_name='Sheet1',
              na_rep='', 
              float_format=None,
              columns=None,
              header=True, 
              index=True,
              index_label=None,
              startrow=0,
              startcol=0,
              engine=None,
              merge_cells=True,
              encoding=None,
              inf_rep='inf',
              verbose=True,
              freeze_panes=None,
              storage_options=None)




# Statistical Description of results

desc_LCI_Aal_Nothermo = res_Aal_Nothermo[12]

desc_LCI_Aal_Nothermo.to_excel('desc_LCI_Aal_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Statistical Description of contributions

desc_contributions_Aal_Nothermo = res_Aal_Nothermo[13]

desc_contributions_Aal_Nothermo.to_excel('desc_contributions_Aal_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Table with LCI figures rescaled to 1 kg of dried biomass

result_LCI_rescaled_Aal_Nothermo = res_Aal_Nothermo[10]

result_LCI_rescaled_Aal_Nothermo.to_excel('result_LCI_rescaled_Aal_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)



###
#Simulating for Aalborg with Thermoregulation at night
###


#  Granada 37.189, -3.572
#  Aalborg 57.109, 10.193

# We just modify the location and the thermoregulation

Locationdict = {'lat': 57.109, #°
                'long': 10.193, #°
                'Twell': 10,  # °C
                'depth_well': 10,  # m
                'azimuthfrontal': 90} # °

Tech_opdict = {'height': 1.5,  # m
                   'tubediameter': 0.03,  # m
                   'gapbetweentubes': 0.01,  # m
                   'horizontaldistance': 0.2,  # m
                   'length_of_PBRunit': 30,    # m
                   'width_of_PBR_unit': 30,   # m
                   'biomassconcentration': 1.4,  # kg.m-3
                   'flowrate': 0.38,     # m.s-1
                   'centrifugation_efficiency': 0.98,
                   'pumpefficiency': 0.90,
                   'slurry_concentration': 0.15,
                   'water_after_drying': 0.05,
                   'recyclingrateaftercentrifuge': 0.3,
                   'rhosuspension': 1015,  # kg.m-3 
                   'roughness': 0.0000015,  # m
                   'cleaningvolumeVSfacilityvolume': 4,
                   'concentration_hypo': 2*10**-3,  # kg.m-3
                   'concentration_hydro': 30,  # kg.m-3
                   'boilerefficiency': 0.75,
                   'glass_life_expectancy': 50,
                   
                   # A value of 1 for Thermoregulation at night
                   # A value of 0 for No  Thermoregulation at night
                   
                   'prob_night_monitoring': 1,
                   
                   'extraction': 'yes',

                    # A value of 0 to use the fish feed substitution
                   'prob_market_subst_animal_feed': 0

                   }


a = time()  # For indication

res_Aal_thermo = mainfunc.final_function_simulations(dict_mono_technosphere_lcas,
                                 Tech_opdict,  # To modify at the beginning
                                 Biodict,  # To modify at the beginning
                                 Locationdict,  # To modify at the beginning
                                 Physicdict,  # To modify at the beginning
                                 Tech_opdict_distributions,  # To modify at the beginning
                                 Biodict_distributions,  # To modify at the beginning
                                 Locationdict_distributions,  # To modify at the beginning
                                 Physicdict_distributions,  # To modify at the beginning
                                 LCIdict,  # Do not modify
                                 Size_sample,  # Sample size
                                 [4, 5, 6, 7, 8, 9],  # Paper value
                                 0.3,  # Paper value
                                 elemental_contents,  # To modify in the csv
                                 fishfeed_table,  # To modify in the csv
                                 methods_selected,  # To modify at the beginning
                                 categories_contribution,  # To modify at the beginning
                                 processes_in_categories,  # To modify at the beginning
                                 'FAST', # Type of sensitivity analysis and stochastic samples 
                                 )  




b = time()-a  # For indication
print('Total time :',b)


# Export the results for plotting

# Output of final_function_simulations :
    
# return (sample,  0
#         problem_sobol_FAST,  1
#         results_table_df,  2
#         results_table,   3
#         results_sobol_fast,  4
#         list_tables_contribution_df_melted,  5
#         list_tables_contribution_abs_df_melted,   6
#         all_methods_contribution_abs_df_melted,  7
#         list_tables_contribution_df,  8
#         list_opti_perfo,   9
#         result_LCI_rescaled,  10
#         sensi_multi_melt,   11
#         desc_stat_results,   12
#         total_desc_stat_contri_df) 13


# Contributions

all_methods_contribution_df_melted_Aal_thermo = res_Aal_thermo[7]


all_methods_contribution_df_melted_Aal_thermo.to_csv('all_methods_contribution_df_melted_Aal_thermo.csv', sep=';', encoding='utf-8')

                   


# Results of all simulations with LCIA results

results_table_df_Aal_thermo=  res_Aal_thermo[2]


results_table_df_Aal_thermo.to_excel('results_table_df_Aal_thermo.xlsx',
                          sheet_name='Sheet1',
                          na_rep='',
                          float_format=None,
                          columns=None,
                          header=True,
                          index=True,
                          index_label=None,
                          startrow=0,
                          startcol=0,
                          engine=None,
                          merge_cells=True,
                          encoding=None,
                          inf_rep='inf', 
                          verbose=True, 
                          freeze_panes=None, 
                          storage_options=None)



# Sensitivity

sensi_multi_melt_Aal_thermo = res_Aal_thermo[11]




sensi_multi_melt_Aal_thermo.to_excel('sensi_multi_melt_Aal_thermo.xlsx', 
              sheet_name='Sheet1',
              na_rep='', 
              float_format=None,
              columns=None,
              header=True, 
              index=True,
              index_label=None,
              startrow=0,
              startcol=0,
              engine=None,
              merge_cells=True,
              encoding=None,
              inf_rep='inf',
              verbose=True,
              freeze_panes=None,
              storage_options=None)




# Statistical Description of LCI

desc_LCI_Aal_thermo = res_Aal_thermo[12]

desc_LCI_Aal_thermo.to_excel('desc_LCI_Aal_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Statistical Description of contributions

desc_contributions_Aal_thermo = res_Aal_thermo[13]

desc_contributions_Aal_thermo.to_excel('desc_contributions_Aal_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Table with LCI figures rescaled to 1 kg of dried biomass

result_LCI_rescaled_Aal_thermo = res_Aal_thermo[10]

result_LCI_rescaled_Aal_thermo.to_excel('result_LCI_rescaled_Aal_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)









###
#Simulating for Granada without thermoregulation at night
###


#  Granada 37.189, -3.572
#  Aalborg 57.109, 10.193

# We just modify the location and the thermoregulation

Locationdict = {'lat': 37.189, #°
                'long': -3.572, #°
                'Twell': 10,  # °C
                'depth_well': 10,  # m
                'azimuthfrontal': 90} # °

Tech_opdict = {'height': 1.5,  # m
                   'tubediameter': 0.03,  # m
                   'gapbetweentubes': 0.01,  # m
                   'horizontaldistance': 0.2,  # m
                   'length_of_PBRunit': 30,    # m
                   'width_of_PBR_unit': 30,   # m
                   'biomassconcentration': 1.4,  # kg.m-3
                   'flowrate': 0.38,     # m.s-1
                   'centrifugation_efficiency': 0.98,
                   'pumpefficiency': 0.90,
                   'slurry_concentration': 0.15,
                   'water_after_drying': 0.05,
                   'recyclingrateaftercentrifuge': 0.3,
                   'rhosuspension': 1015,  # kg.m-3 
                   'roughness': 0.0000015,  # m
                   'cleaningvolumeVSfacilityvolume': 4,
                   'concentration_hypo': 2*10**-3,  # kg.m-3
                   'concentration_hydro': 30,  # kg.m-3
                   'boilerefficiency': 0.75,
                   'glass_life_expectancy': 50,  # years
                   
                   # A value of 1 for Thermoregulation at night
                   # A value of 0 for No  Thermoregulation at night
                   
                   'prob_night_monitoring': 0,
                   
                   'extraction': 'yes',

                    # A value of 0 to use the fish feed substitution
                   'prob_market_subst_animal_feed': 0

                   }


a = time()  # For indication

res_Gra_Nothermo = mainfunc.final_function_simulations(dict_mono_technosphere_lcas,
                                 Tech_opdict,  # To modify at the beginning
                                 Biodict,  # To modify at the beginning
                                 Locationdict,  # To modify at the beginning
                                 Physicdict,  # To modify at the beginning
                                 Tech_opdict_distributions,  # To modify at the beginning
                                 Biodict_distributions,  # To modify at the beginning
                                 Locationdict_distributions,  # To modify at the beginning
                                 Physicdict_distributions,  # To modify at the beginning
                                 LCIdict,  # Do not modify
                                 Size_sample,  # Sample size
                                 [4, 5, 6, 7, 8, 9],  # Paper value
                                 0.3,  # Paper value
                                 elemental_contents,  # To modify in the csv
                                 fishfeed_table,  # To modify in the csv
                                 methods_selected,  # To modify at the beginning
                                 categories_contribution,  # To modify at the beginning
                                 processes_in_categories,  # To modify at the beginning
                                 'FAST', # Type of sensitivity analysis and stochastic samples
                                 )   




b = time()-a  # For indication
print('Total time :',b)


# Export the results for plotting

# Output of final_function_simulations :
    
# return (sample,  0
#         problem_sobol_FAST,  1
#         results_table_df,  2
#         results_table,   3
#         results_sobol_fast,  4
#         list_tables_contribution_df_melted,  5
#         list_tables_contribution_abs_df_melted,   6
#         all_methods_contribution_abs_df_melted,  7
#         list_tables_contribution_df,  8
#         list_opti_perfo,   9
#         result_LCI_rescaled,  10
#         sensi_multi_melt,   11
#         desc_stat_results,   12
#         total_desc_stat_contri_df) 13


# Contributions

all_methods_contribution_df_melted_Gra_Nothermo = res_Gra_Nothermo[7]


all_methods_contribution_df_melted_Gra_Nothermo.to_csv('all_methods_contribution_df_melted_Gra_Nothermo.csv', sep=';', encoding='utf-8')



# Results of all simulations with LCIA results

results_table_df_Gra_Nothermo =  res_Gra_Nothermo[2]


results_table_df_Gra_Nothermo.to_excel('results_table_df_Gra_Nothermo.xlsx',
                          sheet_name='Sheet1',
                          na_rep='',
                          float_format=None,
                          columns=None,
                          header=True,
                          index=True,
                          index_label=None,
                          startrow=0,
                          startcol=0,
                          engine=None,
                          merge_cells=True,
                          encoding=None,
                          inf_rep='inf', 
                          verbose=True, 
                          freeze_panes=None, 
                          storage_options=None)



# Sensitivity

sensi_multi_melt_Gra_Nothermo = res_Gra_Nothermo[11]




sensi_multi_melt_Gra_Nothermo.to_excel('sensi_multi_melt_Gra_Nothermo.xlsx', 
              sheet_name='Sheet1',
              na_rep='', 
              float_format=None,
              columns=None,
              header=True, 
              index=True,
              index_label=None,
              startrow=0,
              startcol=0,
              engine=None,
              merge_cells=True,
              encoding=None,
              inf_rep='inf',
              verbose=True,
              freeze_panes=None,
              storage_options=None)




# Statistical Description of LCI

desc_LCI_Gra_Nothermo = res_Gra_Nothermo[12]

desc_LCI_Gra_Nothermo.to_excel('desc_LCI_Gra_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Statistical Description of contributions

desc_contributions_Gra_Nothermo = res_Gra_Nothermo[13]

desc_contributions_Gra_Nothermo.to_excel('desc_contributions_Gra_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)


# Table with LCI figures rescaled to 1 kg of dried biomass

result_LCI_rescaled_Gra_Nothermo = res_Gra_Nothermo[10]

result_LCI_rescaled_Gra_Nothermo.to_excel('result_LCI_rescaled_Gra_Nothermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)






###
#Simulating for Granada with thermoregulation at night
###


#  Granada 37.189, -3.572
#  Aalborg 57.109, 10.193


# We just modify the location and the thermoregulation

Locationdict = {'lat': 37.189, #°
                'long': -3.572, #°
                'Twell': 10,  # °C
                'depth_well': 10,  # m
                'azimuthfrontal': 90} # °

Tech_opdict = {'height': 1.5,  # m
                   'tubediameter': 0.03,  # m
                   'gapbetweentubes': 0.01,  # m
                   'horizontaldistance': 0.2,  # m
                   'length_of_PBRunit': 30,    # m
                   'width_of_PBR_unit': 30,   # m
                   'biomassconcentration': 1.4,  # kg.m-3
                   'flowrate': 0.38,     # m.s-1
                   'centrifugation_efficiency': 0.98,
                   'pumpefficiency': 0.90,
                   'slurry_concentration': 0.15,
                   'water_after_drying': 0.05,
                   'recyclingrateaftercentrifuge': 0.3,
                   'rhosuspension': 1015,  # kg.m-3 
                   'roughness': 0.0000015,  # m
                   'cleaningvolumeVSfacilityvolume': 4,
                   'concentration_hypo': 2*10**-3,  # kg.m-3
                   'concentration_hydro': 30,  # kg.m-3
                   'boilerefficiency': 0.75,
                   'glass_life_expectancy': 50,  # years
                   
                   # A value of 1 for Thermoregulation at night
                   # A value of 0 for No  Thermoregulation at night
                   
                   'prob_night_monitoring': 1,
                   
                   'extraction': 'yes',

                    # A value of 0 to use the fish feed substitution
                   'prob_market_subst_animal_feed': 0

                   }


a = time()  # For indication

res_Gra_thermo = mainfunc.final_function_simulations(dict_mono_technosphere_lcas,
                                 Tech_opdict,  # To modify at the beginning
                                 Biodict,  # To modify at the beginning
                                 Locationdict,  # To modify at the beginning
                                 Physicdict,  # To modify at the beginning
                                 Tech_opdict_distributions,  # To modify at the beginning
                                 Biodict_distributions,  # To modify at the beginning
                                 Locationdict_distributions,  # To modify at the beginning
                                 Physicdict_distributions,  # To modify at the beginning
                                 LCIdict,  # Do not modify
                                 Size_sample,  # Sample size
                                 [4, 5, 6, 7, 8, 9],  # Paper value
                                 0.3,  # Paper value
                                 elemental_contents,  # To modify in the csv
                                 fishfeed_table,  # To modify in the csv
                                 methods_selected,  # To modify at the beginning
                                 categories_contribution,  # To modify at the beginning
                                 processes_in_categories,  # To modify at the beginning
                                 'FAST',  # Type of sensitivity analysis and stochastic samples 
                                 ) 



b = time()-a  # For indication
print('Total time :',b)


# Export the results for plotting

# Output of final_function_simulations :
    
# return (sample,  0
#         problem_sobol_FAST,  1
#         results_table_df,  2
#         results_table,   3
#         results_sobol_fast,  4
#         list_tables_contribution_df_melted,  5
#         list_tables_contribution_abs_df_melted,   6
#         all_methods_contribution_abs_df_melted,  7
#         list_tables_contribution_df,  8
#         list_opti_perfo,   9
#         result_LCI_rescaled,  10
#         sensi_multi_melt,   11
#         desc_stat_results,   12
#         total_desc_stat_contri_df) 13


# Contributions

all_methods_contribution_df_melted_Gra_thermo = res_Gra_thermo[7]


all_methods_contribution_df_melted_Gra_thermo.to_csv('all_methods_contribution_df_melted_Gra_thermo.csv', sep=';', encoding='utf-8')





# Results of all simulations with LCIA results

results_table_df_Gra_thermo =  res_Gra_thermo[2]


results_table_df_Gra_thermo.to_excel('results_table_df_Gra_thermo.xlsx',
                          sheet_name='Sheet1',
                          na_rep='',
                          float_format=None,
                          columns=None,
                          header=True,
                          index=True,
                          index_label=None,
                          startrow=0,
                          startcol=0,
                          engine=None,
                          merge_cells=True,
                          encoding=None,
                          inf_rep='inf', 
                          verbose=True, 
                          freeze_panes=None, 
                          storage_options=None)



# Sensitivity

sensi_multi_melt_Gra_thermo = res_Gra_thermo[11]




sensi_multi_melt_Gra_thermo.to_excel('sensi_multi_melt_Gra_thermo.xlsx', 
              sheet_name='Sheet1',
              na_rep='', 
              float_format=None,
              columns=None,
              header=True, 
              index=True,
              index_label=None,
              startrow=0,
              startcol=0,
              engine=None,
              merge_cells=True,
              encoding=None,
              inf_rep='inf',
              verbose=True,
              freeze_panes=None,
              storage_options=None)




# Statistical Description of LCI

desc_LCI_Gra_thermo = res_Gra_thermo[12]

desc_LCI_Gra_thermo.to_excel('desc_LCI_Gra_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)



# Statistical Description of contributions

desc_contributions_Gra_thermo = res_Gra_thermo[13]

desc_contributions_Gra_thermo.to_excel('desc_contributions_Gra_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)



# Table with LCI figures rescaled to 1 kg of dried biomass

result_LCI_rescaled_Gra_thermo = res_Gra_thermo[10]

result_LCI_rescaled_Gra_thermo.to_excel('result_LCI_rescaled_Gra_thermo.xlsx', 
             sheet_name='Sheet1',
             na_rep='', 
             float_format=None,
             columns=None,
             header=True, 
             index=True,
             index_label=None,
             startrow=0,
             startcol=0,
             engine=None,
             merge_cells=True,
             encoding=None,
             inf_rep='inf',
             verbose=True,
             freeze_panes=None,
             storage_options=None)









