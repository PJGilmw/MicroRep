
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:26:10 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
pijo@plan.aau.dk
"""


'''Execute the whole script to export an excel file containing the cooling and 
heating energy consumptions calculated by the model in the context of the PBR 
from Pérez-López et al. 2017.  (cf. SI I)

'''



import os
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import itertools
import Functions_for_physical_and_biological_calculations_1 as functions
import Retrieving_solar_and_climatic_data_1 as solardata
import math
import pandas as pd
import Cultivation_simul_Night_Harvest_1 as cultsimul

###
# Execute the import to run the functions individually if needed

elemental_contents = pd.read_csv(
                    "elemental_contents.csv", sep=";",
                    header=0, encoding='unicode_escape',
                    engine='python')
elemental_contents = elemental_contents.iloc[:, 1:]
###


# Validating thermoregulation module with Pérez-López et al. 2017. 

# Estimating input data from Perez Lopez



# Wageningen :
# lat: 51.97
# long : 5.66667


# height =1
# tube diameter = 0.046
#gapbetweentubes = 0.07
#horizontaldistance=0.44

#  Total volume

functions.PBR_geometry(1, 0.046, 0.07, 0.44,
                 6, 5)[0]*31

#1.06 m3


Biodict={'rhoalgae':1100,
          'lipid_af_dw':0.10,
          'ash_dw':0.05,
          'MJ_kglip' :36.3,
          'MJ_kgcarb' :17.3,
          'MJ_kgprot' :23.9,
          'PAR' :0.45,
          'losspigmentantenna' :0.21,
          'quantumyield' :8,
          'lossvoltagejump' :1-1267/1384,
          'losstoATPNADPH' :1-590/1267,
          'losstohexose' :1-469/590,
          'lossrespiration' :0.10,
          'bioact_fraction_molec' : 0.5,  #0<x<1
          'prob_no3' :0.5,
          'Topt':16,
          'T_plateau':5,
          'dcell':20*10**-6,
          'incorporation_rate':0.10,
          'nutrient_utilisation': 0.85,
          'co2_utilisation': 0.85,
          'phospholipid_fraction' : 0.10

          }




# Initiliazing table which will receive the results

results_thermoregulation_convective = pd.DataFrame(np.zeros((12, 7)),
                                         columns=['hconv',
                                             'Summer Cooling',
                                                  'Summer Heating',
                                                  'Fall Cooling',
                                                  'Fall Heating',
                                                  'Winter Cooling',
                                                  'Winter Heating' ])


list_hconv = range(50,110,5)

list_hconv=[a/10 for a in list_hconv] 

for hconv_index in range(0,len(list_hconv)) :

   
    results_thermoregulation_convective['hconv'][hconv_index]=list_hconv[hconv_index]


    # Function inputs
    
    # cultsimul.cultivation_simulation_timestep10(hconv,
    #                                       Twell,
    #                                       depth_well,
    #                                       lat,
    #                                       long,
    #                                       azimuthfrontal,  # environment
    #                                       month,  # period
    #                                       Cp,  # Physics
    #                                       height,
    #                                       tubediameter,
    #                                       gapbetweentubes,
    #                                       horizontaldistance,
    #                                       length_of_PBRunit,
    #                                       width_of_PBR_unit,  # PBR geometry
    #                                       rhoalgae,
    #                                       rhomedium,
    #                                       rhosuspension,
    #                                       dcell,
    #                                       Tmax,
    #                                       Tmin,
    #                                       Biodict,
    #                                       ash_dw,
    #                                       Nsource,  # strain
    #                                       pourcentage_yield,  # which pourcentage of the maximum yield is achieved ?
    #                                       biomassconcentration,
    #                                       flowrate,  # operational
    #                                       centrifugation_efficiency,
    #                                       pumpefficiency,  # technological efficiencies
    #                                       slurry_concentration,
    #                                       water_after_drying,
    #                                       recyclingrateaftercentrifuge,
    #                                       night_monitoring,
    #                                       elemental_contents):



    resultsjuly=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                            20,
                                                            10,
                                                            51.970,
                                                            5.667,
                                                            90,   
                                                            7,   # Month
                                                            4.186,
                                                            1,
                                                            0.046,
                                                            0.07,
                                                            0.44,
                                                            5,
                                                            6,
                                                            1100,
                                                            1000,
                                                            1000,
                                                            5*10**-6,
                                                            30,
                                                            20,
                                                            Biodict,
                                                            0.05,
                                                            'no3',
                                                            0.2,
                                                            1.9,
                                                            0.38,
                                                            0.95,
                                                            0.95,
                                                            0.15,
                                                            0.05,
                                                            0.3,
                                                            'yes',
                                                            elemental_contents)
    
    
    resultsaugust=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                              20,
                                                              10,
                                                              51.970,
                                                              5.667,
                                                              90,   
                                                              8,   # Month
                                                              4.186,
                                                              1,
                                                              0.046,
                                                              0.07,
                                                              0.44,
                                                              5,
                                                              6,
                                                              1100,
                                                              1000,
                                                              1000,
                                                              5*10**-6,
                                                              30,
                                                              20,
                                                              Biodict,
                                                              0.05,
                                                              'no3',
                                                              0.2,
                                                              1.9,
                                                              0.38,
                                                              0.95,
                                                              0.95,
                                                              0.15,
                                                              0.05,
                                                              0.3,
                                                              'yes',
                                                              elemental_contents)
    
    resultssept=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                            20,
                                                            10,
                                                            51.970,
                                                            5.667,
                                                            90,
                                                            9,   # Month
                                                            4.186,
                                                            1,
                                                            0.046,
                                                            0.07,
                                                            0.44,
                                                            5,
                                                            6,
                                                            1100,
                                                            1000,
                                                            1000,
                                                            5*10**-6,
                                                            30,
                                                            20,
                                                            Biodict,
                                                            0.05,
                                                            'no3',
                                                            0.2,
                                                            1.9,
                                                            0.38,
                                                            0.95,
                                                            0.95,
                                                            0.15,
                                                            0.05,
                                                            0.3,
                                                            'yes',
                                                            elemental_contents)
    
    resultsoct=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                           20,
                                                           10,
                                                           51.970,
                                                           5.667,
                                                           90,   
                                                           10,   # Month
                                                           4.186,
                                                           1,
                                                           0.046,
                                                           0.07,
                                                           0.44,
                                                           5,
                                                           6,
                                                           1100,
                                                           1000,
                                                           1000,
                                                           5*10**-6,
                                                           30,
                                                           20,
                                                           Biodict,
                                                           0.05,
                                                           'no3',
                                                           0.2,
                                                           1.9,
                                                           0.38,
                                                           0.95,
                                                           0.95,
                                                           0.15,
                                                           0.05,
                                                           0.3,
                                                           'yes',
                                                           elemental_contents)


    resultsnov=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                           20,
                                                           10,
                                                           51.970,
                                                           5.667,
                                                           90,   
                                                           11,   # Month
                                                           4.186,
                                                           1,
                                                           0.046,
                                                           0.07,
                                                           0.44,
                                                           5,
                                                           6,
                                                           1100,
                                                           1000,
                                                           1000,
                                                           5*10**-6,
                                                           30,
                                                           20,
                                                           Biodict,
                                                           0.05,
                                                           'no3',
                                                           0.2,
                                                           1.9,
                                                           0.38,
                                                           0.95,
                                                           0.95,
                                                           0.15,
                                                           0.05,
                                                           0.3,
                                                           'yes',
                                                           elemental_contents)    

    resultsdec=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                           20,
                                                           10,
                                                           51.970,
                                                           5.667,
                                                           90,   
                                                           12,   # Month
                                                           4.186,
                                                           1,
                                                           0.046,
                                                           0.07,
                                                           0.44,
                                                           5,
                                                           6,
                                                           1100,
                                                           1000,
                                                           1000,
                                                           5*10**-6,
                                                           30,
                                                           20,
                                                           Biodict,
                                                           0.05,
                                                           'no3',
                                                           0.2,
                                                           1.9,
                                                           0.38,
                                                           0.95,
                                                           0.95,
                                                           0.15,
                                                           0.05,
                                                           0.3,
                                                           'yes',
                                                           elemental_contents)    

    
    resultsjanv=cultsimul.cultivation_simulation_timestep10(list_hconv[hconv_index],
                                                           20,
                                                           10,
                                                           51.970,
                                                           5.667,
                                                           90,   
                                                           1,   # Month
                                                           4.186,
                                                           1,
                                                           0.046,
                                                           0.07,
                                                           0.44,
                                                           5,
                                                           6,
                                                           1100,
                                                           1000,
                                                           1000,
                                                           5*10**-6,
                                                           30,
                                                           20,
                                                           Biodict,
                                                           0.05,
                                                           'no3',
                                                           0.2,
                                                           1.9,
                                                           0.38,
                                                           0.95,
                                                           0.95,
                                                           0.15,
                                                           0.05,
                                                           0.3,
                                                           'yes',
                                                           elemental_contents)    
    
    # Total heating  over the cultivation periods followed by Pérez-López et al. 2017. 
    
    # Summer
    
    totalcooling_summer=resultsjuly[0]*25 + resultsaugust[0]*22
    
    totalheating_summer=resultsjuly[1]*25 + resultsaugust[1]*22

    
    results_thermoregulation_convective['Summer Cooling'][hconv_index] = totalcooling_summer
    
    results_thermoregulation_convective['Summer Heating'][hconv_index] = totalheating_summer
    
    #  Fall
    
    totalcooling_fall=resultsaugust[0]*4+resultssept[0]*30 + resultsoct[0]*30+resultsnov[0]*4

    totalheating_fall=resultsaugust[1]*4+resultssept[1]*30 + resultsoct[1]*30+resultsnov[1]*4


    results_thermoregulation_convective['Fall Cooling'][hconv_index] = totalcooling_fall

    results_thermoregulation_convective['Fall Heating'][hconv_index] = totalheating_fall

    # Winter

    totalcooling_winter = resultsnov[0]*23+resultsdec[0]*17

    totalheating_winter = resultsnov[1]*23+resultsdec[1]*17


    results_thermoregulation_convective['Winter Cooling'][hconv_index] = totalcooling_winter

    results_thermoregulation_convective['Winter Heating'][hconv_index] = totalheating_winter



# Export table to folder


results_thermoregulation_convective.to_excel( 'Validation_Thermoregulation.xlsx', 
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





