---
output:
  html_document: default
  word_document: default
  pdf_document: default
---
% README
 

## Content

 This repository contains an archive that must be downloaded on you machine, keeping the same folder structure.
 The files are:

+ 1 json file **_Microalgae_foreground.json_** that contains the foreground database.



+ A folder named **_climatic_data_** containing 206 csv files containing temperature and irradiance data (W.m<sup>-2</sup>)  over an average day of each month of the cultivation period in the 3 locations modeled in the simulations.   
As an example,
*dailydataforlat=57.109andlong=10.193formonth8forangle90forazimuth-90.csv_*
gives the irradiance (W) received by 1 m<sup>2</sup> of surface tilted with an angle 90$^\circ$ (vertical) and facing azimuth  90$^\circ$, for a location with coordinates 57.109,10.193 
Using the model with another location than the ones in these csvs and in the scripts would make the script download the new csvs automatically.  


+ 1 csv file **_elemental_contents.csv_** which contains  average elemental compositions (N, P, C) of microalgal macromolecules (Lipid, Phospholipids, proteins, Carbohydrates) as given 
by Geider et al. 2011.  


+ 1 csv file **_Feed_composition.csv_** containing the fish feed composition (wheat, oil etc.) and the calculated composition in term of macromolecules (Lipid, proteins, carbohydrates, ash, water).  

+ 1 R script named **_Plot_** which is used to plot the figures from the article based on the results of the simulations.  


+ 12 Python scripts for the simulations.  


The csv, the scripts and their functions'interconnections are mapped below.  
<br>  


<img src="Code map.jpg"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />  
<br>  


     

*Scripts with a 1 in their names contain functions needed for the simulations to generate the figures from the paper.*
<br>

**Retrieving_solar_and_climatic_data_1** 

Contains functions which download solar and temperature data from the European Photovoltaic Geographical System and estimate the solar power received by a given PBR geometry during the day.


**Functions_for_physical_and_biological_calculations_1**

Contains functions to calculate values related to :

+ Strain biology and metabolism
+ PBR geometry
+ Culture physical properties and centrifugation
+ Optimization for fish feed substitution


**Cultivation_simul_Night_Harvest_1**

Contains functions which simulate the cultivation over a day with solving of differential equations for temperature evolution and associated thermoregulation.

**Main_simulations_functions_1**

Contains functions which calculate the LCI for one set of primary parameters and the functions which iterate this calculation to propagate uncertainty and assess sensitivity.  


<br>
*The scripts named with a 2 can be used to observe the behaviour of some of the model's modules.*  
<br>






**Thermoregulation_Validation_Perez_Lopez_2**  

Validates the thermoregulation module by simulating thermoregulation in the same conditions as the PBR operated in Pérez-López et al. 2017. 


**Thermoregulation_behavior_2**  

Simulates the temperature evolution and thermoregulation and plots results for different primary parameters.


**Fish_feed_Optimization_behavior_2**  

Demonstrates the behaviour of the optimization algorithm for fish feed substitution.

**Geometry_and_solar_power_behavior_2**  

Demonstrates the behaviour of the module estimating the solar power received by a given PBR geometry.

**Correlation_plot_2**  

Plot the correlation heatmaps as seen in SI I.7.

<br>

*Scripts without numbers in their names are to be executed to obtain the figures from the article.*  

<br>


**Simulate** 

Launch the simulations used in the research article. ( see Reproducing results from the article )

**Prepare_project** 

Create the Brightway2 project and load the foreground database in it. Import your local version of ecoinvent 3.6 consequential in the new project and load bioshpere3.
<br>

## Reproducing results from the article


*You need :*

-Miniconda or Anaconda
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

-A local version of ecoinvent 3.6 consequential

-A python interface ( for ex. Spyder) a R interface(for ex. Rstudio)


1. **Download the zip archive and extract the folder on your machine.**


2. **Install the conda environment with all needed packages from the yml file and activate it.**

+ Open your command prompt or Anaconda/Miniconda terminal.
+ Go to the code folder in your architecture by typing :

```
 cd yourpathtocode
```
+ Then create the conda environment with all necessary packages using the yml.file

```
conda env create --file environment_microalgae.yml
```

+ Now, still in the code folder, activate the newly created environment with :

```
conda activate environment_microalgae
```



3. **Launch spyder and set up the Brigtway2 project**



+ Open spyder from the Miniconda/Anaconda terminal or command prompt by typing

```
spyder
```

+ You should see, with your own path to the code folder:

<img src="conda window 2.jpg"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />


+ In spyder, make sure the working directory is your folder or change it accordingly.

+ From spyder, open the script **Prepare_project**
Execute the whole script to prepare the Brightway2 project.



4. **Run the simulations** 

+ Open the script **_Simulate_**.
Read the instructions at the top of the file and, as indicated, choose the size of the sample for the Fourier Amplitude Sensitivity test.
A value of 1500 (1500*6 parameters = 9000 combinations and iterations)was used in the article but a lower value can be chosen for lower calculation time.


<img src="spyder 1.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
     
+ Wait for all the simulations to be finished. (Takes a few minutes to a few hours depending on the sample size and your computer)  
The script will export excel and csv files in the folder.


5. **Plot the figures based on the excel files generated**

+ Open the R script **_Plot_**. Set the working directory to your folder. 
+ Execute the whole script to plot the 3 original figures from the article and export the jpeg files in the code folder :
+ **Figure_uncertainty.jpeg**
+ **Figure_sensitivity.jpeg**
+ **Figure_contributions.jpeg**  

You may have to install a few extra packages from CRAN as indicated by the R interface.

<br>  








Geider, Richard, and Julie La Roche. 2011. Redfield Revisited : Variability of C : N : P in Marine Microalgae and Its Biochemical Basis Redfield Revisited : Variability of C : N : P in Marine Microalgae and Its Biochemical Basis.
