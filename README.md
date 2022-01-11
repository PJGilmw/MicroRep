## Code documentation for the MicroRep repository

### Overview of the repository

This repository contains  code used to reproduce the results of the manuscript: _A stochastic LCA model of upscaling microalgal molecule productions_ 
 
Overview of folders and files:

**Data**

+ **_elemental_contents.csv_** includes average elemental compositions (N, P, C) of microalgal macromolecules (Lipid, Phospholipids, proteins, Carbohydrates) as given 
by Geider et al. 2011.  


+ **_Feed_composition.csv_** includes the fish feed composition (wheat, oil etc.) and the calculated composition in term of macromolecules (Lipid, proteins, carbohydrates, ash, water).  

+ **_Microalgae_foreground.json_** includes the foreground database.


**Climatic_data**

+ This folder contains 206 .csv files with temperature and irradiance data (W.m<sup>-2</sup>) over an average day of each month of the cultivation period in the three locations modeled in the simulations. As an example,
*dailydataforlat=57.109andlong=10.193formonth8forangle90forazimuth-90.csv_*
gives the irradiance (W) received by 1 m<sup>2</sup> of surface tilted with an angle 90$^\circ$ (vertical) and facing azimuth  90$^\circ$, for a location with coordinates 57.109,10.193 
Using the model with another location than the ones in these csvs and in the scripts would make the script download the new csvs automatically.  


**Plot**

All plots from the scripts are saved in this folder.

+ **_Plot.R_** R script to plot the figures from the article based on the results of the simulations.  

**Environment**

+ **environment_microalgae.yml** file needed to create the virtual environment with all the required dependencies to run the model


**Outputs**

All outputs of csv and xlsx types are saved in this folder.

**Scripts**

+ Twelve **.py** files: python scripts including the model itself and needed to run the simulations. 

Files, scripts, and their functions'interconnections are mapped below.  
<br>  

<img src="Code map.jpg"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />  

<br>  

### Model functions

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


### Behavior of specific model modules

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

### Figures in the article

*Scripts without numbers in their names are to be executed to obtain the figures from the article.*  

<br>


**Simulate** 

Launch the simulations used in the research article. (see Reproducing results from the article )
All figures are exported to folder "Plot".

**Prepare_project** 

Create the Brightway2 project and load the foreground database in it. Import your local version of ecoinvent 3.6 consequential in the new project and load bioshpere3.
<br>

### Reproducing results from the article

*Requirements*

+ Miniconda or Anaconda
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

+ A local version of the ecoinvent 3.6 consequential database

+ A python interface (e.g., Spyder) and a R interface (e.g., Rstudio)

*Step by step procedure:*

1. **Download or clone a local copy of the repository. Keep the folders structure.**

2. **Prepare a conda environment with all needed packages**

+ From terminal or Anaconda/Miniconda terminal access the directory where the repository code has been downloaded:

```
 cd yourpathtothefolder"Environment"
```

+ Create the conda environment with all necessary packages using the .yml file

```
conda env create --file environment_microalgae.yml
```

+ Activate the newly created environment:

```
conda activate environment_microalgae
```

3. **Set up the Brigtway2 project**

+ Open the script **Prepare_project.py** in a text editor or python interface and change the ecoinvent directory to match the directory where the ecoinvent files are on your drive. 

+ From the python interface or from command line (```python Prepare_project.py```) execute the whole script to prepare the Brightway2 project.

4. **Run the simulations using the model** 

+ Open the script **Simulate.py**. Read the instructions at the top of the file and, as indicated, change the value of the variable ```Size_sample``` to choose the size of the sample for the Fourier Amplitude Sensitivity test. A value of ```Size_sample = 1500``` (1500*6 parameters = 9000 combinations and iterations) was used in the article but a lower value can be chosen for lower calculation time.

+ From the python interface or from command line (```python Simulate.py```) execute the whole script to run the simulation. 

+ Wait for all the simulations to be finished (Takes a few minutes to a few hours depending on the sample size and your computer). The script will export excel and csv files in the folder "Outputs".

5. **Plot the figures based on the excel files generated**

+ Open the R script **_Plot_**. Set the working directory to your folder. 
+ Execute the whole script to plot the 3 original figures from the article and export the jpeg files in the  folder "Plot" :
+ **Figure_uncertainty.jpeg**
+ **Figure_sensitivity.jpeg**
+ **Figure_contributions.jpeg**  

You may have to install a few extra packages from CRAN as indicated by the R interface.

<br>  


REFERENCES

Geider, R. & La Roche, J. Redfield revisited: variability of C:N:P in marine microalgae and its biochemical basis, European Journal of Phycology, 37:1, 1-17, (2002)

Perez-Lopez, P. et al. Comparative life cycle assessment of real pilot reactors for microalgae cultivation in different seasons. Appl. Energy 205, 1151-1164 (2017)
