import math
import numpy as np
import csv

InputFileName = "Final Project Input File - Sheet1.csv"   #Read input csv file
InputRow = 4

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
if System_info[2]['Orientation'] == 'Normal':
    bracing_xcoord, bracing_ycoord = system_iden.normal_bracing(System_info)
elif System_info[2]['Orientation'] == 'Parallel': 
    bracing_xcoord, bracing_ycoord = system_iden.parallel_bracing(System_info)

splice_coord = system_iden.splice_local(System_info)
# splice_dist = system_iden.splice_dist_calc(System_info,x_coord,y_coord)

for item in System_info[0]['Cross Section Property']:
    PList,CList = GirderSketch(item, System_info[0]['Girder Type'])

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

## --- Defining Stiffener + Brace Sketch --- ##
def StiffenerBraceSketch(GSpacing, System_info, ii):
    
    SProp = System_info[2]['Stiffner Properties']
    CSProp = System_info[0]['Cross Section Property']
    Offset = System_info[2]['Stiffner Offset']
    Type = System_info[2]['Type']
    
    bs = SProp[0][1]
    dw = CSProp[0][3]
    x, y = Offset
    
    PartName = 'Stiffener - ' + str(ii)
    
    # Construct the stiffeners...
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.setPrimaryObject(option=STANDALONE)
        
    s.rectangle(point1=(0.0, 0.0), point2=(bs, dw))
    s.rectangle(point1=(GSpacing - bs, 0.0), point2=(GSpacing, dw))
    
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
    p.BaseShell(sketch=s)
    
    s.unsetPrimaryObject()
    
    # PLocation = [Offset[1], dw - Offset[1], Offset[0], GSpacing - Offset[0]]
    # jj = 2
    # for i in range(0,4):
    #     DatumPartitionS(PLocation[i], jj, PartName)           
    #     jj += 2
    
    mdb.models['Model-1'].parts[PartName].setValues(space=THREE_D, type=DEFORMABLE_BODY)
    
    # Construct the braces...
    PartName = 'Brace - ' + str(ii)
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
        
    PointList = [[Offset[0],Offset[1]],[GSpacing - Offset[0], Offset[1]],[GSpacing - Offset[0],dw - Offset[1]],[Offset[0], dw - Offset[1]],[GSpacing/2, Offset[1]]]
    V = []
    for i in range(0,5):
        V.append((PointList[i][0], PointList[i][1],0))

    if Type == 'X':
        p.WirePolyLine(points=((V[0], V[1]), (V[1], V[3]), (V[3], V[2]), (V[2], V[0])), mergeType=SEPARATE, meshable=ON)
        
    elif Type == 'L':
        p.WirePolyLine(points=((V[0], V[1]),(V[2], V[3])), mergeType=SEPARATE, meshable=ON)
        
    elif Type == 'K':
        p.WirePolyLine(points=((V[0], V[4]), (V[4], V[3]), (V[3], V[2]), (V[2], V[4]), (V[4], V[1])), mergeType=SEPARATE, meshable=ON)
        
    mdb.models['Model-1'].parts[PartName].setValues(space=THREE_D, type=DEFORMABLE_BODY)
    return

def StiffenerBraceSketch2(GSpacing, System_info, ii):
    
    SProp = System_info[2]['Stiffner Properties']
    CSProp = System_info[0]['Cross Section Property']
    Offset = System_info[2]['Stiffner Offset']
    Type = System_info[2]['Type']
    Skew = System_info[1]['Skew']
    
    bs = SProp[0][1]
    dw = CSProp[0][3]
    x, y = Offset
    
    PartName = 'Stiffener - ' + str(ii)
    
    # Construct the stiffeners...
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.setPrimaryObject(option=STANDALONE)
        
    s.rectangle(point1=(0.0, 0.0), point2=(bs, dw))
    
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
    p.BaseShell(sketch=s)
    
    s.unsetPrimaryObject()
        
    mdb.models['Model-1'].parts[PartName].setValues(space=THREE_D, type=DEFORMABLE_BODY)
    
    # Construct the braces...
    PartName = 'Brace - ' + str(ii)
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=THREE_D, type=DEFORMABLE_BODY)
    
    SkewOffset = GSpacing*math.tan(Skew*math.pi/180.0)
    
    PointList = [[Offset[0],Offset[1]],[GSpacing - Offset[0], Offset[1]],[GSpacing - Offset[0],dw - Offset[1]],[Offset[0], dw - Offset[1]],[GSpacing/2, Offset[1]]]
    
    V = []
    for jj in range(0,5):
        if jj in [1,2]:
            V.append((PointList[jj][0], PointList[jj][1],SkewOffset))
        elif jj == 4:
            V.append((PointList[jj][0], PointList[jj][1],SkewOffset/2))
        else:
            V.append((PointList[jj][0], PointList[jj][1],0))

    if Type == 'X':
        p.WirePolyLine(points=((V[0], V[1]), (V[1], V[3]), (V[3], V[2]), (V[2], V[0])), mergeType=SEPARATE, meshable=ON)
        
    elif Type == 'L':
        p.WirePolyLine(points=((V[0], V[1]),(V[2], V[3])), mergeType=SEPARATE, meshable=ON)
        
    elif Type == 'K':
        p.WirePolyLine(points=((V[0], V[4]), (V[4], V[3]), (V[3], V[2]), (V[2], V[4]), (V[4], V[1])), mergeType=SEPARATE, meshable=ON)
        
    mdb.models['Model-1'].parts[PartName].setValues(space=THREE_D, type=DEFORMABLE_BODY)
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

