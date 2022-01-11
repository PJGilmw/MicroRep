# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:50:12 2021

@author: Pierre Jouannais, Department of Planning, DCEA, Aalborg University
pijo@plan.aau.dk

Run once to load the Brightway2 project which contains the foreground database.

"""

import bw2data
import bw2io
from bw2data.parameters import *
import brightway2 as bw



# Load project

bw2io.restore_project_directory('brightway2-project-Microalgae_1-backup.01-December-2021-12-35AM.tar.gz')

