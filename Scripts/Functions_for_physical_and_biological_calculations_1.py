# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:46:57 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
pijo@plan.aau.dk




"""


'''
Script containing the functions needed to calculate the physical and biological 
variables required during the cultivation simulation and the LCA.

'''

from scipy.optimize import minimize
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import os

# Set working directory to file location 
# (works only when executing the whole file and not only sections (Run Current cell))

currentfolder=os.path.dirname(os.path.realpath(__file__))
os.chdir(currentfolder)


###
# Execute the import to run the functions individually if needed

# elemental_contents = pd.read_csv(
#                    "../Data/elemental_contents.csv", sep=";",
#                     header=0, encoding='unicode_escape',
#                     engine='python')
# elemental_contents = elemental_contents.iloc[:, 1:]
###





#########
# Strain composition and metabolism
###########


def biomasscompo(lipid_af_dw,
                 ash_dw,
                 water_after_drying,
                phospholipid_fraction,
                 elemental_contents):
    """Returns the macronutrient and elemental biomass composition for :
        the ash-free dry weight (ashfree dw) , total dry weight (dw),
        and once the biomass is harvested and dried, with remaining water (dbio).

    #Inputs:

        #lipid_af_dw: lipid content of the ash-free, dry biomass ; g.g ashfree dw -1
        #ash_dw: ash content in dry biomass ; g.g-1 dw
        #water_after_drying: remaining water in dried biomass ; g.g dbio -1
        #phospholipid_fraction: share of phospholipds among lipids ; g.g lipids-1
        #elemental_contents: table containing the elemental composition of 
                             each macronutrient ; g.g macronutrient-1

    #Outputs:

        #prot_af_dw:  protein content ash-free dw ; g.g ashfree dw -1
        #carb_af_dw: carbohydrate content ash-free dw ; g.g ashfree dw-1
        #C_af_dw: C content ash-free dw ; g.g ashfree dw-1
        #N_af_dw: N content ash-free dw ; g.g ashfree dw-1
        #P_af_dw: P content ash-free dw ; g.g ashfree dw-1
        #K_af_dw: K content ash-free dw ; g.g ashfree dw-1
        #Mg_af_dw: Mg content ash-free dw ; g.g ashfree dw-1
        #S_af_dw: S content ash-free dw ; g.g ashfree dw-1

        #lip_dw: lipid content  dw ; g.g dw -1
        #prot_dw: protein content dw ; g.g dw -1
        #carb_dw: carb content dw ; g.g dw -1

        #C_dw: C content dw ; g.g dw -1
        #N_dw: N content dw ; g.g dw -1
        #P_dw: P content dw ; g.g dw -1
        #K_dw: K content dw ; g.g dw -1
        #Mg_dw: Mg content dw ; g.g dw -1
        #S_dw: S content dw ; g.g dw -1

        #lip_dried_biomass: lipid content dried biomass ; g.g dbio -1
        #prot_dried_biomass: prot content dried biomass ;  g.g dbio -1
        #carb_dried_biomass: carb content dried biomass ; g.g dbio -1
        #ash_dried_biomass: ash content dried biomass ; g.g dbio -1
        """

    # ash-free dry weight

    prot_af_dw = (1 - lipid_af_dw)/(5/3)
    carb_af_dw = (2/3)*prot_af_dw

    # dry weight

    lip_dw = lipid_af_dw*(1 - ash_dw)
    prot_dw = prot_af_dw*(1 - ash_dw)
    carb_dw = carb_af_dw*(1 - ash_dw)

    # dried biomass (with remaining water)

    lip_dried_biomass = lip_dw*(1 - water_after_drying)
    prot_dried_biomass = prot_dw*(1 - water_after_drying)
    carb_dried_biomass = carb_dw*(1 - water_after_drying)
    ash_dried_biomass = ash_dw*(1 - water_after_drying)


    # Elemental composition

    C_lip = lipid_af_dw*(elemental_contents.iloc[1, 0]
                         * (1 -phospholipid_fraction)
                         + elemental_contents.iloc[2, 0]*phospholipid_fraction)

    C_prot = prot_af_dw * elemental_contents.iloc[0, 0]
    C_carb = carb_af_dw * elemental_contents.iloc[3, 0]

    C_af_dw = C_lip + C_prot + C_carb
    C_dw = C_af_dw*(1 - ash_dw)

    N_lip = lipid_af_dw*(elemental_contents.iloc[1, 1]*(
        1-phospholipid_fraction)+elemental_contents.iloc[2, 1]*phospholipid_fraction)

    N_prot = prot_af_dw * elemental_contents.iloc[0, 1]
    N_carb = carb_af_dw * elemental_contents.iloc[3, 1]

    N_af_dw = N_lip + N_prot + N_carb
    N_dw = N_af_dw*(1 - ash_dw)

    P_lip = lipid_af_dw*(elemental_contents.iloc[1, 2]*(
        1-phospholipid_fraction)+elemental_contents.iloc[2, 2]*phospholipid_fraction)

    P_prot = prot_af_dw * elemental_contents.iloc[0, 2]
    P_carb = carb_af_dw * elemental_contents.iloc[3, 2]

    P_af_dw = P_lip + P_prot + P_carb
    P_dw = P_af_dw*(1 - ash_dw)

    # ratioC_N = C_af_dw / N_af_dw
    # ratioN_P = N_af_dw / P_af_dw


    # Other components according to Chlorella's observed ratios

    K_af_dw = N_af_dw*0.18
    Mg_af_dw = N_af_dw*0.08
    S_af_dw = N_af_dw*0.048

    K_dw = N_dw*0.18
    Mg_dw = N_dw*0.08
    S_dw = N_dw*0.048

    return [prot_af_dw,
            carb_af_dw,
            lip_dw,
            prot_dw,
            carb_dw,
            lip_dried_biomass,
            prot_dried_biomass,
            carb_dried_biomass,
            ash_dried_biomass,
            C_af_dw,
            N_af_dw,
            P_af_dw,
            K_af_dw,
            Mg_af_dw,
            S_af_dw,
            C_dw,
            N_dw,
            P_dw,
            K_dw,
            Mg_dw,
            S_dw]


def conversion_hexose_tobiomass(lipid_af_dw, ash_dw, water_after_drying,
                               phospholipid_fraction, elemental_contents):
    """Returns the ratios of conversion from hexose to ash-free biomass dw
    based on the latter's composition.

    #Inputs:

        #lipid_af_dw: lipid content of the ash-free, dry biomass ; g.g ash free dw -1
        #ash_dw: ash content dw ; g.g dw -1
        #water_after_drying: remaining water in dried biomass ; g.g dbio -1
        #phospholipid_fraction: share of phospholipds among lipids ; g.g lip -1
        #elemental_contents: table containing the elemental composition of
                             each macronutrient ; g.g macronutrient-1

    #Outputs:

        # ratio : g ash-free dw.g hexose-1

        """

    prot_af_dw = biomasscompo(lipid_af_dw, ash_dw,
                              water_after_drying,phospholipid_fraction,
                              elemental_contents)[0]

    carb_af_dw = biomasscompo(lipid_af_dw, ash_dw,
                              water_after_drying,phospholipid_fraction,
                              elemental_contents)[1]

    ratio = 1/(1.11*carb_af_dw+1.7*prot_af_dw+2.6*lipid_af_dw)

    return ratio




def bioenergeticyield_kjhexoseperkJenergy(PAR, losspigmentantenna, quantumyield,
                                          lossvoltagejump, losstoATPNADPH,
                                          losstohexose, lossrespiration):
    """Returns the maximum theoretical amount of kJ stored as hexose per kJ
       of solar energy received

    #Inputs:

        #PAR: % of the energy received being part of the PAR ; .
        #losspigmentantenna: losses associated to the transfer of electrons
        towards the Chlorophyle ;  .
        #quantumyield: Number of photons needed to produce one moleucle of O2 ; photons/O2
        #lossvoltagejump:  losses associated to voltage jump ; .
        #losstoATPNADPH :losses associated to the conversion to ATP and NADPH ; .
        #losstohexose :losses associated to the production of hexose from ATP and NADPH ; .
        #lossrespiration :losses associated to the respiration ; .


    #Outputs:

        # kjglucose :amount of kJ stored as hexose per kJ of solar energy ; . """

    afterPAR = 1*PAR

    afterlosspigmentantenna = afterPAR*(1-losspigmentantenna)

    afterquantumyield = afterlosspigmentantenna*(8/quantumyield)

    afterlossvoltagejump = afterquantumyield*(1-lossvoltagejump)

    afterlosstoNADPHATP = afterlossvoltagejump*(1-losstoATPNADPH)

    afterlosstohexose = afterlosstoNADPHATP*(1-losstohexose)

    afterlossrespiration = afterlosstohexose*(1-lossrespiration)

    kJglucose = afterlossrespiration

    return kJglucose

