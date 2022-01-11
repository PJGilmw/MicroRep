# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:46:57 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
pijo@plan.aau.dk




"""


'''
Demonstrates the behavior of the optimization algorithm for fish feed substitution.
Execute the whole script to plot for algae with 2 different compositions (cf SI I).

'''



import os
os.getcwd()
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import math
from scipy.optimize import minimize





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


    
    




''' Behaviour analysis '''


fishfeed_table = pd.read_csv("Feed_composition.csv",sep=";",header=0,encoding = 'unicode_escape', engine ='python')

#cleaning to keep what is necessary
fishfeed_table=fishfeed_table[0:8][['Ingredient','kg.kg feed-1', 'Lipid','Protein','Carb','Ash','Water']]

names_ing=list(fishfeed_table['Ingredient'])
for i in range(len(names_ing)):
    names_ing[i]=names_ing[i].replace('PBR','')






# Inputs

# optimization_for_fishfeed_substitution(fishfeed_table,lipidmicro,protmicro,carbmicro,watermicro,ashmicro,incorporation_rate, MJ_kgcarb,MJ_kgprot,MJ_kglip)

# Outputs

 # kgfeedprot, #0
 # MJfeedenergy,  #1
 # x,  #2
 # xinit1, #3
 # solution, #4
 # vect_subst, #5
 # vect_sub_nul,  #6
 # optimization_perfomance #7
 #evaluation_opti  #8
 #evaluation nul  #9
 

#ALGA1


# Influence of incorporation_rate  For Microalga biomass composition = lip : 0.2, prot : 0.5, carb : 0.25, water : 0.05, ashes 0,


collectsusbst = []  
collectsusbst_nul = []  
collectdiff = []
collectdiff_nul = []
collect_perfo = []
plt.figure(figsize=(8, 8))
incorpo_rate_range= [i/10 for i in range(1,11)]

for inc in incorpo_rate_range:   # for different incorporation rates

    res=optimization_for_fishfeed_substitution(fishfeed_table,0.2,0.5,0.25,0.05,0,inc, 15.7,23.9,36)
    
    collectsusbst.append(res[5])     # we collect the substitution vector =[subst for ingredient1,subs for ingreident 2....subst for ingredient n]
    
    collectsusbst_nul.append(res[6]) # we collect the substitution vector for the nul model=[subst for ingredient1,subs for ingreident 2....subst for ingredient n]
   
    collect_perfo.append(res[7]) # we collect the optimization performance

    collectdiff.append(res[8])  #we collect the sum of the squared differences
    
    collectdiff_nul.append(res[9])  # we collect the sum of the squared differences for the nul model


colors=[(1,0,0),(0,1,0.2),(0,0.8,0.8),(0,0.1,1),(1,0.9,0.8),(1,0,0.8),(0.1,0.5,0.1),(0.5,0.3,0.7),(0,0,0.7)]
#len(colors)

for_each_ingredient_subst = [0]*len(collectsusbst[1])

for_each_ingredient_subst_nul = [0]*len(collectsusbst[1])

for i in range(0,len(collectsusbst[1])):
    for_each_ingredient_subst[i]=[]
    for_each_ingredient_subst_nul[i]=[]
    


for inco in range(0,len(collectsusbst)):
    
    for i in range(0,len(collectsusbst[1])):
        
        for_each_ingredient_subst[i].append(collectsusbst[inco][i])
        
        for_each_ingredient_subst_nul[i].append(collectsusbst_nul[inco][i])

    
    
for ing in range(0,len(for_each_ingredient_subst)):
    
    plt.plot(incorpo_rate_range,for_each_ingredient_subst[ing],color=colors[ing],label=names_ing[ing])

    plt.plot(incorpo_rate_range,for_each_ingredient_subst_nul[ing],color=colors[ing])



plt.plot(incorpo_rate_range,collect_perfo,'*',label='Differences Optimized / Differences Proportional')    
plt.xlabel('Incorportation rate',fontsize=10)
plt.ylabel('Mass of substituted ingredient, kg', fontsize=10  )
plt.title('Alga 1')

plt.legend(fontsize=8,loc='best')
plt.savefig('Optimization_substitution_Alga 1',dpi=600)





#ALGA2

# Influence of incorporation_rate  For Microalga biomass composition = lip : 0.7, prot : 0.2, carb : 0.05, water : 0.05, ashes : 0


collectsusbst=[]  
collectsusbst_nul=[]  
collectdiff=[]
collectdiff_nul=[]
collect_perfo=[]
plt.figure(figsize=(8, 8))
incorpo_rate_range= [i/10 for i in range(1,11)]


for inc in incorpo_rate_range:   ##for different incorporation rates

    res=optimization_for_fishfeed_substitution(fishfeed_table,0.7,0.2,0.05,0.05,0,inc, 15.7,23.9,36)
    
    collectsusbst.append(res[5])     # we collect the substitution vector =[subst for ingredient1,subs for ingreident 2....subst for ingredient n]
    
    collectsusbst_nul.append(res[6]) # we collect the substitution vector for the nul model=[subst for ingredient1,subs for ingreident 2....subst for ingredient n]
   
    collect_perfo.append(res[7]) # we collect the optimization performance

    collectdiff.append(res[8])  #we collect the sum of the squared differences
    
    collectdiff_nul.append(res[9])  # we collect the sum of the squared differences for the nul model


colors=[(1,0,0),(0,1,0.2),(0,0.8,0.8),(0,0.1,1),(1,0.9,0.8),(1,0,0.8),(0.1,0.5,0.1),(0.5,0.3,0.7),(0,0,0.7)]
#len(colors)

for_each_ingredient_subst = [0]*len(collectsusbst[1])

for_each_ingredient_subst_nul = [0]*len(collectsusbst[1])

for i in range(0,len(collectsusbst[1])):
    for_each_ingredient_subst[i]=[]
    for_each_ingredient_subst_nul[i]=[]
    


for inco in range(0,len(collectsusbst)):
    
    for i in range(0,len(collectsusbst[1])):
        
        for_each_ingredient_subst[i].append(collectsusbst[inco][i])
        
        for_each_ingredient_subst_nul[i].append(collectsusbst_nul[inco][i])

    
    
for ing in range(0,len(for_each_ingredient_subst)):
    
    plt.plot(incorpo_rate_range,for_each_ingredient_subst[ing],color=colors[ing],label=names_ing[ing])

    plt.plot(incorpo_rate_range,for_each_ingredient_subst_nul[ing],color=colors[ing])



plt.plot(incorpo_rate_range,collect_perfo,'*',label='Differences Optimized / Differences Proportional')    
plt.xlabel('Incorportation rate',fontsize=10)
plt.ylabel('Mass of substituted ingredient, kg', fontsize=10  )
plt.title('Alga 2')

plt.legend(fontsize=8,loc='best')
plt.savefig('Optimization_substituion_Alga2',dpi=600)
