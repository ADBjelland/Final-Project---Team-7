#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:36:10 2022

@author: caradolbear
"""

def GirderSketch(xprops, xtype): # [[tf,bf,tw,dw],...], 'I'
    # assume flange width, bf, and web height, dw, are constant
    
    bf = float(xprops[0][1])
    dw = float(xprops[0][3])
    
    if xtype == 'I': # initialize I beam list
        nodepos = []
        nodeconnect = []
        
        nodepos = [[0,0],[-bf/2,0],[bf/2,0],[0,dw],[-bf/2,dw],[bf/2,dw]]
        nodeconnect = [[0,1],[0,2],[0,3],[3,4],[3,5]]
        
    
    return nodepos, nodeconnect
    
a,b = GirderSketch([[1,2,3,4]],'I')         