###
# Consistency check

# Uncomment the two following lines to check
# Should return 376kJ  (Williams and Laurens)

# for1kjsunlight = bioenergeticyield_kjhexoseperkJenergy(0.45,0.21, 8,
#                                                        1-1267/1384,
#                                                      1-590/1267,1-469/590,
#                                                       0.20)*3908
###


def energeticyield_biomass_perkjenergy(lipid_af_dw, ash_dw, water_after_drying,
                                       PAR, losspigmentantenna, quantumyield,
                                       lossvoltagejump, losstoATPNADPH,
                                       losstohexose, lossrespiration,
                                       Nsource,phospholipid_fraction,
                                       elemental_contents):
    """Returns the maximum theoretical amount of g ash free dw produced by kj of solar energy

    #Inputs:

        #lipid_af_dw: lipid content of the ash-free, dry biomass ; g.g ash free dw -1
        #ash_dw: ash content dw ; g.g dw -1
        #water_after_drying: remaining water in dried biomass ; g.g dbio -1
        #PAR: % of the energy received being part of the PAR ; .
        #losspigmentantenna: losses associated to the transfer of electrons
        towards the Chlorophyle ;  .
        #quantumyield: Number of photons needed to produce one moleucle of O2 ; photons/O2
        #lossvoltagejump:  losses associated to voltage jump ; .
        #losstoATPNADPH :losses associated to the conversion to ATP and NADPH ; .
        #losstohexose :losses associated to the production of hexose from ATP and NADPH ; .
        #lossrespiration :losses associated to the respiration ; .
        #Nsource :Source of nitrogen ; Nitrate or Ammonium (no3 or nh3)
        #phospholipid_fraction: share of phospholipds among lipids ; g.g lip -1
        #elemental_contents: table containing the elemental composition of
                             each macronutrient ; g.g macronutrient-1

    #Outputs:

        # biomass2 :amount of ash-free dw biomass produced per kJ of solar energy

        """

    gglucose = bioenergeticyield_kjhexoseperkJenergy(
                PAR, losspigmentantenna, quantumyield, lossvoltagejump,
                losstoATPNADPH, losstohexose, lossrespiration)/15.6

    biomass = conversion_hexose_tobiomass(
                lipid_af_dw, ash_dw, water_after_drying,
               phospholipid_fraction, elemental_contents)*gglucose

    if Nsource == 'no3':
        biomass = biomass/1.25

    return biomass

