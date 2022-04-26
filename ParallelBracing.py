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
    
    uni = uniformity.lower()
    
    if uni == 'uniform':
        bracings = []
        sep = 0
        if skew >= 0:
            bps = bracingperspan
            bs = bspacing
            
            for i, span in enumerate(spanlength):
                print(bracings)
                if i > 0:
                    sep = spanlength[i - 1] + sep
                for b in range(bps):
                    bracings.append([(b+1)*bs + sep, 0])
            
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1) * gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
                
        if skew < 0:
            bps = bracingperspan
            bs = bspacing
            
            for i, span in enumerate(spanlength):
                print(bracings)
                if i > 0:
                    sep = spanlength[i - 1] + sep
                for b in range(bps):
                    bracings.append([(b+1)*bs + sep, gspacing*girderamt])
           
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1)*gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
        return bstore   
        
    if uni == 'nonuniform':
        bracings = []
        sep = 0
        bprev = 0
        if skew >= 0:
            print(bspacing)
            for i, span in enumerate(spanlength):
                print(bracings)
                if i > 0:
                    sep = spanlength[i - 1] + sep
                for j, bps in enumerate(bracingperspan[i]):
                    print(j)
                    print(bps)
                    # for k, bp in enumerate(bps):
                    #     print(bp)
                    for b in range(bps):
                        bs = bspacing[i][j]
                        
                        bracings.append([bprev + bs, 0])
                        
                        bprev = bprev + bs
                        # print(bracings)
                    
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1) * gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
        if skew < 0:
            print(bspacing)
            for i, span in enumerate(spanlength):
                print(bracings)
                if i > 0:
                    sep = spanlength[i - 1] + sep
                for j, bps in enumerate(bracingperspan[i]):
                    print(j)
                    print(bps)
                    # for k, bp in enumerate(bps):
                    #     print(bp)
                    for b in range(bps):
                        bs = bspacing[i][j]
                        
                        bracings.append([bprev + bs, gspacing*girderamt])
                        
                        bprev = bprev + bs
                        # print(bracings)
                    
            bstore = [np.array(bracings)]
            
            for g in range(girderamt - 1):
                globalspacing = (g+1)*gspacing
                skewoffset = globalspacing * math.tan(math.radians(skew))
                skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing])
                bstore.append(skewedgirder)
        
        return bstore   


# Examples
nonuniform_test = ParallelBracing(-20, 6, [10,20,10], 5, [[5,5],[2,2,2,2],[2,2]], [[1,1],[2,3,3,2],[3,2]], 'nonuniform')
uniform_test = ParallelBracing(30, 3, [10,20,10], 10, 20, 2, 'uniform')

a = [uniform_test, nonuniform_test]

# Plot points to check
for i, b in enumerate(a):
    plt.figure(i)
    
    npb = np.array(b)
    for d in range(len(npb[0])):
        bracing = npb[:,d,:]
        xcross = []
        ycross = []
        for g in bracing:
            xcross.append(g[0]) 
            ycross.append(g[1])
        plt.plot(xcross,ycross,'0.6')
    for c in b:
        xset = c[:,0]
        yset = c[:,1]
        plt.plot(xset,yset,'k')
        for point in c:
            x, y = point
            plt.plot(x,y,'r.')
    