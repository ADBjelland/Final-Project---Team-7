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
        #Bridge_info = {}
        #Brace_info = {}
        
        return Girder_info #, Bridge_info, Brace_info
    
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

## --- Defining Stiffener + Brace Sketch --- ##
def StiffenerBraceSketch(SProp,CSProp, GSpacing, Offset, Type, ii):
    bs = SProp[1]
    dw = CSProp[3]
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
    
    PLocation = [Offset[1], dw - Offset[1], Offset[0], GSpacing - Offset[0]]
    
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
        V.append((PointList[i][0],PointList[i][1],0))

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
    
    PartName = 'Brace - 1'
    IName = PartName
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=IName, part=p, dependent=ON)

    PartName = 'Stiffener - 1'
    IName = PartName
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=IName, part=p, dependent=ON)
    
    a.InstanceFromBooleanMerge(name='Brace System - 1', instances=(
        a.instances['Brace - 1'], a.instances['Stiffener - 1'], ), 
        originalInstances=DELETE, domain=GEOMETRY)
    
    del a.features['Brace System - 1-1']
    
    return

def SystemAssembly(nGriders, nBraces, GLocation, BLocation):
    a = mdb.models['Model-1'].rootAssembly
    for ii in range(1, nGirders + 1):
        PartName = 'Girder - 1'
        IName = PartName + ' - ' + str(ii)
        
        p = mdb.models['Model-1'].parts[PartName]
        a.Instance(name=IName, part=p, dependent=ON)
        a.translate(instanceList=(IName, ), vector=GLocation[ii - 1])

    for ii in range(1, nBraces + 1):
        PartName = 'Brace System - 1'
        IName = PartName + ' - ' + str(ii)
        
        p = mdb.models['Model-1'].parts[PartName]
        a.Instance(name=IName, part=p, dependent=ON)
        a.translate(instanceList=(IName, ), vector=BLocation[ii - 1])
        
    return

ModelName = 'Model-1'

ii = 1
CrossSection = Girder_info['Cross Section Property'][0]
s = mdb.models[ModelName].ConstrainedSketch(name='__profile__',sheetSize=200.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
PList,CList = GirderSketch(CrossSection,'I')
IBeamSketch(s, PList, CList)
PartBeamExtrude(ii, Girder_info['Girder Length'])

ii = 1
for item in Girder_info['Cross Section Property']:
    ii += 1

ii = 2
jj = 1
for item in x_coord:    
    DatumPartition(item, ii, jj)
    ii += 2

SProp = (0.5,2)
CSProp = (1,1,1,6)
GSpacing = 20
Offset = (2,1)
Type = 'K'
ii = 1
StiffenerBraceSketch(SProp,CSProp, GSpacing, Offset, Type, ii)

BProp = ()

CrossSection = Girder_info['Cross Section Property']
BridgeMaterial()
CreateBridgeSections(CrossSection,SProp,BProp)

nGirders = 3
nBraces = 3
GLocation = [(0,0,0),(20,0,0),(40,0,0)]
BLocation = [(0,0,10),(0,0,20),(0,0,40)]

SPartName = 'Stiffener - 1'
SSectionName = 'Stiffener'
BPartName = 'Brace - 1'
BSectionName = 'Truss'
BracingAssignment(SPartName, BPartName, SSectionName, BSectionName)

ii = 1
BraceAssembly(ii)
SystemAssembly(nGirders, nBraces, GLocation, BLocation)