###
# Consistency check
# Uncomment the following lines for check

# Should return 0.0035 for  (Williams and Laurens)

# energeticyield_biomass_perkjenergy(0.25,0,0,0.45,0.21, 8, 1-1267/1384,
#                                    1-590/1267,1-469/590, 0.20,'nh3', 0.6,
#                                        elemental_contents)
###







#################
# PBR geometry
#################



def PBR_geometry(height, tubediameter, gapbetweentubes, horizontaldistance,
                 length_of_PBRunit, width_of_PBR_unit):

    """Returns key geometrical features of the PBR.

    #Inputs:

        #height: Height of the PBR, ; m
        #tubediameter: Tube diameter  ; m
        #gapbetweentubes: Vertical gap between tubes ; m
        #horizontaldistance: Horizontal distance between stacks ; m
        #length_of_PBRunit: Length of the  PBR unit ; m
        #width_of_PBR_unit: width of the PBR unit ; m


    #Outputs:

        # facilityvolume : PBR volume per m2 ; m3
        # tubelength : total tube length per m2 ; m
        # frontalside : Total surface of the frontal side for the whole unit ; m2
        # lateralside : Total surface of the lateral side for the whole unit ; m2
        # horizontalsurface : Total horizontal surface for the whole unit ; m2
        # exchangearea : Total exchange area with air per m2 ; m2

        """

    numberofstacks_perm2 = (((width_of_PBR_unit + horizontaldistance)
                            / (tubediameter + horizontaldistance))
                            / width_of_PBR_unit)

    # number of rows per stack
    nrows = (height+gapbetweentubes)/(tubediameter+gapbetweentubes)

    horizontalsurface = (numberofstacks_perm2*tubediameter
                         * length_of_PBRunit*width_of_PBR_unit)

    frontalside = nrows*tubediameter*length_of_PBRunit

    lateralside = numberofstacks_perm2*tubediameter*height*width_of_PBR_unit

    tubelength = numberofstacks_perm2*nrows
    facilityvolume = tubelength*math.pi*(tubediameter/2)**2  # length*section
    exchangearea = tubelength*math.pi*tubediameter  # length*perimeter

    return [facilityvolume,
            tubelength,
            frontalside,
            lateralside,
            horizontalsurface,
            exchangearea]





