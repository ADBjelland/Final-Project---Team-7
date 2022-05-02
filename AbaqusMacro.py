#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 16:21:14 2022

@author: caradolbear
"""

import math
import numpy as np
import csv
from InputPreprocessor import *

InputFileName = "Final Project Input File - Sheet1.csv"   #Read input csv file
InputRow = 4

System_info = system_iden.retrieve(InputFileName,InputRow)
x_coord = system_iden.splice_local(System_info)

# Bracing Logic...
if System_info[2]['Orientation'] == 'Normal':
    bracing_xcoord, bracing_ycoord = system_iden.normal_bracing(System_info)
elif System_info[2]['Orientation'] == 'Parallel': 
    bracing_xcoord, bracing_ycoord = system_iden.parallel_bracing(System_info)

splice_coord = system_iden.splice_local(System_info)
# splice_dist = system_iden.splice_dist_calc(System_info,x_coord,y_coord)

for item in System_info[0]['Cross Section Property']:
    PList,CList = GirderSketch(item, System_info[0]['Girder Type'])