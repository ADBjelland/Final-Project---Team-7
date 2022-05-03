import math
import numpy as np
import csv
from InputPreprocessor import *

InputFileName = "Final Project Input File - Sheet1.csv"   #Read input csv file
WorkingDirectory = 'D://temp//'
InputRow = 6

System_info = system_iden.retrieve(InputFileName,InputRow)
x_coord = system_iden.splice_local(System_info)

# Bracing Logic...
if System_info[2]['Orientation'] == 'Normal':
    bracing_xcoord, bracing_ycoord = system_iden.normal_bracing(System_info)
elif System_info[2]['Orientation'] == 'Parallel': 
    bracing_xcoord, bracing_ycoord = system_iden.parallel_bracing(System_info)

splice_coord = system_iden.splice_local(System_info)

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
    # Create IBeam sketch from points and connectivity
    s.setPrimaryObject(option=STANDALONE)
    
    for item in CList:
        x1, y1 = PList[item[0]]
        x2, y2 = PList[item[1]]
        s.Line(point1=(x1, y1),point2=(x2, y2))    
    return

## --- Defining Deck Sketch --- ##
def DeckSketch(System_info, PartName):
    DeckInfo = System_info[1]['Deck']
    GSpacing = System_info[0]['Girder Spacing']
    GLength = System_info[0]['Girder Length']
    Skew = System_info[1]['Skew']
    
    BWidth = sum(GSpacing) + DeckInfo[4]*2
    
    # Define points for a rhombus/rectangle, connect them, and turn into part...
    CList = [(0,1), (1,2), (2,3), (3,0)]
    PList = [(0,0),(GLength,0),(GLength + BWidth*math.tan(Skew*math.pi/180.0),BWidth),(BWidth*math.tan(Skew*math.pi/180.0),BWidth)]    
    
    s = mdb.models[ModelName].ConstrainedSketch(name='__profile__',sheetSize=200.0)
    s.setPrimaryObject(option=STANDALONE)
    
    for item in CList:
        x1, y1 = PList[item[0]]
        x2, y2 = PList[item[1]]
        s.Line(point1=(x1, y1),point2=(x2, y2))
    
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=THREE_D, type=DEFORMABLE_BODY)   
    p.BaseShell(sketch=s)
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
    
    # Construct the stiffeners by sketching rectangles...
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
    
    # Construct the braces by defining and joining points...
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
    
    # Construct the stiffeners by sketching rectangles...
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

    s.setPrimaryObject(option=STANDALONE)
        
    s.rectangle(point1=(0.0, 0.0), point2=(bs, dw))
    
    p = mdb.models['Model-1'].Part(name=PartName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
    p.BaseShell(sketch=s)
    
    s.unsetPrimaryObject()
        
    mdb.models['Model-1'].parts[PartName].setValues(space=THREE_D, type=DEFORMABLE_BODY)
    
    # Construct the braces by defining and joining points...
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
def DatumPartition(PLocation, Plane, PartName, ii):
    ## --- Defining a datum --- ###
    p = mdb.models['Model-1'].parts[PartName]
    if Plane == 'XY':
        p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=PLocation)
    if Plane == 'XZ':
        p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=PLocation)
    if Plane == 'YZ':
        p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=PLocation)
    
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
def BridgeMaterial(System_info):
    SteelProp = System_info[1]['Steel Property']
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((SteelProp[1], SteelProp[0]), ))
    
    ConreteProp = System_info[1]['Deck']
    mdb.models['Model-1'].Material(name='Concrete')
    mdb.models['Model-1'].materials['Concrete'].Elastic(table=((ConreteProp[1], ConreteProp[0]), ))
    return