##################
# Culture physical properties and centrifugation
##################





def mumediatemperature(temperature):  # mPa.s
    """Returns the dynamic viscosity of the cultivation medium (without algae).

    Regression using data from Petkov, G. D. (1996). See Appendix X.


    #Inputs:

        #temperature :Temperature of the medium in the PBR ; °C


    #Outputs:

        #averagemedium : Dynamic viscosity of the medium ; mPa.s


        """

    medium1 = (-0.0108*temperature + 1.1408)
    medium2 = (-0.0146*temperature + 1.3353)
    medium3 = (-0.0114*temperature + 1.3171)
    averagemedium = (medium1 + medium2 + medium3)/3

    return averagemedium



def mususpension(temperature, concentration):
    """Returns the dynamic viscosity of the suspension.

    Regression using data from Petkov, G. D. (1996). See Appendix X.


    #Inputs:

        #temperature :Temperature of the medium in the PBR ; °C
        #concentration :Biomass concentration ; g.L-1


    #Outputs:

        #visco : Dynamic viscosity of the suspension ; mPa.s


        """

    # See regression for non excreting strains
    visco = (1.507027 - 0.019466*temperature + 0.035762*concentration)

    return visco


def Centrifugationenergy_m3(rhoalgae, rhomedium, temperature,
                            dcell, harvestingflowrate):
    """Returns energy requirement to centrifuge 1m3 of suspension.


    #Inputs:

        #rhoalgae : Density of the algae cell ; kg.m-3
        #rhomedium : Density of the medium (without algae) ; kg.m-3
        #temperature : Temperature of the culture in the PBR ; °C
        #dcell : Diameter of the cell ; m
        #harvestingflowrate : Harvesting flow rate going through the centrifuge; m3.h-1


    #Outputs:

        #Eactualdisk : Energy to centrifuge 1m3 of suspension for a disk centrifuge ; kWh
        #Eactualtubularhelical : Energy to centrifuge 1m3 of suspension for a tubular or helical centrifuge ; kWh

        #Emasterdisk : Energy to centrifuge 1m3 of suspension for a
        tubular or disk centrifuge,
        for a strain with settling velocity = 0.1um.s-1 ; kWh

        #EmastertubularHelical : Energy to centrifuge 1m3 of suspension for a
        tubular or helical centrifuge,
        for a strain with settling velocity = 0.1um.s-1 ; kWh

        """

    mumedia = mumediatemperature(temperature)

    Emasterdisk = 1.447*harvestingflowrate**0.304

    EmastertubularHelical = 2.15*harvestingflowrate**0.405

    mumedia = mumediatemperature(temperature)

    settlingvelocityactual = ((rhoalgae - rhomedium)*(dcell**2)*9.81/(18*mumedia/1000))  # m.s-1

    setlvelocitiesratio = settlingvelocityactual/(0.1*10**-6)

    Qcorrected = (1/setlvelocitiesratio)*harvestingflowrate

    Eactualdisk = 1.447 * Qcorrected**0.304

    Eactualtubularhelical = 2.15 * Qcorrected**0.405

    return [Eactualdisk,
            Eactualtubularhelical,
            Emasterdisk,
            EmastertubularHelical]