def DatumPartitionS(PLocation, ii, PartName):
    ## --- Defining a datum --- ###
    p = mdb.models['Model-1'].parts[PartName]
    
    if ii == 2 or ii == 4:
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=PLocation)
    else:
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=PLocation)
    
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

## --- Section Assignments --- ##
def BridgeMaterial():
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((29000.0, 0.3), ))
    return

def CreateBridgeSections(CProp, SProp, BProp):
    mdb.models['Model-1'].GeneralizedProfile(name='Strut', area=10.0, 
    i11=10.0, i12=10.0, i22=10.0, j=1.0, gammaO=0.0, gammaW=0.0)
    
    mdb.models['Model-1'].BeamSection(name='Truss', 
    integration=BEFORE_ANALYSIS, poissonRatio=0.3, beamShape=CONSTANT, 
    profile='Strut', thermalExpansion=OFF, temperatureDependency=OFF, 
    dependencies=0, table=((29000.0, 11500.0), ), alphaDamping=0.0, 
    betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
    shearCenter=(0.0, 0.0), consistentMassMatrix=False)
    
    ii = 1
    for Prop in CProp:
        WebName = 'Web - ' + str(ii)
        FlangeName = 'Flange - ' + str(ii)
        
        mdb.models['Model-1'].HomogeneousShellSection(name=WebName, preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=Prop[0], 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    
        mdb.models['Model-1'].HomogeneousShellSection(name=FlangeName, preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=Prop[2], 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
        
        ii += 1
        
    mdb.models['Model-1'].HomogeneousShellSection(name='Stiffener', 
    preIntegrate=OFF, material='Steel', thicknessType=UNIFORM, 
    thickness=SProp[0], thicknessField='', nodalThicknessField='', 
    idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=5)
    return

def BeamAssignment(System_info, splice_coord, PartName):
    p = mdb.models['Model-1'].parts[PartName]
    f = p.faces   
    
    CSProp = System_info[0]['Cross Section Property'][0]
    CSO = System_info[0]['Cross Section Order']
    CSO = [item for sublist in CSO for item in sublist]
    GL = System_info[0]['Girder Length']
    
    TotalCoord = splice_coord[0]

    for ii in range(1,len(TotalCoord)):
        ID = int(CSO[ii - 1])
        
        # Top Flange Assignment
        SectionName = 'Flange - ' + str(ID)
        Selection = f.getByBoundingBox(-CSProp[1]/2, CSProp[3], TotalCoord[ii - 1], CSProp[1]/2, CSProp[3], TotalCoord[ii])
        region = regionToolset.Region(faces=Selection)
        p.SectionAssignment(region=region, sectionName=SectionName, offset=0.0, 
            offsetType=TOP_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        
        # Web Assignment       
        SectionName = 'Web - ' + str(ID)
        Selection = f.findAt(((0.0, CSProp[3]/2, (TotalCoord[ii] + TotalCoord[ii - 1])/2),))
        region = regionToolset.Region(faces=Selection)
        p.SectionAssignment(region=region, sectionName=SectionName, offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        
        # Bottom Flange Assignment       
        SectionName = 'Flange - ' + str(ID)
        Selection = f.getByBoundingBox(-CSProp[1]/2, 0, TotalCoord[ii - 1], CSProp[1]/2, 0, TotalCoord[ii])
        region = regionToolset.Region(faces=Selection)
        p.SectionAssignment(region=region, sectionName=SectionName, offset=0.0, 
            offsetType=TOP_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        
        ii += 1
    
    return

def BracingAssignment(SPartName, BPartName, SSectionName, BSectionName):
    p = mdb.models['Model-1'].parts[SPartName]
    f = p.faces
    region = p.Set(faces=f, name=SSectionName)
    p.SectionAssignment(region=region, sectionName=SSectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    
    p = mdb.models['Model-1'].parts[BPartName]
    e = p.edges
    region = p.Set(edges=e, name=BSectionName)
    
    p.SectionAssignment(region=region, sectionName=BSectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0,-1.0))
    
    return

## --- Component Assembly --- ##

def BraceAssembly(ii):
    a = mdb.models['Model-1'].rootAssembly
    
    PartName = 'Brace - ' + str(ii)
    INameB = PartName
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=INameB, part=p, dependent=ON)

    PartName = 'Stiffener - ' + str(ii)
    INameS = PartName
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=INameS, part=p, dependent=ON)
    
    AName = 'Brace System - ' + str(ii)
    a.InstanceFromBooleanMerge(name=AName, instances=(
        a.instances[INameB], a.instances[INameS], ), 
        originalInstances=DELETE, domain=GEOMETRY)
    
    del a.features[AName + str(-1)]
    
    p = mdb.models['Model-1'].parts[AName]
    region = p.sets['Truss']
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0,-1.0))
    
    return

def BraceAssembly2(ii, System_info):
    
    Skew = System_info[1]['Skew']
    GSpacing = System_info[0]['Girder Spacing'][ii - 1]
    Offset = System_info[2]['Stiffner Offset']
    SProp = System_info[2]['Stiffner Properties'][0]
    
    SkewOffset = GSpacing*math.tan(Skew*math.pi/180.0)
    V = [GSpacing - SProp[1],0,SkewOffset]
    
    a = mdb.models['Model-1'].rootAssembly
    
    PartName = 'Brace - ' + str(ii)
    INameB = PartName
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=INameB, part=p, dependent=ON)

    PartName = 'Stiffener - ' + str(ii)
    INameS1 = PartName + '1'
    INameS2 = PartName + '2'
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=INameS1, part=p, dependent=ON)
    a.Instance(name=INameS2, part=p, dependent=ON)
    a.translate(instanceList=(INameS2, ), vector=V)
    
    AName = 'Brace System - ' + str(ii)
    a.InstanceFromBooleanMerge(name=AName, instances=(
        a.instances[INameB], a.instances[INameS1], a.instances[INameS2], ), 
        originalInstances=DELETE, domain=GEOMETRY)
    
    del a.features[AName + str(-1)]
    
    p = mdb.models['Model-1'].parts[AName]
    region = p.sets['Truss']
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0,-1.0))
    
    return

