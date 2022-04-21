# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:47:42 2022

@author: adbje
"""

# -*- coding: mbcs -*-
# Do not delete the following import lines
import pandas as pd
import math

# "Example Input File - Sheet1.csv"   #Read input csv file

class system_iden:
    
    def retrieve (filename,i = 1):       #Asks for filename, Bridge Number as inputs
        
        data = pd.read_csv(filename)        

        data = data[data["Bridge"] == str(i)]    # Open data of bridge user selected  
        data = data.reset_index(drop=True)       # Reorganizing index 
        
        
        G_number_raw = data ["Girder"]          # Girder Number
        G_span_length_raw = data["Girder.1"]    # Girder span length
        G_order_raw = data["Girder.2"]          # Girder section order
        G_properties_raw = data["Girder.3"]     # Cross section dimension
        G_splice_raw = data["Girder.4"]         # Location of splice
        
        G_number = []
        G_span_length = []
        G_order = []
        G_properties = []
        G_splice = []
        
        
        # Loops to format information into list or list of lists
        
        for x in range (len(data)):          
            
            G_number.append(data ["Girder"][x])     
            G_span_length.append(data["Girder.1"][x])
            G_order.append((list(G_order_raw[x].split(";"))))
            G_properties.append((list(G_properties_raw[x].split(";"))))
            G_splice.append((list(G_splice_raw[x].split(";"))))
        
        for i in range(len(G_number)):
            G_number[i] = int(G_number[i])
        
        y = 0
        while y < len(G_properties):
            
            for z in range(len(G_properties[y])):
                G_properties[y][z] = G_properties[y][z][1:-1].split(",")
                for k in range(len(G_properties[y][z])):
                    G_properties[y][z][k] = float(G_properties[y][z][k])
            y+=1
        
        y = 0 
        while y < len(G_splice):
            
            for z in range(len(G_splice[y])):
                G_splice[y][z] = G_splice[y][z][1:-1].split(",")
                for k in range(len(G_splice[y][z])):
                    G_splice[y][z][k] = float(G_splice[y][z][k])
            y+=1
        
        
        y = 0
        while y < len(G_order):
            
            for z in range(len(G_order[y])):
                G_order[y][z] = G_order[y][z][1:-1].split(",")
                for k in range(len(G_order[y][z])):
                    G_order[y][z][k] = int(G_order[y][z][k])
            y+=1   
        
        y = 0
        while y < len(G_span_length):
            
            G_span_length[y] = G_span_length[y][1:-1].split(",")
            for z in range(len(G_span_length)):
                G_span_length[y][z] = float(G_span_length[y][z])    
            y+=1 
        
        # Create dictionary of Girder information
        # Values are either list or list of lists
        Girder_info = {"Girder Number":G_number, "Span Length": G_span_length, "Cross Section order": G_order,"Cross section Property": G_properties, 'Splice location': G_splice}
        
        
        return Girder_info



    def splice_global (Girder_info, dist_x = 5, dist_y = 5):
        
        # Function to assign global coordinates of each splice
        # dist_x and dist_y are distance between each Girder
        # Creates list of lists. Each component is list of global coordinate of all splices within each girder
        # Length of output will be # of girder, # of each list inside of output is # of splices
        a = Girder_info["Splice location"]
        
        splice_global = []
        x_start = 0
        y_start = 0 
        x_coord = []
        y_coord = []
        for i in range(len(a)):
            m = []
            x_start = 0
            if i != 0:
                x_start += dist_x
            for j in range (len(a[i])):
                for k in range (len(a[i][j])):
                        x_start += a[i][j][k]
                        m.append(x_start)  
            x_coord.append(m)
        
        for i in range(len(a)):
            m = []
            y_start = 0
            if i != 0:
                y_start += dist_y
            for j in range (len(a[i])):
                for k in range (len(a[i][j])):
                        m.append(y_start)  
            y_coord.append(m)
        
        return x_coord,y_coord



    def splice_dist_calc (x_coord, y_coord, Girder_num = [1,2], splice_num = [1,1]):
        
        # Calculates distance between splices based on user input
        # User defines total global x-y coordinate of all splices, Girder Number and splice number of two splices that user wants
        
        m1 = Girder_num[0]-1
        m2 = Girder_num[1]-1
        n1 = splice_num[0]-1
        n2 = splice_num[1]-1
        splice_dist = math.hypot(x_coord[m2][n2] - x_coord[m1][n1], y_coord[m2][n2] - y_coord[m1][n1])
        return splice_dist

Girder_info = system_iden.retrieve("Example Input File - Sheet1.csv",i = 1)
print (system_iden.splice_global(Girder_info))
x_coord = system_iden.splice_global(Girder_info)[0]
y_coord = system_iden.splice_global(Girder_info)[1]
print (x_coord)
print (y_coord)
print (system_iden.splice_dist_calc(x_coord,y_coord))

# system_iden.retrieve ("Example Input File - Sheet1.csv")



# print (G_number, G_length, G_section,G_properties)

# from abaqus import *
# from abaqusConstants import *
# import __main__

# def GirderShell1():
#     import section
#     import regionToolset
#     import displayGroupMdbToolset as dgm
#     import part
#     import material
#     import assembly
#     import step
#     import interaction
#     import load
#     import mesh
#     import optimization
#     import job
#     import sketch
#     import visualization
#     import xyPlot
#     import displayGroupOdbToolset as dgo
#     import connectorBehavior
#     s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=200.0)

#     g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

#     ## --- Defining Girder Sketch --- ###
#     s.setPrimaryObject(option=STANDALONE)
#     s.Line(point1=(-10.0, 0.0), point2=(0.0, 0.0))
#     s.HorizontalConstraint(entity=g[2], addUndoState=False)

#     s.Line(point1=(0.0, 0.0), point2=(10.0, 0.0))
#     s.HorizontalConstraint(entity=g[3], addUndoState=False)
#     s.ParallelConstraint(entity1=g[2], entity2=g[3], addUndoState=False)

#     s.Line(point1=(0.0, 0.0), point2=(0.0, 20.0))
#     s.VerticalConstraint(entity=g[4], addUndoState=False)
#     s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)

#     s.Line(point1=(0.0, 20.0), point2=(-10.0, 20.0))
#     s.HorizontalConstraint(entity=g[5], addUndoState=False)
#     s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)

#     s.Line(point1=(0.0, 20.0), point2=(10.0, 20.0))
#     s.HorizontalConstraint(entity=g[6], addUndoState=False)
#     s.PerpendicularConstraint(entity1=g[4], entity2=g[6], addUndoState=False)

#     s.EqualLengthConstraint(entity1=g[2], entity2=g[5])
#     s.EqualLengthConstraint(entity1=g[5], entity2=g[3], addUndoState=False)
#     s.EqualLengthConstraint(entity1=g[3], entity2=g[6], addUndoState=False)

#     s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-3.69686889648438,-3.1705150604248), value=10.0)
#     s.ObliqueDimension(vertex1=v[1], vertex2=v[3], textPoint=(3.75900268554688, 8.57904052734375), value=20.0)

#     ## --- Defining Part --- ###
#     p = mdb.models['Model-1'].Part(name='G1', dimensionality=THREE_D,type=DEFORMABLE_BODY)
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?

#     ## --- Converting sketch to shell... --- ###
#     p.BaseShellExtrude(sketch=s, depth=40.0)
#     s.unsetPrimaryObject()

#     p = mdb.models['Model-1'].parts['G1'] # Repeat?

#     session.viewports['Viewport: 1'].setValues(displayedObject=p)

#     del mdb.models['Model-1'].sketches['__profile__']
#     session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, engineeringFeatures=ON)
#     session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=OFF)

#     ## --- Defining material properties (Steel - Elastic)
#     mdb.models['Model-1'].Material(name='Steel')
#     mdb.models['Model-1'].materials['Steel'].Elastic(table=((29000.0, 0.3), ))

#     ## --- Defining shell sections w/ properties.
#     mdb.models['Model-1'].HomogeneousShellSection(name='Web', preIntegrate=OFF,
#         material='Steel', thicknessType=UNIFORM, thickness=0.25,
#         thicknessField='', nodalThicknessField='',
#         idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
#         thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
#         integrationRule=SIMPSON, numIntPts=5)
#     mdb.models['Model-1'].HomogeneousShellSection(name='Flange', preIntegrate=OFF,
#         material='Steel', thicknessType=UNIFORM, thickness=0.35,
#         thicknessField='', nodalThicknessField='',
#         idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
#         thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
#         integrationRule=SIMPSON, numIntPts=5)

#     ## --- Apply section properties --- ###
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     f = p.faces
#     faces = f.getSequenceFromMask(mask=('[#1d ]', ), )
#     region = p.Set(faces=faces, name='Flange')

#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     p.SectionAssignment(region=region, sectionName='Flange', offset=0.0,
#         offsetType=MIDDLE_SURFACE, offsetField='',
#         thicknessAssignment=FROM_SECTION)

#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     f = p.faces
#     faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
#     region = p.Set(faces=faces, name='Web')
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     p.SectionAssignment(region=region, sectionName='Web', offset=0.0,
#         offsetType=MIDDLE_SURFACE, offsetField='',
#         thicknessAssignment=FROM_SECTION)
#     mdb.models['Model-1'].parts['G1'].sectionAssignments[0].setValues(
#         offsetType=TOP_SURFACE, offsetField='', offset=0.0)

#     # Changing views.... Not necessary
#     session.viewports['Viewport: 1'].partDisplay.setValues(renderShellThickness=ON)
#     session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF,
#         engineeringFeatures=OFF)
#     session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
#         referenceRepresentation=ON)
#     session.viewports['Viewport: 1'].view.setValues(nearPlane=80.1213,
#         farPlane=133.354, width=64.1602, height=32.6048, cameraPosition=(
#         2.09447, 29.6578, 124.906), cameraUpVector=(-0.264498, 0.822531,
#         -0.503472), cameraTarget=(-0.00461483, 8.47763, 21.527))

#     # Fixing orientation of shell elements (way to ensure we can skip this step, annoying...)
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     f = p.faces
#     p.RepairFaceNormals(faceList = f[3:5])

#     # Changing views... Not necessary
#     session.viewports['Viewport: 1'].view.setValues(nearPlane=77.6961,
#         farPlane=135.409, width=62.2182, height=31.6179, cameraPosition=(
#         56.9607, 36.1383, 106.191), cameraUpVector=(-0.386581, 0.818979,
#         -0.424062), cameraTarget=(0.607108, 8.54988, 21.3183))
#     session.viewports['Viewport: 1'].view.setValues(nearPlane=75.9594,
#         farPlane=137.145, width=82.8822, height=42.1188, viewOffsetX=3.56744,
#         viewOffsetY=-0.176565)

#     ## --- Defining a datum --- ###
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=20.0)
#     session.viewports['Viewport: 1'].view.fitView()

#     ## --- Defining a partition --- ###
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     f = p.faces
#     pickedFaces = f.getSequenceFromMask(mask=('[#1f ]', ), )
#     d1 = p.datums
#     p.PartitionFaceByDatumPlane(datumPlane=d1[5], faces=pickedFaces)

#     session.viewports['Viewport: 1'].view.setValues(nearPlane=80.062,
#         farPlane=139.672, width=71.5544, height=36.3623, viewOffsetX=7.11179,
#         viewOffsetY=0.811227)

#     ## --- Creating a stiffener --- ###
#     p = mdb.models['Model-1'].parts['G1'] # Repeat?
#     f1, e = p.faces, p.edges
#     t = p.MakeSketchTransform(sketchPlane=f1[3], sketchUpEdge=e[12],
#         sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 10.0,
#         30.0))

#     s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
#         sheetSize=89.44, gridSpacing=2.23, transform=t)
#     g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
#     s1.setPrimaryObject(option=SUPERIMPOSE)
#     p = mdb.models['Model-1'].parts['G1']
#     p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)

#     session.viewports['Viewport: 1'].view.setValues(nearPlane=39.0607,
#         farPlane=74.0764, width=83.0119, height=42.1848, cameraPosition=(
#         56.5685, 11.6447, 20.9528), cameraTarget=(0, 11.6447, 20.9528))

#     s1.Line(point1=(10.0, 10.0), point2=(10.0, -10.0))
#     s1.VerticalConstraint(entity=g[18], addUndoState=False)
#     s1.PerpendicularConstraint(entity1=g[4], entity2=g[18], addUndoState=False)

#     p = mdb.models['Model-1'].parts['G1']
#     f, e1 = p.faces, p.edges
#     p.ShellExtrude(sketchPlane=f[3], sketchUpEdge=e1[12], sketchPlaneSide=SIDE1,
#         sketchOrientation=RIGHT, sketch=s1, depth=5.0,
#         flipExtrudeDirection=OFF)
#     s1.unsetPrimaryObject()

#     del mdb.models['Model-1'].sketches['__profile__']
#     session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON,
#         engineeringFeatures=ON)
#     session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
#         referenceRepresentation=OFF)
#     mdb.models['Model-1'].HomogeneousShellSection(name='Stiffener',
#         preIntegrate=OFF, material='Steel', thicknessType=UNIFORM,
#         thickness=0.1, thicknessField='', nodalThicknessField='',
#         idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
#         thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
#         integrationRule=SIMPSON, numIntPts=5)

#     p = mdb.models['Model-1'].parts['G1']
#     f = p.faces
#     faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
#     region = p.Set(faces=faces, name='Stiffener')
#     p = mdb.models['Model-1'].parts['G1']
#     p.SectionAssignment(region=region, sectionName='Stiffener', offset=0.0,
#         offsetType=MIDDLE_SURFACE, offsetField='',
#         thicknessAssignment=FROM_SECTION)