def reynolds(rhosuspension, flowrate, tubediameter, mususpension_value):
    """Returns Reynolds number in a pipe.


    #Inputs:

        #rhosuspension : Density of the culture suspension ; kg.m-3
        #flowrate : Flow rate in the pipe ; m.s-1
        #tubediameter : Tube diameter ; m
        #mususpension_value : Dynamic viscosity of the suspension ; Pa.s


    #Outputs:

        #Re : Reynolds number ; .

        """
    Re = (rhosuspension*flowrate*tubediameter)/mususpension_value

    return Re


def ffactor(roughness, tubediameter, rhosuspension, flowrate, mususpension_value):
    """Returns the friction factor in a pipe.


    #Inputs:

        #roughness : Tube roughness ; m
        #tubediameter: Tube diameter  ; m  
        #rhosuspension : Density of the culture suspension ; kg.m-3
        #flowrate : Flow rate in the pipe ; m.s-1
        #tubediameter : Tube diameter ; m
        #mususpension_value : Dynamic viscosity of the suspension ; Pa.s


    #Outputs:

        #ffactor : Friction factor ; .

        """
    #  Calculating Reynolds number
    Re = (rhosuspension*flowrate*tubediameter)/mususpension_value

    # Zigrang-Sylvester Equation
    if roughness/tubediameter/3.7 - (5.02/Re)*math.log10(roughness/tubediameter/3.7 + 13/Re) > 0:
        ffactor = ((-4*math.log10((roughness/tubediameter/3.7-(5.02/Re)
                    * math.log10(roughness/tubediameter/3.7 + 13/Re))))**-1)**2

    # Haaland Equation , to avoid Math domain error that may occur.
    else:
        ffactor = (-1.8*math.log10(((roughness/tubediameter)/3.7)**1.11 + 6.9/Re))**-1
        ffactor = ffactor**2

    return ffactor


def headloss(ffactor, tubelength, tubediameter, flowrate):
    """Returns the head loss for the mixing pump.


    #Inputs:

        #ffactor : Friction factor ; .
        # tubelength : total tube length per m2 ; m
        #rhosuspension : Density of the culture suspension ; kg.m-3
        #tubediameter : Tube diameter ; m
        #flowrate : Flow rate in the pipe ; m.s-1


    #Outputs:

        #headloss : headloss for the mixing pump ; m

        """
    headloss = 2*ffactor*(tubelength/tubediameter)*((flowrate**2)/9.81)

    return headloss


def mixing_perday(rhosuspension, tubediameter, pumpefficiency,
                  flowrate, roughness, temp, biomassconcentration, tubelength):
    """Returns energy consumption for the pump to mix/circulate the
    culture over 1m2 of facility and 24h.


    #Inputs:
        #rhosuspension : Density of the culture suspension ; kg.m-3
        #tubediameter : Tube diameter ; m
        #pumpefficiency : Efficiency of the mixing/circulating pump ; .
        #flowrate : Flow rate in the pipe ; m.s-1
        #roughness : Tube roughness ; m
        #temp :  Temperature of the culture in the PBR ; °C
        #biomassconcentration :  Biomass concentration ; g.L-1
        # tubelength : total tube length per m2 ; m

    #Outputs:

        #Emixingday : Energy to mix/circulate the culture over 1m2 of
        facility and 24 hours ; MJ     (MJ.m-2.d-1)
        #ffactor1 :  Friction factor ; . (for checking)
        #headloss1 :  headloss for the mixing pump ; m (for checking)

        """

    mususpension1 = mususpension(temp, biomassconcentration)/1000  # to Pa.s

    ffactor1 = ffactor(roughness, tubediameter, rhosuspension, flowrate, mususpension1)

    headloss1 = headloss(ffactor1, tubelength, tubediameter, flowrate)

    # Volumetric flow rate ; m3.s-1
    volflowrate = flowrate*math.pi*(tubediameter/2)**2

    Emixingday = ((rhosuspension*volflowrate*9.81*headloss1
                   * 24*0.001*3.6))/pumpefficiency

    return Emixingday, ffactor1, headloss1