def SystemAssembly(GLocation, BCoord, System_info):
    nGirders = System_info[0]['Girder Number']
    
    a = mdb.models['Model-1'].rootAssembly
    
    ii = 1
    for item in GLocation:
        PartName = 'Girder - 1'
        IName = PartName + ' - ' + str(ii)
        
        p = mdb.models['Model-1'].parts[PartName]
        a.Instance(name=IName, part=p, dependent=ON)
        a.translate(instanceList=(IName, ), vector=GLocation[ii - 1])
        ii += 1
    
    ii = 0
    for CoordList in reversed(BCoord):
        ii += 1
        jj = 1
        for ZCoord, XCoord in zip(CoordList[0],CoordList[1]):
            if ii == nGirders:
                return
            
            PartName = 'Brace System - ' + str(ii)
            IName = PartName + ' - ' + str(ii) + ' - ' + str(jj)
            
            V = (XCoord,0,ZCoord)

            p = mdb.models['Model-1'].parts[PartName]
            a.Instance(name=IName, part=p, dependent=ON)
            a.translate(instanceList=(IName, ), vector=V)
            jj += 1
    return

## --- Analysis Components --- ###
def Supports(System_info, GLocation):
    nGirder = System_info[0]['Girder Number']
    SLength = System_info[0]['Span Length']
    SType = System_info[3]['Support type']
    
    a = mdb.models['Model-1'].rootAssembly
    
    SGlobal = [[0,0,0]]
    Total = 0.0
    for item in SLength:
        Total = item + Total
        SGlobal.append([0, 0, Total])
    
    for ii in range(0, nGirder):
        InstanceName = 'Girder - 1 - ' + str(ii + 1)
        e = a.instances[InstanceName].edges
        
        jj = 0
        for BoundaryType in SType:

            GlobalLoc = tuple([E1 + E2 for E1, E2 in zip(GLocation[ii], SGlobal[jj])])

            Selection = e.findAt((GlobalLoc, ))
    
            region = regionToolset.Region(edges=Selection)
        
            BoundaryName = 'Support - ' + str(ii + 1) + ' - ' + str(jj + 1)
            if BoundaryType == 0:
                mdb.models['Model-1'].DisplacementBC(name=BoundaryName, createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            else:
                mdb.models['Model-1'].DisplacementBC(name=BoundaryName, createStepName='Initial', region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            jj += 1
    return

def Mesh(System_info):
    nGirder = System_info[0]['Girder Number']
    
    # Mesh Girders
    PartName = 'Girder - 1'
    p = mdb.models['Model-1'].parts['Girder - 1']
    p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    
    a = mdb.models['Model-1'].rootAssembly
    # Mesh Bracing System
    for ii in range(1, nGirder):
        PartName = 'Brace System - ' + str(ii)
        p = mdb.models['Model-1'].parts[PartName]
                
        region = p.sets['Truss'].edges
        
        p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
        
        p.seedEdgeByNumber(edges=region, number=1, constraint=FINER)
        elemType1 = mesh.ElemType(elemCode=T3D2, elemLibrary=STANDARD)
        p.setElementType(regions=p.sets['Truss'], elemTypes=(elemType1, ))
        
        p.generateMesh()
    
    return

##### --- Main Abaqus Code --- #####
ModelName = 'Model-1'

# Create Girder Part...
ii = 1
CrossSection = System_info[0]['Cross Section Property'][0]
s = mdb.models[ModelName].ConstrainedSketch(name='__profile__',sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
PList,CList = GirderSketch(CrossSection,'I')
IBeamSketch(s, PList, CList)
PartBeamExtrude(ii, System_info[0]['Girder Length'])

# Breakup Girder Geometry by Partitions...
ii = 2
jj = 1
for item in splice_coord[0][1:-1]:
    DatumPartition(item, ii, jj)
    ii += 2

CrossSection = System_info[0]['Cross Section Property']
BridgeMaterial()
CreateBridgeSections(CrossSection,SProp,BProp)

# Assign Girder Sections
PartName = 'Girder - 1'
BeamAssignment(System_info, splice_coord, PartName)

# Create Braces...
ii = 1
for GSpacing in System_info[0]['Girder Spacing']:
    if System_info[2]['Orientation'] == 'Parallel':
        StiffenerBraceSketch2(GSpacing, System_info, ii)
    else:
        StiffenerBraceSketch(GSpacing, System_info, ii)
    ii += 1
nBraces = ii

# Assemble Bracing...
for ii in range(1,nBraces):
    SPartName = 'Stiffener - ' + str(ii)
    SSectionName = 'Stiffener'
    BPartName = 'Brace - ' + str(ii)
    BSectionName = 'Truss'
    BracingAssignment(SPartName, BPartName, SSectionName, BSectionName)
    if System_info[2]['Orientation'] == 'Parallel':
        BraceAssembly2(ii, System_info)
    else:
        BraceAssembly(ii)

# Assemble System ...
# Determine Location of Girders...
GLocation = [(0,0,0)]
ii = 0
Skew = System_info[1]["Skew"]
for GSpacing in System_info[0]["Girder Spacing"]:
    Pos = (GSpacing + GLocation[ii][0], 0, (GSpacing + GLocation[ii][0])*math.tan(Skew*math.pi/180.0))
    GLocation.append(Pos)
    ii += 1
    
BCoord = list(zip(bracing_xcoord,bracing_ycoord))
SystemAssembly(GLocation, BCoord, System_info)

# Assign Girder Supports
Supports(System_info, GLocation)
Mesh(System_info)

# Assign Output Parameters...
mdb.models['Model-1'].StaticStep(name='LC_1', previous='Initial')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'U'))
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(frequency=LAST_INCREMENT)

# Assign Job for Analysis...
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB)