def CreateBridgeSections(System_info):
    CProp = System_info[0]['Cross Section Property']
    SProp = System_info[2]['Stiffner Properties'][0]
    SteelProp = System_info[1]['Steel Property']
    BProp = System_info[2]['Brace Properties']
    DProp = System_info[1]['Deck']
    
    mdb.models['Model-1'].TrussSection(area=BProp[0], material='Steel', name='Truss')
    
    # Define cross-section properties along gider
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
    
    # Define stiffener properties...
    mdb.models['Model-1'].HomogeneousShellSection(name='Stiffener', 
    preIntegrate=OFF, material='Steel', thicknessType=UNIFORM, 
    thickness=SProp[1], thicknessField='', nodalThicknessField='', 
    idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
    thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
    integrationRule=SIMPSON, numIntPts=5)
    
    # Define deck properties...
    mdb.models['Model-1'].HomogeneousShellSection(name='Deck', preIntegrate=OFF, 
    material='Concrete', thicknessType=UNIFORM, thickness=DProp[3], 
    thicknessField='', nodalThicknessField='', 
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
    
    return

def BracingAssignment(SPartName, BPartName, SSectionName, BSectionName):
    # Stiffener property assignment...
    p = mdb.models['Model-1'].parts[SPartName]
    f = p.faces
    region = p.Set(faces=f, name=SSectionName)
    p.SectionAssignment(region=region, sectionName=SSectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    
    # Strut property assignment...
    p = mdb.models['Model-1'].parts[BPartName]
    e = p.edges
    region = p.Set(edges=e, name=BSectionName)
        
    p.SectionAssignment(region=region, sectionName=BSectionName, offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)    
    return

def DeckAssignment(System_info, PartName, SectionName):
    p = mdb.models['Model-1'].parts[PartName]
    f = p.faces
    
    region = p.Set(faces=f, name=SectionName)
    p.SectionAssignment(region=region, sectionName=SectionName, offset=0.0, 
        offsetType=BOTTOM_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
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
    
    # Merge all instances of brace system.
    AName = 'Brace System - ' + str(ii)
    IList = a.instances.keys()
    a.InstanceFromBooleanMerge(name=AName, instances=([a.instances[IList[i]] for i in range(len(IList))]), mergeNodes=ALL, nodeMergingTolerance=0.1, domain=GEOMETRY, originalInstances=DELETE)
    
    del a.features[AName + str(-1)]   
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
    IList = a.instances.keys()
    a.InstanceFromBooleanMerge(name=AName, instances=([a.instances[IList[i]] for i in range(len(IList))]), mergeNodes=ALL, nodeMergingTolerance=0.1, domain=GEOMETRY, originalInstances=DELETE)
    
    del a.features[AName + str(-1)]
    
    p = mdb.models['Model-1'].parts[AName]
    region = p.sets['Truss']
    p.assignBeamSectionOrientation(region=region, method=N1_COSINES, n1=(0.0, 0.0,-1.0))
    
    return

def SuperstructureAssembly(GLocation, BCoord, System_info):
    nGirders = System_info[0]['Girder Number']    
    a = mdb.models['Model-1'].rootAssembly
    
    # Adding Girder to System...
    ii = 1
    for item in GLocation:
        PartName = 'Girder - 1'
        IName = PartName + ' - ' + str(ii)
        
        p = mdb.models['Model-1'].parts[PartName]
        a.Instance(name=IName, part=p, dependent=ON)
        a.translate(instanceList=(IName, ), vector=GLocation[ii - 1])
        ii += 1
        
    # Adding Bracing to System...
    ii = 0
    for CoordList in BCoord:
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

def BridgeAssembly(System_info):
    Skew = System_info[1]['Skew']
    DeckInfo = System_info[1]['Deck']
    CSProp = System_info[0]['Cross Section Property'][0]
    
    a = mdb.models['Model-1'].rootAssembly
   
    # Adding Deck to System...
    PartName = 'Deck'
    IName = PartName
    DLocation = (-DeckInfo[4],CSProp[3],-DeckInfo[4]*math.tan(Skew*math.pi/180.0))
    
    p = mdb.models['Model-1'].parts[PartName]
    a.Instance(name=IName, part=p, dependent=ON)
    a.rotate(instanceList=(IName, ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 1.0, 0.0), angle=-90.0)
    a.rotate(instanceList=(IName, ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0.0, 0.0, 1.0), angle=-90.0)
    a.translate(instanceList=(IName, ), vector=DLocation)
    return

## --- Analysis Components --- ###
def TieInteraction(System_info, GLocation):
    DeckInfo = System_info[1]['Deck']
    nGirder = System_info[0]['Girder Number']
    GSpacing = System_info[0]['Girder Spacing']
    GLength = System_info[0]['Girder Length']
    Skew = System_info[1]['Skew']
    CSProp = System_info[0]['Cross Section Property'][0]
    
    BWidth = sum(GSpacing) + DeckInfo[4]*2  
    
    # Connect top flange of girders to respective area along deck...
    for ii in range(nGirder):   
        a = mdb.models['Model-1'].rootAssembly
                
        s1 = a.instances['Superstructure-1'].faces
        side2Faces1 = s1.getByBoundingBox(GLocation[ii][0] - CSProp[1]/2, CSProp[3] - 0.1, 0, GLocation[ii][0] + CSProp[1]/2, CSProp[3] + 0.1, GLength + BWidth*math.tan(Skew*math.pi/180.0))
        region1=regionToolset.Region(side2Faces=side2Faces1)
    
        s1 = a.instances['Deck'].faces
        side2Faces1 = s1.findAt(((GLocation[ii][0], CSProp[3], GLocation[ii][2]), ))
        region2=regionToolset.Region(side2Faces=side2Faces1)
        
        mdb.models['Model-1'].Tie(name='Tie - ' + str(ii), master=region1, slave=region2, 
            positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, 
            thickness=ON)
    return

def Supports(System_info, GLocation):
    nGirder = System_info[0]['Girder Number']
    SLength = System_info[0]['Span Length']
    SType = System_info[3]['Support type']
    
    a = mdb.models['Model-1'].rootAssembly
    
    # Calculate location for supports...
    SGlobal = [[0,0,0]]
    Total = 0.0
    for item in SLength:
        Total = item + Total
        SGlobal.append([0, 0, Total])
    
    InstanceName = 'Superstructure-1'
    e = a.instances[InstanceName].edges
    
    # Define support at along edges at support location...
    for ii in range(0, nGirder):        
        jj = 0
        for BoundaryType in SType:

            GlobalLoc = [E1 + E2 for E1, E2 in zip(GLocation[ii], SGlobal[jj])]
            GlobalLoc[0] = GlobalLoc[0] + 0.05
            
            Selection = e.findAt((tuple(GlobalLoc), ))
            
            GlobalLoc[0] = GlobalLoc[0] - 0.1
            Selection = Selection + e.findAt((tuple(GlobalLoc), ))
            
            region = regionToolset.Region(edges=Selection)
        
            BoundaryName = 'Support - ' + str(ii + 1) + ' - ' + str(jj + 1)
            if BoundaryType == 1:
                mdb.models['Model-1'].DisplacementBC(name=BoundaryName, createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            else:
                mdb.models['Model-1'].DisplacementBC(name=BoundaryName, createStepName='Initial', region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
            jj += 1
    return

def Mesh(System_info): 
    # Mesh Superstructure
    PartName = 'Superstructure'
    p = mdb.models['Model-1'].parts[PartName]
    region = p.sets['Truss'].edges
    
    p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
    p.seedEdgeByNumber(edges=region, number=1, constraint=FINER)
    elemType1 = mesh.ElemType(elemCode=T3D2, elemLibrary=STANDARD)
    p.setElementType(regions=p.sets['Truss'], elemTypes=(elemType1, ))
    
    p.generateMesh()
    
    # Mesh Deck
    PartName = 'Deck'
    p = mdb.models['Model-1'].parts[PartName]
    p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    
    return

##### --- Main Abaqus Code --- #####
ModelName = 'Model-1'

# Create Girder Part...
ii = 1
s = mdb.models[ModelName].ConstrainedSketch(name='__profile__',sheetSize=200.0)
PList,CList = GirderSketch(System_info[0]['Cross Section Property'][0],'I')
IBeamSketch(s, PList, CList)
PartBeamExtrude(ii, System_info[0]['Girder Length'])

# Breakup Girder Geometry by Partitions...
ii = 2
PartName = 'Girder - 1'
Plane = 'XY'
for item in splice_coord[0][1:-1]:
    DatumPartition(item, Plane, PartName, ii)
    ii += 2

BridgeMaterial(System_info)
CreateBridgeSections(System_info)

# Assign Girder Sections
PartName = 'Girder - 1'
BeamAssignment(System_info, splice_coord, PartName)

# Create Deck & Assign Properties...
PartName = 'Deck'
SectionName = 'Deck'
DeckSketch(System_info, PartName)
DeckAssignment(System_info, PartName, SectionName)

# Break Deck Geometry by Partitions...
PartName = 'Deck'
Plane = 'XZ'

DeckInfo = System_info[1]['Deck']
bf = System_info[0]['Cross Section Property'][0][1]

DPLocation = []

Pos = DeckInfo[4] - bf/2
DPLocation.append(Pos)
Pos = DeckInfo[4] + bf/2
DPLocation.append(Pos)

ii = 2
for GSpacing in System_info[0]["Girder Spacing"]: 
    Pos = GSpacing + DPLocation[ii - 2]
    DPLocation.append(Pos)
    
    Pos = GSpacing + DPLocation[ii - 1]
    DPLocation.append(Pos)
    
    ii += 2

ii = 3
for item in DPLocation:
    DatumPartition(item, Plane, PartName, ii)
    ii += 2

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

# Assemble Superstructre ...
# Determine Location of Girders...
GLocation = [(0,0,0)]
ii = 0
Skew = System_info[1]["Skew"]
for GSpacing in System_info[0]["Girder Spacing"]:
    Pos = (GSpacing + GLocation[ii][0], 0, (GSpacing + GLocation[ii][0])*math.tan(Skew*math.pi/180.0))
    GLocation.append(Pos)
    ii += 1

if System_info[2]['Orientation'] == 'Parallel':
    BCoord = list(zip(bracing_xcoord,bracing_ycoord))
else:
    BCoord = reversed(list(zip(bracing_xcoord,bracing_ycoord)))
SuperstructureAssembly(GLocation, BCoord, System_info)

AName = 'Superstructure'
a = mdb.models['Model-1'].rootAssembly
IList = a.instances.keys()
a.InstanceFromBooleanMerge(name=AName, instances=([a.instances[IList[i]] for i in range(len(IList))]), mergeNodes=ALL, nodeMergingTolerance=0.1, domain=GEOMETRY, originalInstances=DELETE)

# Assemble Bridge System...
BridgeAssembly(System_info)

# Assign Girder/Deck Tie, Supports, and Mesh...
TieInteraction(System_info, GLocation)
Supports(System_info, GLocation)
Mesh(System_info)

# Assign Load Step...
mdb.models['Model-1'].StaticStep(name='LC_1', previous='Initial')

# Define basic pressure load along center of bridge...
Z = System_info[0]['Girder Length']/2
Y = System_info[0]['Cross Section Property'][0][3]
X = sum(System_info[0]['Girder Spacing'])/2

a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Deck'].faces
side2Faces1 = s1.findAt(((X, Y, Z), ))
region = regionToolset.Region(side2Faces=side2Faces1)
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='LC_1', 
    region=region, distributionType=UNIFORM, field='', magnitude=-1.0, 
    amplitude=UNSET)

# Assign Output Parameters...
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 'U'))
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(frequency=LAST_INCREMENT)

# Assign Job for Analysis...
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB)

mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1'].waitForCompletion()

# Select output file...
session.mdbData.summary()
o3 = session.openOdb(name=WorkingDirectory + '//Job-1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)

# Create Displacement Report...
leaf = dgo.LeafFromNodeSets(nodeSets=("SUPERSTRUCTURE-1.TRUSS","DECK.DECK", ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
odb = session.odbs[WorkingDirectory + '//Job-1.odb']
session.writeFieldReport(fileName='DISPREPORT.csv', append=ON, sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL, variable=(('U', NODAL, ((COMPONENT, 'U1'), (COMPONENT, 'U2'), (COMPONENT, 'U3'), )), ))

# Create Stress Report...
leaf = dgo.LeafFromElementSets(elementSets=("SUPERSTRUCTURE-1.TRUSS","DECK.DECK", ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
odb = session.odbs[WorkingDirectory + '//Job-1.odb']
session.writeFieldReport(fileName='STRESSREPORT.csv', append=ON, sortItem='Element Label', odb=odb, step=0, frame=1, outputPosition=INTEGRATION_POINT, variable=(('S', INTEGRATION_POINT, ((COMPONENT, 'S11'), )), ))