def pumping_per_m3(rhowater, height, pumpefficiency):
    
    """Returns energy consumption to pump 1m3 of water from a given depth.


    #Inputs:
        #rhowater : Density of water ; kg.m-3
        #height : Heigth from which the water is pumped (vertical distance or depth) ; m
        #pumpefficiency : Efficiency of the pump ; .


    #Outputs:

        #Elecwaterpumpingperm3 : Energy to pump 1m3 of water from a given depth. MJ.m-3

        """

    Elecwaterpumpingperm3 = (rhowater*9.81*height) / (pumpefficiency*10**6)

    return Elecwaterpumpingperm3




##################
# Co-product substitution
##################


def optimization_for_fishfeed_substitution(fishfeed_table, lipidmicro,
                                           protmicro, carbmicro, watermicro,
                                           ashmicro, incorporation_rate,
                                           MJ_kgcarb, MJ_kgprot, MJ_kglip):
    """Returns the substitution entailed by 1 kg of a given dried milcroalgal biomass :
    Model1 : If the biomass enters the market for feed energy and feed protein
    Model2 :If the biomass is directly integrated into fish feed. (Model2)

    For Model2 ,the function performs an optimization under constraint
    to find the fish feed recipe which is the closest to the reference one once
    the microalgal biomass is integrated.



    #Inputs:

        #fishfeed_table : Table containing the composition of the reference
        fish feed recipe and the macronutrient profile of each ingredient ;

        #lipidmicro : share of lipid in the dried microalgal biomass ; .
        #protmicro : share of proteins in the dried microalgal biomass ; .
        #carbmicro : share of carbohydrate in the dried microalgal biomass ; .
        #watermicro : share of water in the dried microalgal biomass ; .
        #ashmicro : share of ash in the dried microalgal biomass ; .
        #incorporation_rate :Share of microalgal biomass integrated in 1 kg of fish feed; .
        #MJ_kgcarb : Energetical content of microalgal cabrohydrates ; MJ.kg-1
        #MJ_kgprot : Energetical content microalgal proteins ; MJ.kg-1
        #MJ_kglip : Energetical content microalgal lipids ; MJ.kg-1

    #Outputs:

        #kgfeedprot : Substituted kilos on the market "feed protein" ; kg (Model1)
        #MJfeedenergy : Substituted MJ  on the market "feed energy" ; kg (Model2)
        #x : Vector containing the shares of each ingredient in the new
        optimized fish feed recipe (except microalgae) ; kg

        #xinit1 : Vector containing the shares of each ingredient in the
        new fish feed recipe (except microalgae) calculated with model null (proportional)  ; kg 

        #solution : Complete result of scipy.minimize

        #vect_subst : Vector containing the mass of each fish feed ingredient
        which is substituted by the incorporation of 1 kg of microalgae  using
        an optimized recipe

        #vect_sub_nul : Vector containing the mass of each fish feed ingredient
        which is substituted by the incorporation of 1 kg of microalgae using
        an the recipe from the model null (proportional)

        #optimization_performance : Evaluation of the performance of the
        optimization :  ratio between the squared differences in the optimized
        model divided by the ones in the null model (evaluation_opti/evaluation/nul)
        
        #evaluation_opti : sum of the squared differences in the optimized
        model.
        
        #evaluation_nul :  sum of the squared differences in the null
        model.

        """

    # Lip,prot,carb,ashes,water
    microcompo = (lipidmicro, protmicro, carbmicro, ashmicro, watermicro)

    """ Model 1 """
    kgfeedprot = protmicro

    # only lipids and carbohydrates are sold on the market for feed energy
    MJfeedenergy = MJ_kgcarb*carbmicro+MJ_kglip*lipidmicro

    """ Model 2 """

    #############
    # 1)Calculation incumbent nutritional profile
    #############

    # Multiplying each ingredien's mass by its associated nutrient content
    incumbent_lipid = sum(
        fishfeed_table['kg.kg feed-1']*fishfeed_table['Lipid'])

    incumbent_prot = sum(
        fishfeed_table['kg.kg feed-1']*fishfeed_table['Protein'])

    incumbent_carb = sum(fishfeed_table['kg.kg feed-1']*fishfeed_table['Carb'])

    incumbent_ash = sum(fishfeed_table['kg.kg feed-1']*fishfeed_table['Ash'])

    incumbent_water = sum(
        fishfeed_table['kg.kg feed-1']*fishfeed_table['Water'])


    # Fish feed standard macronutrient profile Lip,prot,carb,ashes,water
    incumbentvect = [incumbent_lipid, incumbent_prot,
                     incumbent_carb, incumbent_ash, incumbent_water]

    #############
    # 2)Optimization problem with the incorporation of microalgae
    #############


    # Initial guess to initialize the algorithm

    incumbentcomposition = list(fishfeed_table['kg.kg feed-1'])
    xinit = incumbentcomposition  # kg.kg-1

    # The initial guess corresponds to the null model in which the
    # incorporation of microalgal biomass is done by a proportional decrease
    # of the share oh each ingredient in the fish feed.

    xinit1 = [x*(1 - incorporation_rate) for x in xinit]  # proportional incorporation

    # Collecting the nutrient profile of each of the fish feed ingredients

    ingredientscomposition = []
    for i in range(len(fishfeed_table)):
        ingredientscomposition.append((fishfeed_table.loc[i, 'Lipid'],
                                       fishfeed_table.loc[i, 'Protein'],
                                       fishfeed_table.loc[i, 'Carb'],
                                       fishfeed_table.loc[i, 'Ash'],
                                       fishfeed_table.loc[i, 'Water']))

    # Object function definition : the function that needs to be minimized
    # We want to minimize the sum of the squared differences between the
    # incumbent feed composition and the new one after microalgae
    # incorporation, for each nutrient.

    def functionobje(x):
        """Returns the sum of the squared differences in content for each nutrient
        between the reference fish feed composition and the one after
        microalgal biomass incorporation.

        #Inputs:

            #x : vector containing the share of each ingredient in a fish feed
            (except microalgae)

        #Outputs:

            #functionobj : sum of the squared differences in content for
            each nutrient between the reference fish feed composition
            and the one in input.
            """

        functionobj = 0  # Initialization
        for biochem in range(0, 5):  # for each nutrient Lip,prot,carb,ashes,water

            diff = (incumbentvect[biochem]
                    - (sum([xi*content[biochem] for (xi, content) in
                            zip(x, ingredientscomposition)])
                    + incorporation_rate*microcompo[biochem]))  # Incumbent - New
            
            functionobj += diff**2  # squared difference

        return(functionobj)

    # Sum of squared differences for the null model
    # (evaluation)
    evaluation_nul = functionobje(xinit1)

    def constraint1(x):
        """Defines the constraint for the optimization problem
        The sum of all ingredients' shares should equal 1.

        #Inputs:

            #x : vector containing the share of each ingredient in a fish feed
            without the microalgal biomass
        #Outputs:

            Returns the sum of the shares - 1 (Should equal 0)
            """
        return sum(x) + incorporation_rate - 1


    # Defining the boundaries for each ingredient's share (except microalgae) : 
    # The share can vary between 0 and 1-incorporation rate and
    # is the same for each ingredient

    b = (0, 1 - incorporation_rate)
    bnds = (b, b, b, b, b, b, b, b)

    # Define our first constraint as an equation,
    # "constraint1" of x must be equal to 0
    con1 = {'type': 'eq', 'fun': constraint1}
    cons = ([con1])

    # Calling the optimization algorithm (scipy)
    solution = minimize(functionobje, xinit1, method='SLSQP',
                        bounds=bnds, constraints=cons)

    # The optimized vector with the new fish feed compostion
    # after microalgae incorporation
    x = solution.x
    # Sum of squared differences for the optimized fish feed composition
    # (evaluation)
    evaluation_opti = solution.fun

    # The optimization performance is defined as the ratio between
    # the squared differences in the optimized model divided by the ones in the null model
    # The lower, the better

    optimization_performance = evaluation_opti/evaluation_nul



    # 3) Calculating the substitution induced by
    # incoporation of 1 kg of microalgal biomass

    # vect_subst contains the mass of each fish feed ingredient
    # substituted by the incorporation of 1 kg of microalgal biomass with
    # a given incorporation rate

    vect_subst = (x-incumbentcomposition)/incorporation_rate

    # compared to the substitution if for model null proportional

    vect_sub_nul = (np.array(xinit1)-incumbentcomposition)/incorporation_rate

    return [kgfeedprot,
            MJfeedenergy,
            x,
            xinit1,
            solution,
            vect_subst,
            vect_sub_nul,
            optimization_performance,
            evaluation_opti,
            evaluation_nul]

