#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:12:57 2022

@author: caradolbear
"""
import math
import numpy as np
import matplotlib.pyplot as plt

def ParallelBracing(skew, girderamt, spanlength, gspacing, bracingperspan, bspacing, uniformity):
    '''Function to create parallel bracings on girders. 
        Inputs:
            skew (deg, float), number of girders (int), span lengths (list), girder spacing (float),
            number of bracings per span (int or list of lists), bracing spacing (int or list of lists),
            uniformit ('uniform' or 'nonuniform')'''
    
    uni = uniformity.lower()
    
    if uni == 'uniform':
        bracings = []
        sep = 0
        if skew >= 0:
            bps = bracingperspan
            bs = bspacing
            
            for i, span in enumerate(spanlength): # Iterate over span lengths
                if i > 0: # start at 0 if working with first span
                    sep = spanlength[i - 1] + sep # start at sum(previous spans) for later spans
                for b in range(bps): # Iterate over number of bracings per span
                    bracings.append([(b+1)*bs + sep, 0]) # append global location of bracing for base girder
            
            bstore = [np.array(bracings)] # store numpy array of global bracing location per girder
            
            for g in range(girderamt - 1): # noninclusive of first girder
                globalspacing = (g+1) * gspacing # total spacing from 0
                skewoffset = globalspacing * math.tan(math.radians(skew)) # parralel offset for y-location
                skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing]) # global bracing locations for skewed girder
                bstore.append(skewedgirder)
                
        if skew < 0:
            bps = bracingperspan
            bs = bspacing
            
            for i, span in enumerate(spanlength):
                if i > 0:
                    sep = spanlength[i - 1] + sep
                for b in range(bps):
                    bracings.append([(b+1)*bs + sep, gspacing*girderamt]) # y-location of base girder is maximum
           
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1) * gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing]) # subtract
                bstore.append(skewedgirder)
                
        return bstore   
        
    if uni == 'nonuniform':
        bracings = []
        bprev = 0
        if skew >= 0:
            for i, span in enumerate(spanlength): # Iterate over span lengths
                for j, bps in enumerate(bracingperspan[i]): # Iterate over bracings per span for current span length
                    for b in range(bps): # Iterate over range of bracings per span integers
                        bs = bspacing[i][j] # bracing spacing corresponds with span and bracing per span
                        bracings.append([bprev + bs, 0]) # append global bracing location based on spacing and previous bracing location
                        bprev = bprev + bs # modify bprev to current iteration
                    
            bstore = [np.array(bracings)] # store global location of bracings for base girder
            
            for g in range(girderamt - 1):
                globalspacing = (g+1) * gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
                
        if skew < 0:
            for i, span in enumerate(spanlength): 
                for j, bps in enumerate(bracingperspan[i]):
                    for b in range(bps):
                        bs = bspacing[i][j]
                        bracings.append([bprev + bs, gspacing*girderamt]) # y-location is y max
                        bprev = bprev + bs
                    
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1)*gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
        
        return bstore   


# Examples
nonuniform_test = ParallelBracing(-20, 6, [10,20,10], 5, [[5,5],[2,2,2,2],[2,2]], [[1,1],[2,3,3,2],[3,2]], 'nonuniform')
uniform_test = ParallelBracing(30, 3, [10,20,10], 10, 20, 2, 'uniform') # what happens if spans are diff lengths?

a = [uniform_test, nonuniform_test]
titles = ['Uniform Test','Nonuniform Test']

# Plot points to check
for i, b in enumerate(a): # Iterate through results
    plt.figure(i) # New figure for each bridge
    plt.title(titles[i])
    npb = np.array(b) # numpy array of result
    for d in range(len(npb[0])): # Iterate over bracing # for each girder
        bracing = npb[:,d,:] # Find parallel point locations
        xcross = []
        ycross = []
        for g in bracing: # store parallel locations in sets
            xcross.append(g[0]) 
            ycross.append(g[1])
        plt.plot(xcross,ycross,'0.6') # plot bracings
    for c in b: # Iterate over girders in result
        xset = c[:,0] # girder x values
        yset = c[:,1] # girder y values
        plt.plot(xset,yset,'k') # plot girders
        for point in c:
            x, y = point
            plt.plot(x,y,'r.') # plot bracing locations on girders
    
