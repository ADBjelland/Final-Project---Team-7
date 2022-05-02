#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:54:55 2022

@author: caradolbear
"""

import math
import numpy as np
import csv
import matplotlib.pyplot as plt

InputFileName = "Final Project Input File - Sheet1.csv"   # Read input csv file
InputRow = 4

DEBUG_Setting = 2
# 0: error handling
# 1: plotting
# 2: plotting and error handling

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
            x_end = Girder_spanpoint_x[0][-1]
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
        
        a = 0
        for i in range(len(splice_location)):
            a += len(splice_location[i])
            
        m1 = splice_num[0]-1
        m2 = splice_num[1]-1    
        
        splice_dist = x_coord[m2] - x_coord[m1]
        
        return splice_dist

System_info = system_iden.retrieve(InputFileName,InputRow)
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
    PList,CList = GirderSketch(item,'I')
    
    
## ------------- DEBUG Checks -------------

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
    
    for list_ in xsect_props:
        if len(list_) != 4:
            raise ListLengthError('Cross Section Property must be Lists of Length 4')
            
    if len(steel) != 3:
        raise ListLengthError('Steel must be List of Length 3')
        
    if len(deck) != 3:
        raise ListLengthError('Deck must be List of Length 3')
        
    if len(st_offset) != 2:
        raise ListLengthError('Stiffener Offset must be List of Length 2')
        
    if len(b_props) != 2:
        raise ListLengthError('Brace Properties must be List of Length 2')
        
    # stiffener properties are just a list in excel, but a list of 1 list in python
    # if len(st_props) != 2:
    #     raise ListLengthError('Stiffener Properties must be List of Length 2')

    # if len(su_type) != len(span_lengths):
    #     raise ListLengthError('Support Types != # of Spans')
    

    # Data Errors -----------------------------
    if g_nums != len(g_spacing) + 1:
        raise DataError('# of Girders and Girder Spacing not Compatible')
        
    splice_sum = []
    for list_ in splice_loc:
        for value in list_:
            splice_sum.append(value)
    
    if sum(span_lengths) <= sum(splice_sum):
        raise DataError('Splice Locations > Girder Length')
    
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
    
    title = 'Bridge Layout: {} Spacing, {}'.format(Orientation, Uniformity)
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

if DEBUG_Setting == 2:
    DEBUG_DataErrors(System_info)
    DEBUG_Plotting(bracing_xcoord, bracing_ycoord, System_info)
if DEBUG_Setting == 1:
    DEBUG_Plotting(bracing_xcoord, bracing_ycoord, System_info)
if DEBUG_Setting == 0:
    DEBUG_DataErrors(System_info)
