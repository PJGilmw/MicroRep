# -*- coding: utf-8 -*-
"""
Created on Wed May 19 23:26:10 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
'pijo@plan.aau.dk


"""

"""
Execute the specific blocks to reproduce the thermoregulation module's outputs as in SI I'
"""


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





# Execute these lines as these inputs are needed for the functions
# The values are arbitratry and do not affect the results


###

elemental_contents = pd.read_csv(
                    "elemental_contents.csv", sep=";",
                    header=0, encoding='unicode_escape',
                    engine='python')
elemental_contents = elemental_contents.iloc[:, 1:]



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


###




# Influence of hconv, convective exchange coefficient



listh = [5, 6, 7, 8, 9]



#Plot appendix



# As a reminder , the function takes as inputs :
    
# cultivation_simulation_timestep10(hconv,
#                                       Twell,
#                                       depth_well,
#                                       lat,
#                                       long,
#                                       azimuthfrontal,  
#                                       month,  #  Month
#                                       Cp,  
#                                       height,
#                                       tubediameter,
#                                       gapbetweentubes,
#                                       horizontaldistance,
#                                       length_of_PBRunit,
#                                       width_of_PBR_unit, 
#                                       rhoalgae,
#                                       rhomedium,
#                                       rhosuspension,
#                                       dcell,
#                                       Tmax,
#                                       Tmin,
#                                       Biodict,
#                                       ash_dw,
#                                       Nsource,  
#                                       fraction_maxyield,  
#                                       biomassconcentration,
#                                       flowrate, 
#                                       centrifugation_efficiency,
#                                       pumpefficiency, 
#                                       slurry_concentration,
#                                       water_after_drying,
#                                       recyclingrateaftercentrifuge,
#                                       night_monitoring,
#                                       elemental_contents)


#Heating energy evolution

plt.figure()

for h in listh:
    resultsjuly=cultsimul.cultivation_simulation_timestep10(h,
                                                            10,
                                                            10,
                                                            51.970,
                                                            5.667,
                                                            90,     
                                                            7,       # Month
                                                            4.186,
                                                            1.5,
                                                            0.05,
                                                            0.05,
                                                            0.4,
                                                            5,
                                                            6,
                                                            1100,
                                                            1000,
                                                            1000,
                                                            200*10**-6,
                                                            30,
                                                            20,
                                                            Biodict,
                                                            0.05,
                                                            'no3',  
                                                            0.5, 
                                                            1.9,
                                                            0.38,
                                                            0.95,
                                                            0.95,  
                                                            0.15,
                                                            0.05,
                                                            0.3,
                                                            'yes',
                                                            elemental_contents)



    # Uncomment for november
    
    resultsnov=cultsimul.cultivation_simulation_timestep10(h,10,10,51.970,5.667,90,    
                            11,                                   
                            4.186,   
                            1.5,0.05,0.05,0.4,5,6,   
                            2,1000,1000,200*10**-6,30,20,Biodict,0.05,'no3',  
                            0.5, 
                            1.9,0.38,       
                            0.95,0.95,  
                            0.15,
                            0.05,0.3,'yes',elemental_contents)


    #Replace resultsjuly by resultsnov for november
    
    plt.plot([a/360 for a in range(0,8640)],resultsnov[14], label=str(h))
    
    

plt.legend(title='hconv',loc='best', ncol=2)
plt.xlabel('Time of the day, h')
plt.ylabel('kWh')
plt.title('Heating-November')

plt.savefig('C:/Users/GF20PZ/OneDrive - Aalborg Universitet/Dokumenter/AAU/Microalgae production/Paper drafts/Figures papers/Thermo/hconvinfluence_heating_november.png',dpi=300, bbox_inches='tight')



#Cooling energy evolution

plt.figure()

for h in listh:
    
    # Uncomment for july

    resultsjuly=cultsimul.cultivation_simulation_timestep10(h,10,10,51.970,5.667,90,    
                                7,  # Month
                                4.186,
                                1.5,0.05,0.05,0.4,5,6,
                                1100,1000,1000,200*10**-6,30,20,Biodict,0.05,'no3',
                                0.5,
                                1.9,0.38, 
                                0.95,0.95,
                                0.15,
                                0.05,0.3,'yes',elemental_contents)

    resultsnov=cultsimul.cultivation_simulation_timestep10(h,10,10,51.970,5.667,90,    
                            11,                              
                            4.186,   
                            1.5,0.05,0.05,0.4,5,6,   
                            2,1000,1000,200*10**-6,30,20,Biodict,0.05,'no3',  
                            0.5,
                            1.9,0.38,           
                            0.95,0.95, 
                            0.15,
                            0.05,0.3,'yes',elemental_contents)

     #Replace  resultsnov by resultsjuly for july
    #plt.plot([a/360 for a in range(0,8640)],resultsjuly[15], label=str(h))

    plt.plot([a/360 for a in range(0,8640)],resultsnov[15], label=str(h))

plt.legend(title='hconv',loc='best', ncol=2)
plt.xlabel('Time of the day, h')
plt.ylabel('kWh')
plt.title('Cooling-November')
plt.savefig('C:/Users/GF20PZ/OneDrive - Aalborg Universitet/Dokumenter/AAU/Microalgae production/Paper drafts/Figures papers/Thermo/hconvinfluence_cooling_november.png',dpi=300, bbox_inches='tight')





#Temperature evolution

plt.figure()
plt.ylim([0, 35])

for h in listh:
    resultsjuly=cultsimul.cultivation_simulation_timestep10(h,10,10,51.970,5.667,90,    
                                7,  
                                4.186,  
                                1.5,0.05,0.05,0.4,5,6,   
                                1100,1000,1000,200*10**-6,30,20,Biodict,0.05,'no3', 
                                0.5,
                                1.9,0.38,         
                                0.95,0.95, 
                                0.15,
                                0.05,0.3,'no',elemental_contents)

    
    resultsnov=cultsimul.cultivation_simulation_timestep10(h,10,10,51.970,5.667,90,    
                            11,    # Month                              
                            4.186,   
                            1.5,0.05,0.05,0.4,5,6,   
                            1100,1000,1000,200*10**-6,30,20,Biodict,0.05,'no3', 
                            0.5,
                            1.9,0.38,           
                            0.95,0.95, 
                            0.15,
                            0.05,0.3,'no',elemental_contents)


    #plt.plot([a/360 for a in range(0,8640)],resultsnov[9])

    #Replace resultsjuly  by resultsnov for november
    
    plt.plot([a/360 for a in range(0,8640)],resultsnov[9], label=str(h))


plt.legend(title='hconv',loc='best', ncol=2)
plt.xlabel('Time of the day, h')
plt.ylabel('°C')
plt.title('Temperature evolution-November, No thermoregulation at night')
#plt.savefig('C:/Users/GF20PZ/OneDrive - Aalborg Universitet/Dokumenter/AAU/Microalgae production/Paper drafts/Figures papers/Thermo/Temperature_november_1centrifuge.png',dpi=300, bbox_inches='tight')

plt.savefig('C:/Users/GF20PZ/OneDrive - Aalborg Universitet/Dokumenter/AAU/Microalgae production/Paper drafts/Figures papers/Thermo/No_thermo_at_night_november.png',dpi=300, bbox_inches='tight')
