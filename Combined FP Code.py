#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 14:14:19 2022

@author: inrae
"""


import math
import csv

InputFileName = "Final Project Input File - Sheet1.csv"   #Read input csv file
InputRow = 6


def GirderSketch(xprops, xtype): # [[tf,bf,tw,dw],...], 'I'
    # assume flange width, bf, and web height, dw, are constant
    
    bf = xprops[1]
    dw = xprops[3]
    
    if xtype == 'I': # initialize I beam list
        nodepos = []
        nodeconnect = []
        
        # node 0 in middle-bottom orientation
        nodepos = [[0,0],[-bf/2,0],[bf/2,0],[0,dw],[-bf/2,dw],[bf/2,dw]]
        nodeconnect = [[0,1],[0,2],[0,3],[3,4],[3,5]]
        
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
    def retrieve(filename,i = 3):       #Asks for filename, Bridge Number as inputs
        
        DATA = []
        
        # Grabs data only from one row in the csv...
        with open(filename) as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            next(csv_reader)
            for row in csv_reader:
                if csv_reader.line_num == i:
                    print(csv_reader.line_num)
                    DATA.append(list(row))     
          
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
        
        # Data checks would go here...    
    
    
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
        
        Support_buffer = int(Support_buffer)
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
        
        # x = 0 
        
        # x_coord = []
        # y_coord = []
        
        # while x < Girder_num:
        #     x_start = 0.0
        #     y_start = 0.0
            
        #     x_start = x_start + ((sum(Girder_spacing[x:]))*(math.tan(skew*math.pi/180)))
        #     y_start = y_start + sum(Girder_spacing[x:])
            
           
        #     for i in range(len(a)):
        #         for j in range(len(a[i])):
        #             x_start += a[i][j]
        #             x_coord.append(x_start)
            
        #     for i in range(len(a)):
        #         for j in range(len(a[i])):
        #             y_coord.append(y_start)
        #     x += 1
        
        splice_local = []        
        m = []
        
        for i in range(len(a)):                       
            x_start = 0
            
            if i != 0:
                x_start += GLength[i - 1]           ## Changed to start each splice at new span - AB ##
                
            for j in range (len(a[i])):
                x_start += a[i][j]
                m.append(x_start)  
        
        for i in span_length:
            if i not in m:
                m.append(i)
        
        x_coord = sorted(m)        ## Changed to be single list instead of list of lists - AB ## Currently not putting splice at Supports, would be nice to add that...
        
        n = []
        y_start = 0
        for i in range(len(x_coord)):
            n.append(y_start)  
        
        y_coord = n         ## Changed to be single list instead of list of lists - AB ##

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
                    while k < int(bracing_number[i])-1:
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
system_iden.normal_bracing(System_info)                                       ## Can we put this in Girder_info?
splice_coord = system_iden.splice_local(System_info)
# splice_dist = system_iden.splice_dist_calc(System_info,x_coord,y_coord)

for item in System_info[0]['Cross Section Property']:
    PList,CList = GirderSketch(item,'I')

## --- Run Abaqus Script --- ##

# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

## --- Defining Girder Sketch --- ##
def IBeamSketch(s, PList, CList):
    s.setPrimaryObject(option=STANDALONE)
    
    for item in CList:
        x1, y1 = PList[item[0]]
        x2, y2 = PList[item[1]]
        s.Line(point1=(x1, y1),point2=(x2, y2))    
    return

## --- Defining Stiffener Sketch --- ##
def StiffenerSketch():
    s.setPrimaryObject(option=STANDALONE)
    
    return

## --- Defining Datums & Partitions --- ##
def DatumPartition(PLocation, ii, i):
    ## --- Defining a datum --- ###
    PartName = 'Girder - ' + str(i)
    p = mdb.models['Model-1'].parts[PartName]
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=PLocation)
    
    ## --- Defining a partition --- ###
    f = p.faces
    d = p.datums
    p.PartitionFaceByDatumPlane(datumPlane=d[ii], faces=f)
    return

## --- Defining Part Extrusion --- ##
def PartBeamExtrude(i, GLength):
    PartName = 'Girder - ' + str(i)
    
    ## --- Defining Part --- ##
    p = mdb.models[ModelName].Part(name=PartName, dimensionality=THREE_D,type=DEFORMABLE_BODY)
    
    ## --- Converting sketch to shell... --- ##
    p.BaseShellExtrude(sketch=s, depth=GLength)
    s.unsetPrimaryObject()
    return

## -- Defining Part Extrusion --- ##
def PartStiffenerExtrude():
    return

def PartAssembly():
    for i in range(0,nGirder):
        IBeamSketch(s, PList, CList)
        PartBeamExtrude()
    return

ModelName = 'Model-1'

ii = 1
for item in Girder_info['Cross Section Property']:
    s = mdb.models[ModelName].ConstrainedSketch(name='__profile__',sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    PList,CList = GirderSketch(item,'I')
    IBeamSketch(s, PList, CList)
    PartBeamExtrude(ii, Girder_info['Girder Length'])
    ii += 1

ii = 2
jj = 1
for item in x_coord:    
    DatumPartition(item, ii, jj)
    ii += 2
