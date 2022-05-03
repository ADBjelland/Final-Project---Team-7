#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 16:12:08 2022

@author: caradolbear
"""

import math
import numpy as np
import csv

def GirderSketch(xprops, xtype): # [[tf,bf,tw,dw],...], 'I'
    # assume flange width, bf, and web height, dw, are constant
    
    bf = xprops[1]
    dw = xprops[3]
    
    if xtype == 'I': # initialize I beam list
        nodepos = []
        nodeconnect = []
        
        # node 0 in middle-bottom orientation
        nodepos = [[0,0],[-bf/2,0],[bf/2,0],[0,dw],[-bf/2,dw],[bf/2,dw]]
        nodeconnect = [[0,1],[0,2],[0,3],[4,3],[3,5]]
        
    return nodepos, nodeconnect

def FormatCorrector(ListofLists):
    # Formats string of list of lists to proper float counterpart.
    ListofLists = ListofLists[1:-1].split(';')
        
    ii = 0
    for item in ListofLists:
        item = item.replace('[','')
        item = item.replace(']','')
        ListofLists[ii] = item.split(',')            
        ii += 1
        
    ListofLists = [[float(x) for x  in sublist] for sublist in ListofLists]
    return (ListofLists)

def FormatCorrector2(List):
    # Formats string of list to proper float counterpart.
    List = List[1:-1].split(',')
    List = [float(x) for x in List]
    
    return (List)

class system_iden:
        
    @staticmethod
    def retrieve(filename, i = 3):       #Asks for filename, Bridge Number as inputs
        
        DATA = []
        
        # Grabs data only from one row in the csv...
        with open(filename) as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            next(csv_reader)
            for row in csv_reader:
                if csv_reader.line_num == i:
                    DATA.append(list(row))   
                    
        Bridge_ID = DATA[0][0]
        print('Reading the following bridge:', Bridge_ID)  
        G_number = DATA[0][1]         # Girder Number
        G_span_length = DATA[0][2]    # Girder span length
        G_order = DATA[0][3]          # Girder section order
        G_properties = DATA[0][4]     # Cross section dimension
        G_splice = DATA[0][5]         # Location of splice
        G_spacing = DATA[0][6]
        G_type = DATA[0][7]
        
        # Formats data to lists of floats/ints...
        G_number = int(G_number)
        G_span_length = FormatCorrector2(G_span_length)
        G_order = FormatCorrector(G_order)
        G_properties = FormatCorrector(G_properties)
        G_splice = FormatCorrector(G_splice)
        G_length = sum(G_span_length)
        G_spacing = FormatCorrector2(G_spacing)
    
        # Create dictionary of Girder information
        # Values are either list or list of lists
        Girder_info = {"Girder Number":G_number, "Span Length": G_span_length, "Girder Length": G_length, "Cross Section Order": G_order,"Cross Section Property": G_properties, 'Splice Location': G_splice, "Girder Spacing" : G_spacing, "Girder Type": G_type}
        
        Bridge_skew = DATA[0][8]
        Steel_prop = DATA[0][9]
        Deck = DATA[0][10]
        
        
        Bridge_skew = float(Bridge_skew)
        Steel_prop = FormatCorrector2(Steel_prop)
        Deck = FormatCorrector2(Deck)
        Bridge_info = {"Skew" : Bridge_skew,"Steel Property": Steel_prop, "Deck": Deck}
        
        Bracing_config = DATA[0][11]
        Bracing_number = DATA[0][12]
        Bracing_spacing = DATA[0][13]
        Bracing_orient = DATA[0][14]
        Bracing_type = DATA[0][15]
        Stiff_offset = DATA[0][16]
        Bracing_prop = DATA[0][17]
        Stiff_prop = DATA[0][18]
        
        if Bracing_config == "Uniform" :
            Bracing_number = int(Bracing_number)
        if Bracing_config == "Nonuniform":    
            if Bracing_type == "Normal":
                Bracing_number = FormatCorrector2(Bracing_number)
            else:
                Bracing_number = FormatCorrector(Bracing_number)
        
        if Bracing_config == "Uniform":
            Bracing_spacing = FormatCorrector2(Bracing_spacing)
        if Bracing_config == "Nonuniform":    
            if Bracing_type == "Normal":
                Bracing_spacing = FormatCorrector2(Bracing_spacing)
            else:
                Bracing_spacing = FormatCorrector(Bracing_spacing)    
        
        Stiff_offset = FormatCorrector2(Stiff_offset)
        Bracing_prop = FormatCorrector2(Bracing_prop)
        Stiff_prop = FormatCorrector(Stiff_prop)
        
        Brace_info = {"Bracing Configuration" : Bracing_config, "Number of Bracing":Bracing_number,"Bracing Spacing": Bracing_spacing, "Orientation": Bracing_orient, "Type": Bracing_type, "Stiffner Offset": Stiff_offset, "Brace Properties":Bracing_prop, "Stiffner Properties":Stiff_prop}
        
        Support_buffer = DATA[0][19]
        Support_type = DATA[0][20]
        
        Support_buffer = float(Support_buffer)
        Support_type = FormatCorrector2(Support_type)
       
        
        Support_info = {"Support Buffer": Support_buffer, "Support type": Support_type}
        
        
        return Girder_info, Bridge_info, Brace_info,Support_info
        
    @staticmethod
    def splice_local (System_info):
        
        # Function to assign global coordinates of each splice
        # dist_x and dist_y are distance between each Girder
        # Creates list of lists. Each component is list of global coordinate of all splices within each girder
        # Length of output will be # of girder, # of each list inside of output is # of splices
        
        a = System_info[0]["Splice Location"]
        GLength =  System_info[0]["Span Length"]
        Girder_num = System_info[0]["Girder Number"]
        Girder_spacing = System_info[0]["Girder Spacing"]
        span_length = System_info[0]["Span Length"]
        Girder_length = sum(span_length)
        
        skew = System_info[1]["Skew"]
        
        m = []
        ii = 0
        for List in a:

            if ii == 0:
                x_sum = 0
            else:
                x_sum = sum(span_length[0:ii])
            
            m.append(x_sum)
            
            ii += 1
            
            for Item in List:
            
                x_sum += Item
                m.append(x_sum)
        
        m.append(sum(span_length[0:ii]))
        x_coord = m
        
        n = []
        y_start = 0
        for i in range(len(x_coord)):
            n.append(y_start)  
        
        y_coord = n

        return x_coord, y_coord
    
    @staticmethod
    def normal_bracing (System_info):   #Will return 
        
        Girder_info = System_info[0]
        Girder_length = sum(Girder_info["Span Length"])
        span_length = Girder_info["Span Length"]
        Girder_num = Girder_info["Girder Number"]
        Girder_spacing = Girder_info["Girder Spacing"]
        
        bridge_info = System_info [1]
        skew = bridge_info["Skew"]
        
        bracing_info = System_info [2]
        bracing_config = bracing_info["Bracing Configuration"]
        bracing_number = bracing_info["Number of Bracing"]
        bracing_spacing = bracing_info ["Bracing Spacing"]
        
        Support_info = System_info[3]
        buffer_length = Support_info["Support Buffer"]

        x_start = 0
        y_start = 0 
        

        Girder_spanpoint_x = []
        Girder_spanpoint_y = []
        
        i = 0 
        while i < Girder_num:
            x_start = 0.0
            y_start = 0.0
            m = []
            n = []
            
            x_start = x_start + ((sum(Girder_spacing[i:]))*(math.tan(skew*math.pi/180)))
            y_start = y_start + sum(Girder_spacing[i:])
            m.append(x_start)
            n.append(y_start)
           
            for j in range(len(span_length)):
                m.append(x_start + span_length[j])
            x_end = x_start + Girder_length
            y_end = y_start
            
            m.append(x_end)
            n.append(y_end)
            
            Girder_spanpoint_x.append(m)
            Girder_spanpoint_y.append(n)
            i += 1
        
        x_grid = []
        y_grid = []
        bracing_xcoord = []
        bracing_ycoord = []
        
        
        # return Girder_endpoint_x, Girder_endpoint_y
        if bracing_config == "Uniform":
            
            x_grid_point= 0
            x_end = Girder_spanpoint_x[1][-1]
            y_end = Girder_spanpoint_y[0][-1]
            
            d = bracing_spacing[0]
            
            while x_grid_point < x_end:
                if x_grid_point + d < x_end:
                    x_grid_point += d
                    x_grid.append(x_grid_point)
                else:
                    break
            i = 0
            for L in Girder_spanpoint_x:
                m = []
                n = []
                for k in x_grid:
                    if k >= L[0] and k <= L[-1]:
                        m.append(k)
                        n.append(Girder_spanpoint_y[i][0])
                        
                i+=1
                bracing_xcoord.append(m)
                bracing_ycoord.append(n)
            
            check_buffer = []
            for L in Girder_spanpoint_x:
                for k in range(len(L)):
                    check_buffer.append(L[k] - buffer_length)
                    check_buffer.append(L[k] + buffer_length)
            
            for i in range(len(bracing_xcoord)):
                for j in bracing_xcoord[i]:
                    if j in check_buffer:
                        bracing_xcoord[i].remove(j)
                        bracing_ycoord[i].pop(0)
                
            return bracing_xcoord, bracing_ycoord
              
        if bracing_config == "Nonuniform":    
            
            bracing_number = bracing_info["Number of Bracing"][0]
            bracing_spacing = bracing_info ["Bracing Spacing"][0]
            
            x_end = Girder_spanpoint_x[1][-1]
            y_end = Girder_spanpoint_y[0][-1]
            
            x_grid_point = 0
            c = []
            z = 0
                
            
            for i in range(len(bracing_number)):  
                
                d = bracing_spacing[i]
                k = 0
                if i == 0:
                    while k < int(bracing_number[i]):
                        if x_grid_point + d < x_end:
                            x_grid_point += d
                            x_grid.append(x_grid_point)
                        k+=1
                else:
                    while k < int(bracing_number[i]):
                        if x_grid_point + d < x_end:
                            x_grid_point += d
                            x_grid.append(x_grid_point)
                            k+=1
                        else:
                            break
                
            
            i = 0
            for L in Girder_spanpoint_x:
                m = []
                n = []
                for k in x_grid:
                    if k >= L[0] and k <= L[-1]:
                        m.append(k)
                        n.append(Girder_spanpoint_y[i][0])
                i += 1
                bracing_xcoord.append(m)
                bracing_ycoord.append(n)
            
            return bracing_xcoord, bracing_ycoord
        
    @staticmethod    
    def parallel_bracing(System_info):
        '''Function to create parallel bracings on girders. 
            Inputs:
                skew (deg, float), number of girders (int), span lengths (list), girder spacing (list of floats),
                number of bracings per span (int or list of lists), bracing spacing (int or list of lists),
                uniformit ('uniform' or 'nonuniform')'''
        
        Girder_info = System_info[0]
        Bridge_info = System_info[1]
        Bracing_info = System_info[2]
        
        skew = Bridge_info['Skew']
        girderamt = Girder_info['Girder Number']
        spanlength = Girder_info['Span Length']
        gspacing = Girder_info['Girder Spacing']
        bracingperspan = Bracing_info['Number of Bracing']
        bspacing = Bracing_info['Bracing Spacing']
        uniformity = Bracing_info['Bracing Configuration']
        
        
        uni = uniformity.lower()
        
        if uni == 'uniform':
            bracings = []
            sep = 0
            if skew >= 0:
                bs = bspacing[0]
                
                for i, span in enumerate(spanlength): # Iterate over span lengths
                    if i > 0: # start at 0 if working with first span
                        sep = spanlength[i - 1] + sep # start at sum(previous spans) for later spans
                    bps = math.floor(span/bs)
                    if i == len(spanlength) - 1:
                        bps = math.floor(span/bs) - 1
                    for b in range(int(bps)): # Iterate over number of bracings per span
                        bracings.append([(b+1)*bs + sep, 0]) # append global location of bracing for base girder
                
                bstore = [np.array(bracings)] # store numpy array of global bracing location per girder
                
                globalspacing = 0
                for g, gs in enumerate(gspacing): # noninclusive of first girder
                    globalspacing = globalspacing + gs # total spacing from 0
                    skewoffset = globalspacing * math.tan(math.radians(skew)) # parralel offset for y-location
                    skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing]) # global bracing locations for skewed girder
                    bstore.append(skewedgirder)
                    
            if skew < 0:
                bs = bspacing[0]
                
                for i, span in enumerate(spanlength):
                    if i > 0:
                        sep = spanlength[i - 1] + sep
                    bps = math.floor(span/bs)
                    if i == len(spanlength) - 1:
                        bps = math.floor(span/bs) - 1
                    for b in range(int(bps)):
                        bracings.append([(b+1)*bs + sep, gspacing*girderamt]) # y-location of base girder is maximum
               
                bstore = [np.array(bracings)]
                
                globalspacing = 0
                for g, gs in enumerate(gspacing): # noninclusive of first girder
                    globalspacing = globalspacing + gs # total spacing from 0
                    skewoffset = globalspacing * math.tan(math.radians(skew))
                    skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing]) # subtract
                    bstore.append(skewedgirder)
            
        if uni == 'nonuniform':
            bracings = []
            bprev = 0
            if skew >= 0:
                for i, span in enumerate(spanlength): # Iterate over span lengths
                    for j, bps in enumerate(bracingperspan[i]): # Iterate over bracings per span for current span length
                        bps = int(bps)
                        for b in range(int(bps)): # Iterate over range of bracings per span integers
                            bs = bspacing[i][j] # bracing spacing corresponds with span and bracing per span
                            bracings.append([bprev + bs, 0]) # append global bracing location based on spacing and previous bracing location
                            bprev = bprev + bs # modify bprev to current iteration
                        
                bstore = [np.array(bracings)] # store global location of bracings for base girder
                
                globalspacing = 0
                for g, gs in enumerate(gspacing): # noninclusive of first girder
                    globalspacing = globalspacing + gs # total spacing from 0
                    skewoffset = globalspacing * math.tan(math.radians(skew)) # parralel offset for y-location
                    skewedgirder = np.array(bracings) + np.array([skewoffset, globalspacing]) # global bracing locations for skewed girder
                    bstore.append(skewedgirder)
                    
            if skew < 0:
                for i, span in enumerate(spanlength): 
                    for j, bps in enumerate(bracingperspan[i]):
                        bps = int(bps)
                        for b in range(int(bps)):
                            bs = bspacing[i][j]
                            bracings.append([bprev + bs, gspacing*girderamt]) # y-location is y max
                            bprev = bprev + bs
                        
                bstore = [np.array(bracings)]
                
                globalspacing = 0
                for g, gs in enumerate(gspacing): # noninclusive of first girder
                    globalspacing = globalspacing + gs # total spacing from 0
                    skewoffset = globalspacing * math.tan(math.radians(skew))
                    skewedgirder = np.array(bracings) - np.array([skewoffset, globalspacing]) # subtract
                    bstore.append(skewedgirder)
        
        # Convert to list of lists of x and y coordinates
        bracing_xcoord = []
        bracing_ycoord= []
        for girder in bstore:
            bracing_xcoord.append(girder[:,0].tolist())
            bracing_ycoord.append(girder[:,1].tolist())
        
        return bracing_xcoord, bracing_ycoord  
        
    @staticmethod
    def splice_dist_calc (splice_location, splice_num = [1,2]):
        
        # Calculates distance between splices based on user input
        # User defines total global x-y coordinate of all splices, Girder Number and splice number of two splices that user wants
        
        x_coord = splice_location[0]
            
        m1 = splice_num[0]-1
        m2 = splice_num[1]-1    
        
        splice_dist = x_coord[m2] - x_coord[m1]
        
        return splice_dist