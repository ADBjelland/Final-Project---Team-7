#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 16:22:20 2022

@author: caradolbear
"""

import math
import numpy as np
import csv
import matplotlib.pyplot as plt
from InputPreprocessor import *

InputFileName = "Final Project Input File - Sheet1.csv"   #Read input csv file
InputRow = 5
DEBUG_Setting = 2
# 0: error handling
# 1: plotting
# 2: plotting and error handling

class DataTypeError(Exception): 
    pass

class UnacceptedEntry(Exception): 
    def __init__(self, entry, accepted_entry, message):
        self.entry = entry
        self.accepted_entry = accepted_entry
        self.message = message
    def __str__(self):
        errormessage = self.message + ': {} is not in {}'.format(self.entry, self.accepted_entry)
        return errormessage
    
class ListLengthError(Exception): 
    pass
class DataError(Exception): 
    pass

def DEBUG_DataErrors(System_info):
    # All System_info data
    Girder_info = System_info[0]
    g_nums = Girder_info['Girder Number']
    span_lengths = Girder_info['Span Length']
    xsect_order = Girder_info['Cross Section Order']
    xsect_props = Girder_info['Cross Section Property']
    splice_loc = Girder_info['Splice Location']
    g_spacing = Girder_info['Girder Spacing']
    g_type = Girder_info['Girder Type']
    
    Bridge_info = System_info[1]
    skew = Bridge_info['Skew']
    steel = Bridge_info['Steel Property']
    deck = Bridge_info['Deck']
    
    Bracing_info = System_info[2]
    b_config = Bracing_info['Bracing Configuration']
    b_nums = Bracing_info['Number of Bracing']
    b_spacing = Bracing_info['Bracing Spacing']
    b_orientation = Bracing_info['Orientation']
    b_type = Bracing_info['Type']
    st_offset = Bracing_info['Stiffner Offset']
    b_props = Bracing_info['Brace Properties']
    st_props = Bracing_info['Stiffner Properties']
    
    Support_info = System_info[3]
    buffer = Support_info['Support Buffer']
    su_type = Support_info['Support type']
    
    # Accepted String Inputs
    accepted_g_type = ['I']
    accepted_b_config = ['Uniform','Nonuniform']
    accepted_b_orientation = ['Parallel','Normal']
    accepted_b_type = ['X','K','L']
    
    # Data Types -------------------------------
    if type(g_nums) is not int:
        raise DataTypeError('Girder Number must be Int')
    
    if type(span_lengths) is not list:
        raise DataTypeError('Span Lengths must be List')
        
    if type(xsect_order) is not list or type(xsect_order[0]) is not list:
        raise DataTypeError('Cross Section Order must be List of Lists')
    
    if type(xsect_props) is not list or type(xsect_props[0]) is not list:
        raise DataTypeError('Cross Section Property must be List of Lists')
        
    if type(splice_loc) is not list or type(splice_loc[0]) is not list:
        raise DataTypeError('Splice Location must be List of Lists')
        
    if type(g_spacing) is not list:
        raise DataTypeError('Girder Spacing must be List')
        
    if type(g_type) is not str:
        raise DataTypeError('Girder Type must be Str')
        
    if type(skew) is not float:
        raise DataTypeError('Skew must be Float')
    
    if type(steel) is not list:
        raise DataTypeError('Steel must be List')
    
    if type(deck) is not list:
        raise DataTypeError('Deck must be List')
        
    if type(b_config) is not str:
        raise DataTypeError('Bracing Configuration must be Str')
        
    if b_config == 'Uniform':
        if type(b_nums) is not int:
            raise DataTypeError('Uniform Number of Bracing must be Int')
    
    if b_config == 'Nonuniform':   
        if b_orientation == 'Normal':
            if type(b_nums) is not list:
                raise DataTypeError('Nonuniform/Normal Number of Bracing must be List')
        if b_orientation == 'Parallel':
            if type(b_nums) is not list and type(b_nums[0]) is not list:
                raise DataTypeError('Nonuniform/Parallel Number of Bracing must be List of Lists')
    
    if b_config == 'Uniform':
        if type(b_spacing) is not list:
            raise DataTypeError('Uniform Bracing Spacing must be List')
    
    if b_config == 'Nonuniform':   
        if b_orientation == 'Normal':
            if type(b_spacing) is not list:
                raise DataTypeError('Nonuniform/Normal Bracing Spacing must be List')
        if b_orientation == 'Parallel':
            if type(b_spacing) is not list and type(b_spacing[0]) is not list:
                raise DataTypeError('Nonuniform/Parallel Bracing Spacing must be List of Lists')
    
    if type(b_orientation) is not str:
        raise DataTypeError('Bracing Orientation must be Str')
        
    if type(b_type) is not str:
        raise DataTypeError('Bracing Type must be Str')
        
    if type(st_offset) is not list:
        raise DataTypeError('Stiffener Offset must be List')
        
    if type(b_props) is not list:
        raise DataTypeError('Brace Properties must be List')
        
    if type(st_props) is not list:
        raise DataTypeError('Stiffener Properties must be List')
        
    if type(buffer) is not float:
        raise DataTypeError('Support Buffer must be Float')
        
    if type(su_type) is not list:
        raise DataTypeError('Support Type must be List')
    
    
    # Accepted String Inputs -------------------
    if g_type not in accepted_g_type:
        raise UnacceptedEntry(g_type, accepted_g_type,'Girder Type')
        
    if b_config not in accepted_b_config:
        raise UnacceptedEntry(b_config, accepted_b_config, 'Bracing Configuration')
    
    if b_orientation not in accepted_b_orientation:
        raise UnacceptedEntry(b_orientation, accepted_b_orientation, 'Bracing Orientation')
    
    if b_type not in accepted_b_type:
        raise UnacceptedEntry(b_type, accepted_b_type, 'Bracing Type')
    
    # Related/Required List Lengths ----------------------
    if len(span_lengths) != len(xsect_order):
        raise ListLengthError('List Length Error: Cross Section Order != # of Spans')
    
    # if len(span_lengths) != len(xsect_props):
    #     raise ListLengthError('Cross Section Property != # of Spans')
    
    if len(span_lengths) != len(splice_loc):
        raise ListLengthError('Splice Location != # of Spans')
    
    if b_orientation == 'Parallel' and b_config == 'Nonuniform': 
        if len(span_lengths) != len(b_nums):
            raise ListLengthError('Number of Bracing (Parallel/Nonuniform) != # of Spans')
        
        if len(span_lengths) != len(b_spacing):
            raise ListLengthError('Bracing Spacing (Parallel/Nonuniform) != # of Spans')

    if b_orientation == 'Normal' and b_config == 'Nonuniform':
        if len(b_nums[0]) != len(b_spacing[0]):
            raise ListLengthError('(Normal/Nonuniform) Number of Bracing != Bracing Spacing')
            
    if b_config == 'Uniform' and len(b_spacing) != 1:
        raise ListLengthError('(Uniform) More than one Bracing Spacing Provided')
    
    for list_ in xsect_props:
        if len(list_) != 4:
            raise ListLengthError('Cross Section Property must be Lists of Length 4')
            
    if len(steel) != 4:
        raise ListLengthError('Steel must be List of Length 4')
        
    if len(deck) != 5:
        raise ListLengthError('Deck must be List of Length 5')
        
    if len(st_offset) != 2:
        raise ListLengthError('Stiffener Offset must be List of Length 2')
        
    if len(b_props) != 2:
        raise ListLengthError('Brace Properties must be List of Length 2')
        
    # stiffener properties are just a list in excel, but a list of 1 list in python
    # if len(st_props) != 2:
    #     raise ListLengthError('Stiffener Properties must be List of Length 2')

    if len(su_type) != len(span_lengths) + 1:
         raise ListLengthError('Support Types != # of Spans')

    # Data Errors -----------------------------
    if g_nums != len(g_spacing) + 1:
        raise DataError('# of Girders and Girder Spacing not Compatible')

    for i, span in enumerate(span_lengths):
        if span <= sum(splice_loc[i]):
            raise DataError('Splice Locations > Girder Length in Span {}'.format(i+1))
    
    if b_orientation == 'Parallel':
        if type(b_nums) is list:
            if type(b_nums[0]) is list:
                fix_b = b_nums.copy()
                b_nums = []
                for list_ in fix_b:
                    for value in list_:
                        b_nums.append(value)
        if type(b_spacing) is list:          
            if type(b_spacing[0]) is list:
                fix_b = b_spacing.copy()
                b_spacing = []
                for list_ in fix_b:
                    for value in list_:
                        b_spacing.append(value)
    
    b_product = np.array(b_nums)*np.array(b_spacing)
    
    if sum(span_lengths) <= sum(b_product):
        raise DataError('Bracing Length > Girder Length') 
        
    for value in su_type:
        if value != float(0) and value != float(1):
            raise DataError('Support Type must be 1 (pin) or 0 (roller)')
    

def DEBUG_Plotting(bracing_xcoord, bracing_ycoord, System_info):
    Orientation = System_info[2]['Orientation']
    Uniformity = System_info[2]['Bracing Configuration']
    Span_length = System_info[0]['Span Length']
    girder_length = sum(Span_length)
    Skew = System_info[1]['Skew']
    Girder_spacing = System_info[0]['Girder Spacing']
    
    title = 'Bridge Layout: {} Spacing, {}'.format(Uniformity, Orientation)
    plt.figure()
    plt.title(title)
    
    gxi = 0
    gxf = girder_length
    globalspacing = 0
    skewoffset = 0
    gx = np.array([gxi + skewoffset, gxf + skewoffset])
    gy = np.array([globalspacing, globalspacing])
    plt.plot(gx,gy,'k')
    for girder, gs in enumerate(Girder_spacing):
        globalspacing = globalspacing + gs
        skewoffset = globalspacing * math.tan(math.radians(Skew))
        gx = np.array([gxi + skewoffset, gxf + skewoffset])
        gy = np.array([globalspacing, globalspacing])
        plt.plot(gx,gy,'k')
    
    gyi = 0
    gymax = sum(Girder_spacing)
    gxi_skewed = gxi + gymax * math.tan(math.radians(Skew))
    gxf_skewed = gxf + gymax * math.tan(math.radians(Skew))
    grightx = np.array([gxi, gxi_skewed])
    grighty = np.array([gyi, gymax])
    gleftx = np.array([gxf, gxf_skewed])
    glefty = np.array([gyi, gymax])
    plt.plot(grightx,grighty,'k')
    plt.plot(gleftx,glefty,'k')
    
    if Orientation == 'Normal':
        normal_dict = {}   
        for girder, xpoints in enumerate(bracing_xcoord):
            for xpoint in xpoints:
                normal_dict[xpoint] = []
        for girder, xpoints in enumerate(bracing_xcoord):
            for i, xpoint in enumerate(xpoints):
                normal_dict[xpoint].append(bracing_ycoord[girder][i])

        for x, yvalues in normal_dict.items():
            Ys = []
            Xs = []
            for y in yvalues:
                Ys.append(y)
                Xs.append(x)
            plt.plot(Xs,Ys,'0.6')
        for x, yvalues in normal_dict.items():
            for y in yvalues:
                plt.plot(x,y,'r.')
    
    if Orientation == 'Parallel':
        a = []
        for i, xset in enumerate(bracing_xcoord):
            XY = np.zeros([len(xset),2])
            XY[:,0] = bracing_xcoord[i]
            XY[:,1] = bracing_ycoord[i]
            a.append(XY)
        # Plot bracings
        for bracing_num in range(len(a[0])):
            npa = np.array(a)
            bracing = npa[:, bracing_num, :]
            xcross = []
            ycross = []
            for g in bracing:
                xcross.append(g[0])
                ycross.append(g[1])
            plt.plot(xcross,ycross,'0.6') # plot bracings
        
        # Plot girders
        for k, girder in enumerate(a):
            xcross = []
            ycross = []
            for i, row in enumerate(girder):
                xcross.append(girder[i,0])
                ycross.append(girder[i,1])
                plt.plot(xcross,ycross,'k') # plot girders
        
        # Plot points
        for k, girder in enumerate(a):
            for i, row in enumerate(girder):
                for point in row:
                    x, y = row
                    plt.plot(x,y,'r.') # plot bracing locations on girders
                    
System_info = system_iden.retrieve(InputFileName,InputRow)

if DEBUG_Setting == 0 or DEBUG_Setting == 2:
    DEBUG_DataErrors(System_info)

x_coord = system_iden.splice_local(System_info)

# Bracing Logic...
# normal bracing for uniform generates point on end of girder
if System_info[2]['Orientation'] == 'Normal':
    bracing_xcoord, bracing_ycoord = system_iden.normal_bracing(System_info)
elif System_info[2]['Orientation'] == 'Parallel': 
    bracing_xcoord, bracing_ycoord = system_iden.parallel_bracing(System_info)

splice_coord = system_iden.splice_local(System_info)
# splice_dist = system_iden.splice_dist_calc(System_info,x_coord,y_coord)

for item in System_info[0]['Cross Section Property']:
    PList,CList = GirderSketch(item, System_info[0]['Girder Type'])
    
    
## ------------- DEBUG Checks -------------

if DEBUG_Setting == 2:
    DEBUG_Plotting(bracing_xcoord, bracing_ycoord, System_info)
    DEBUG_DataErrors(System_info)
if DEBUG_Setting == 1:
    DEBUG_Plotting(bracing_xcoord, bracing_ycoord, System_info)
if DEBUG_Setting == 0:
    DEBUG_DataErrors(System_info)
