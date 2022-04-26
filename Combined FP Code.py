import math
import csv

InputFileName = "Example Input File - Sheet1.csv"   #Read input csv file
InputRow = 3


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
        
        # Formats data to lists of floats/ints...
        G_number = int(G_number)
        G_span_length = FormatCorrector2(G_span_length)
        G_order = FormatCorrector(G_order)
        G_properties = FormatCorrector(G_properties)
        G_splice = FormatCorrector(G_splice)
        G_length = sum(G_span_length)
    
        
        # Data checks would go here...    
    
    
        # Create dictionary of Girder information
        # Values are either list or list of lists
        Girder_info = {"Girder Number":G_number, "Span Length": G_span_length, "Girder Length": G_length, "Cross Section Order": G_order,"Cross Section Property": G_properties, 'Splice location': G_splice}
        Bridge_info = {}
        Brace_info = {}
        
        return Girder_info, Bridge_info, Brace_info
    
    @staticmethod
    def splice_global (Girder_info, dist_x = 0, dist_y = 0):
        
        # Function to assign global coordinates of each splice
        # dist_x and dist_y are distance between each Girder
        # Creates list of lists. Each component is list of global coordinate of all splices within each girder
        # Length of output will be # of girder, # of each list inside of output is # of splices
        a = Girder_info["Splice location"]
        GLength =  Girder_info["Span Length"]
        
        splice_global = []        
        m = []
        
        for i in range(len(a)):                       
            x_start = 0
            
            if i != 0:
                x_start += GLength[i - 1]           ## Changed to start each splice at new span - AB ##
                
            for j in range (len(a[i])):
                x_start += a[i][j]
                m.append(x_start)  
        
        x_coord = m        ## Changed to be single list instead of list of lists - AB ## Currently not putting splice at Supports, would be nice to add that...
        
        m = []
        for i in range(len(a)):
            
            y_start = 0
            if i != 0:
                y_start += dist_y
            for j in range (len(a[i])):
                m.append(y_start)  
        
        y_coord = m         ## Changed to be single list instead of list of lists - AB ##

        return x_coord, y_coord
    
    @staticmethod
    def splice_dist_calc (x_coord, y_coord, Girder_num = [1,2], splice_num = [1,1]):
        
        # Calculates distance between splices based on user input
        # User defines total global x-y coordinate of all splices, Girder Number and splice number of two splices that user wants
        
        m1 = Girder_num[0]-1
        m2 = Girder_num[1]-1
        n1 = splice_num[0]-1
        n2 = splice_num[1]-1
        splice_dist = math.hypot(x_coord[m2][n2] - x_coord[m1][n1], y_coord[m2][n2] - y_coord[m1][n1])
        return splice_dist

Girder_info = system_iden.retrieve(InputFileName,InputRow)
x_coord, y_coord = system_iden.splice_global(Girder_info)                                            ## Can we put this in Girder_info?
#splice_dist = system_iden.splice_dist_calc(x_coord,y_coord)

for item in Girder_info['Cross Section Property']:
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


