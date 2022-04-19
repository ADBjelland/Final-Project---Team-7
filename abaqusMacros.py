# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def GBeam():
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
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(0.0, 0.0), point2=(50.0, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseWire(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((29000.0, 0.3), ))
    mdb.models['Model-1'].GeneralizedProfile(name='Profile-1', area=100.0, 
        i11=100.0, i12=100.0, i22=100.0, j=50.0, gammaO=0.0, gammaW=0.0)
    mdb.models['Model-1'].BeamSection(name='Section-1', 
        integration=BEFORE_ANALYSIS, poissonRatio=0.3, beamShape=CONSTANT, 
        profile='Profile-1', thermalExpansion=OFF, temperatureDependency=OFF, 
        dependencies=0, table=((29000.0, 11500.0), ), alphaDamping=0.0, 
        betaDamping=0.0, compositeDamping=0.0, centroid=(0.0, 0.0), 
        shearCenter=(0.0, 0.0), consistentMassMatrix=False)
    p = mdb.models['Model-1'].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(edges=edges, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
    mdb.models['Model-1'].StaticStep(name='Elastic Flexure', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        step='Elastic Flexure')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        constraints=ON, connectors=ON, engineeringFeatures=ON, 
        adaptiveMeshConstraints=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, interactions=OFF, constraints=OFF, 
        engineeringFeatures=OFF)
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['Part-1-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#2 ]', ), )
    region = regionToolset.Region(vertices=verts1)
    mdb.models['Model-1'].ConcentratedForce(name='Point Load', 
        createStepName='Elastic Flexure', region=region, cf2=-1.0, 
        distributionType=UNIFORM, field='', localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    v1 = a.instances['Part-1-1'].vertices
    verts1 = v1.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(vertices=verts1)
    mdb.models['Model-1'].DisplacementBC(name='Fixed', 
        createStepName='Elastic Flexure', region=region, u1=0.0, u2=0.0, 
        u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0, amplitude=UNSET, fixed=OFF, 
        distributionType=UNIFORM, fieldName='', localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=5.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB)


def Chisholm():
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
    s1.Line(point1=(238.8, 46.0), point2=(238.8, -46.0))
    s1.VerticalConstraint(entity=g[417], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[252], entity2=g[417], addUndoState=False)
    s1.Line(point1=(358.8, 46.0), point2=(358.8, -46.0))
    s1.VerticalConstraint(entity=g[418], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[252], entity2=g[418], addUndoState=False)
    s1.Line(point1=(478.8, 46.0), point2=(478.8, -46.0))
    s1.VerticalConstraint(entity=g[419], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[237], entity2=g[419], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14251.9, 
        farPlane=14898.1, width=3640.97, height=1730.51, cameraPosition=(14575, 
        -72.9448, 4581.57), cameraTarget=(0, -72.9448, 4581.57))
    s1.Line(point1=(598.8, 46.0), point2=(598.8, -46.0))
    s1.VerticalConstraint(entity=g[420], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[229], entity2=g[420], addUndoState=False)
    s1.Line(point1=(718.8, 46.0), point2=(718.8, -46.0))
    s1.VerticalConstraint(entity=g[421], addUndoState=False)
    s1.ParallelConstraint(entity1=g[228], entity2=g[421], addUndoState=False)
    s1.Line(point1=(838.8, 46.0), point2=(838.8, -46.0))
    s1.VerticalConstraint(entity=g[422], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[213], entity2=g[422], addUndoState=False)
    s1.Line(point1=(1258.8, 46.0), point2=(1258.8, -46.0))
    s1.VerticalConstraint(entity=g[423], addUndoState=False)
    s1.ParallelConstraint(entity1=g[204], entity2=g[423], addUndoState=False)
    s1.Line(point1=(1438.8, 46.0), point2=(1438.8, -46.0))
    s1.VerticalConstraint(entity=g[424], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[178], entity2=g[424], addUndoState=False)
    s1.Line(point1=(1618.8, 46.0), point2=(1618.8, -46.0))
    s1.VerticalConstraint(entity=g[425], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[179], entity2=g[425], addUndoState=False)
    s1.Line(point1=(1903.8, 46.0), point2=(1903.8, -46.0))
    s1.VerticalConstraint(entity=g[426], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[170], entity2=g[426], addUndoState=False)
    s1.Line(point1=(2188.8, 46.0), point2=(2188.8, -46.0))
    s1.VerticalConstraint(entity=g[427], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[165], entity2=g[427], addUndoState=False)
    s1.Line(point1=(2188.8, -46.0), point2=(2277.33639453125, -181.386016845703))
    s1.undo()
    s1.Line(point1=(2473.8, 46.0), point2=(2473.8, -46.0))
    s1.VerticalConstraint(entity=g[428], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[157], entity2=g[428], addUndoState=False)
    s1.Line(point1=(2758.8, 46.0), point2=(2758.8, -46.0))
    s1.VerticalConstraint(entity=g[429], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[149], entity2=g[429], addUndoState=False)
    s1.Line(point1=(2938.8, 46.0), point2=(2938.8, -46.0))
    s1.VerticalConstraint(entity=g[430], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[141], entity2=g[430], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14345.4, 
        farPlane=14804.6, width=2542.75, height=1208.54, cameraPosition=(14575, 
        43.2847, 4011.88), cameraTarget=(0, 43.2847, 4011.88))
    s1.Line(point1=(3118.8, 46.0), point2=(3118.8, -46.0))
    s1.VerticalConstraint(entity=g[431], addUndoState=False)
    s1.ParallelConstraint(entity1=g[140], entity2=g[431], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14036.5, 
        farPlane=15113.5, width=6984.29, height=3319.56, cameraPosition=(14575, 
        226.313, 5922.47), cameraTarget=(0, 226.313, 5922.47))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14288, 
        farPlane=14862, width=3217.16, height=1529.08, cameraPosition=(14575, 
        151.322, 2836.24), cameraTarget=(0, 151.322, 2836.24))
    s1.Line(point1=(3298.8, 46.0), point2=(3298.8, -46.0))
    s1.VerticalConstraint(entity=g[432], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[125], entity2=g[432], addUndoState=False)
    s1.Line(point1=(3418.8, 46.0), point2=(3418.8, -46.0))
    s1.VerticalConstraint(entity=g[433], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[117], entity2=g[433], addUndoState=False)
    s1.Line(point1=(3538.8, 46.0), point2=(3538.8, -46.0))
    s1.VerticalConstraint(entity=g[434], addUndoState=False)
    s1.ParallelConstraint(entity1=g[116], entity2=g[434], addUndoState=False)
    s1.Line(point1=(3658.8, 46.0), point2=(3658.8, -46.0))
    s1.VerticalConstraint(entity=g[435], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[101], entity2=g[435], addUndoState=False)
    s1.Line(point1=(3778.8, 46.0), point2=(3778.8, -46.0))
    s1.VerticalConstraint(entity=g[436], addUndoState=False)
    s1.ParallelConstraint(entity1=g[100], entity2=g[436], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14348, 
        farPlane=14802, width=2511.79, height=1193.83, cameraPosition=(14575, 
        96.7657, 2651.08), cameraTarget=(0, 96.7657, 2651.08))
    s1.undo()
    s1.Line(point1=(4018.8, 46.0), point2=(4018.8, -46.0))
    s1.VerticalConstraint(entity=g[436], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[66], entity2=g[436], addUndoState=False)
    s1.Line(point1=(4138.8, 46.0), point2=(4138.8, -46.0))
    s1.VerticalConstraint(entity=g[437], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[66], entity2=g[437], addUndoState=False)
    s1.Line(point1=(4258.8, 46.0), point2=(4258.8, -46.0))
    s1.VerticalConstraint(entity=g[438], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[58], entity2=g[438], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14304.4, 
        farPlane=14845.6, width=3422.51, height=1626.68, cameraPosition=(14575, 
        97.6857, 3054.2), cameraTarget=(0, 97.6857, 3054.2))
    s1.Line(point1=(4510.8, 46.0), point2=(4510.8, -46.0))
    s1.VerticalConstraint(entity=g[439], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[58], entity2=g[439], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14211.1, 
        farPlane=14938.9, width=4663.43, height=2216.48, cameraPosition=(14575, 
        154.841, 3620.73), cameraTarget=(0, 154.841, 3620.73))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14394.9, 
        farPlane=14755.1, width=1961.08, height=932.081, cameraPosition=(14575, 
        82.316, 1042.97), cameraTarget=(0, 82.316, 1042.97))
    s1.Line(point1=(4762.8, 46.0), point2=(4762.8, -46.0))
    s1.VerticalConstraint(entity=g[440], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[53], entity2=g[440], addUndoState=False)
    s1.Line(point1=(5014.8, 46.0), point2=(5014.8, -46.0))
    s1.VerticalConstraint(entity=g[441], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[45], entity2=g[441], addUndoState=False)
    s1.Line(point1=(5266.8, 46.0), point2=(5266.8, -46.0))
    s1.VerticalConstraint(entity=g[442], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[37], entity2=g[442], addUndoState=False)
    s1.Line(point1=(5386.8, 46.0), point2=(5386.8, -46.0))
    s1.VerticalConstraint(entity=g[443], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[29], entity2=g[443], addUndoState=False)
    s1.Line(point1=(5506.8, 46.0), point2=(5506.8, -46.0))
    s1.VerticalConstraint(entity=g[444], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[21], entity2=g[444], addUndoState=False)
    s1.Line(point1=(5626.8, 46.0), point2=(5626.8, -46.0))
    s1.VerticalConstraint(entity=g[445], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[13], entity2=g[445], addUndoState=False)
    s1.Line(point1=(5746.8, 46.0), point2=(5746.8, -46.0))
    s1.VerticalConstraint(entity=g[446], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[5], entity2=g[446], addUndoState=False)
    s1.Line(point1=(5866.8, 46.0), point2=(5866.8, -46.0))
    s1.VerticalConstraint(entity=g[447], addUndoState=False)
    s1.ParallelConstraint(entity1=g[4], entity2=g[447], addUndoState=False)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13947.2, 
        farPlane=15202.8, width=7220.77, height=3431.96, cameraPosition=(14575, 
        182.929, 1287.83), cameraTarget=(0, 182.929, 1287.83))
    p = mdb.models['Model-1'].parts['CT G6']
    f, e = p.faces, p.edges
    p.ShellExtrude(sketchPlane=f[168], sketchUpEdge=e[433], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, depth=9.0, 
        flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13255.7, 
        farPlane=18434.9, width=5152.6, height=2448.98, viewOffsetX=-202.037, 
        viewOffsetY=-463.291)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(name='S3-4', preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=0.75, 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    mdb.models['Model-1'].HomogeneousShellSection(name='S1-1/4', preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=1.25, 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    mdb.models['Model-1'].sections.changeKey(fromName='S3-4', toName='S3/4')
    mdb.models['Model-1'].sections.changeKey(fromName='F1-5', toName='F1/5')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13133.7, 
        farPlane=18556.8, width=6592.43, height=3133.31, viewOffsetX=376.308, 
        viewOffsetY=-293.099)
    mdb.models['Model-1'].sections.changeKey(fromName='F1/5', toName='F1-5')
    session.viewports['Viewport: 1'].view.setValues(width=6212.08, height=2952.54, 
        viewOffsetX=309.462, viewOffsetY=-306.252)
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10906.7, 
        farPlane=18243.3, width=312.979, height=148.756, cameraPosition=(
        168.771, 99.8842, 18216.9), cameraUpVector=(-0.00986891, 0.999944, 
        -0.00392588))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10906.9, 
        farPlane=18243.1, width=312.984, height=148.758, cameraPosition=(
        0.220116, 46.0914, 18218), cameraUpVector=(-0.0061484, 0.999981, 
        -0.000349222), cameraTarget=(2.28882e-05, 41, 3643.03))
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10913, 
        farPlane=18237, width=313.159, height=148.841, cameraPosition=(931.385, 
        166.249, 18187.7), cameraUpVector=(-0.00286802, 0.99996, -0.00842737))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10901.2, 
        farPlane=18248.8, width=490.617, height=233.185, viewOffsetX=-27.1569, 
        viewOffsetY=-0.529536)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10898.8, 
        farPlane=18251.1, width=490.511, height=233.135, cameraPosition=(
        931.289, 168.206, 18187.7), cameraUpVector=(-0.0566872, 0.99838, 
        -0.00496739), cameraTarget=(-0.0964575, 42.957, 3643.02), 
        viewOffsetX=-27.1511, viewOffsetY=-0.529423)
    p = mdb.models['Model-1'].parts['CT G6']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#ffffffff #3f ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['CT G6']
    p.SectionAssignment(region=region, sectionName='S3/4', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10884.7, 
        farPlane=18265.3, width=710.099, height=337.503, viewOffsetX=-72.9207, 
        viewOffsetY=18.9684)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11252.7, 
        farPlane=17815, width=734.106, height=348.913, cameraPosition=(6824.7, 
        -112.58, 16474), cameraUpVector=(-0.145535, 0.985245, 0.0900624), 
        cameraTarget=(-10.0643, 54.472, 3601.93), viewOffsetX=-75.386, 
        viewOffsetY=19.6097)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11019.3, 
        farPlane=18048.4, width=3852.57, height=1831.09, viewOffsetX=-540.082, 
        viewOffsetY=220.742)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11260.3, 
        farPlane=17514.2, width=3936.83, height=1871.13, cameraPosition=(
        9169.04, 7.91318, 14730), cameraUpVector=(-0.111174, 0.98934, 
        0.0940563), cameraTarget=(-103.668, 34.9675, 3485.07), 
        viewOffsetX=-551.894, viewOffsetY=225.569)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11385.7, 
        farPlane=17388.8, width=2144.06, height=1019.05, viewOffsetX=-965.514, 
        viewOffsetY=208.856)
    p = mdb.models['Model-1'].parts['CT G6']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14371.2, 
        farPlane=14775.4, width=2219.42, height=1054.87, cameraPosition=(
        14573.3, 44.9768, 4688.38), cameraTarget=(0, 44.9768, 4688.38))
    s2.Line(point1=(958.8, 46.0), point2=(958.8, -46.0))
    s2.VerticalConstraint(entity=g[780], addUndoState=False)
    s2.PerpendicularConstraint(entity1=g[213], entity2=g[780], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14309.1, 
        farPlane=14837.5, width=2949.07, height=1401.66, cameraPosition=(
        14573.3, -54.266, 2157.68), cameraTarget=(0, -54.266, 2157.68))
    s2.Line(point1=(3778.8, 46.0), point2=(3778.8, -46.0))
    s2.VerticalConstraint(entity=g[781], addUndoState=False)
    s2.PerpendicularConstraint(entity1=g[101], entity2=g[781], addUndoState=False)
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G6']
    p.features['Shell extrude-2'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G6']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G6']
    p.regenerate()
    p1 = mdb.models['Model-1'].parts['CT G6']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11271, 
        farPlane=17503.5, width=3496.12, height=1661.67, viewOffsetX=-1363.35, 
        viewOffsetY=180.335)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12662.8, 
        farPlane=18509.1, width=1222, height=580.802, viewOffsetX=668.066, 
        viewOffsetY=-101.174)
    p = mdb.models['Model-1'].parts['CT G6']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#ffffffff #ff ]', ), )
    region=regionToolset.Region(faces=faces)
    mdb.models['Model-1'].parts['CT G6'].sectionAssignments[5].setValues(
        region=region)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12668.8, 
        farPlane=18503, width=1301.29, height=618.49, viewOffsetX=201.769, 
        viewOffsetY=73.1645)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models['Model-1'].parts['CT G6']
    f1, e1 = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f1[167], sketchUpEdge=e1[464], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 46.0, 
        4873.032))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=2761.33, gridSpacing=69.03, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['CT G6']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=308.508, 
        farPlane=500.086, width=1098.14, height=521.936, cameraPosition=(
        404.297, -24.6797, 5157.96), cameraTarget=(0, -24.6797, 5157.96))
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['CT G6']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[167], sketchUpEdge=e[26], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 46.0, 
        4873.032))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=2761.33, gridSpacing=69.03, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['CT G6']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=886.307, 
        farPlane=1572.32, width=3874.82, height=1841.66, cameraPosition=(
        1229.31, 219.642, 3062.73), cameraTarget=(0, 219.642, 3062.73))
    s1.Line(point1=(-90.0, 46.0), point2=(-90.0, -46.0))
    s1.VerticalConstraint(entity=g[450], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[245], entity2=g[450], addUndoState=False)
    s1.Line(point1=(2730.0, 46.0), point2=(2730.0, -46.0))
    s1.VerticalConstraint(entity=g[451], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[130], entity2=g[451], addUndoState=False)
    p = mdb.models['Model-1'].parts['CT G6']
    f1, e1 = p.faces, p.edges
    p.ShellExtrude(sketchPlane=f1[167], sketchUpEdge=e1[26], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, depth=11.0, 
        flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12471.7, 
        farPlane=18700.2, width=3917.73, height=1862.06, viewOffsetX=-930.805, 
        viewOffsetY=468.171)
    p = mdb.models['Model-1'].parts['CT G6']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3 ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['CT G6']
    p.SectionAssignment(region=region, sectionName='S1-1/4', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12744.3, 
        farPlane=18427.5, width=263.059, height=125.029, viewOffsetX=-441.296, 
        viewOffsetY=48.9645)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12439, 
        farPlane=19451.7, width=256.756, height=122.034, cameraPosition=(
        4160.65, 1769.14, 18942), cameraUpVector=(-0.0640666, 0.992923, 
        -0.0999938), cameraTarget=(-189.522, -8.11591, 4081.34), 
        viewOffsetX=-430.724, viewOffsetY=47.7914)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13652.1, 
        farPlane=18038.5, width=548.806, height=260.842, viewOffsetX=1178.71, 
        viewOffsetY=651.534)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10991.3, 
        farPlane=20699.2, width=32363.9, height=15382.2, viewOffsetX=15082.1, 
        viewOffsetY=5016.24)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13178.2, 
        farPlane=18512.4, width=6866.69, height=3263.67, viewOffsetX=120.04, 
        viewOffsetY=39.1294)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p1 = mdb.models['Model-1'].parts['CT G6']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G5', 
        objectToCopy=mdb.models['Model-1'].parts['CT G6'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13110.4, 
        farPlane=18580.1, width=6831.39, height=3246.89, viewOffsetX=297.113, 
        viewOffsetY=123.672)
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Datum plane-52'].suppress()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13025.1, 
        farPlane=18665.4, width=8805.06, height=4184.95, viewOffsetX=716.528, 
        viewOffsetY=316.406)
    p = mdb.models['Model-1'].parts['CT G5']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=55.032)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13579.6, 
        farPlane=18110.9, width=1336.61, height=635.279, viewOffsetX=1871.97, 
        viewOffsetY=1084.53)
    p = mdb.models['Model-1'].parts['CT G5']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#11 #20000 #0:5 #1100000 ]', ), )
    d1 = p.datums
    p.PartitionFaceByDatumPlane(datumPlane=d1[120], faces=pickedFaces)
    p = mdb.models['Model-1'].parts['CT G5']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14517.3, 
        farPlane=14629.3, width=502.699, height=238.928, cameraPosition=(
        14573.3, 48.1911, 275.858), cameraTarget=(0, 48.1911, 275.858))
    s2.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14403.2, 
        farPlane=14743.4, width=1843.41, height=876.156, cameraPosition=(
        14573.3, 75.0321, 6380.15), cameraTarget=(0, 75.0321, 6380.15))
    s1.delete(objectList=(g[319], ))
    s1.delete(objectList=(g[381], g[410], c[1332]))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13853.1, 
        farPlane=15293.5, width=9400.79, height=4468.1, cameraPosition=(
        14573.3, 635.05, 3815.64), cameraTarget=(0, 635.05, 3815.64))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Shell extrude-2'].setValues(sketch=s1)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    s2.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13491.3, 
        farPlane=18199.3, width=2376.34, height=1129.45, viewOffsetX=1876.79, 
        viewOffsetY=978.192)
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Shell extrude-2'].resume()
    p = mdb.models['Model-1'].parts['CT G5']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14444.9, 
        farPlane=14701.6, width=1352.89, height=643.014, cameraPosition=(
        14573.3, 15.494, 679.759), cameraTarget=(0, 15.494, 679.759))
    s1.resetView()
    s1.resetView()
    mdb.models['Model-1'].sketches['__edit__'].sketchOptions.setValues(
        sheetSize=999.0, sheetAuto=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13858.8, 
        farPlane=15287.8, width=9324.34, height=4431.76, cameraPosition=(
        14573.3, 252.027, 2743.47), cameraTarget=(0, 252.027, 2743.47))
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Shell extrude-3'].resume()
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[2], sketchUpEdge=e[8], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 46.0, 
        115.032))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=9817.72, gridSpacing=245.44, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['CT G5']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=239.689, 
        farPlane=365.145, width=658.551, height=313.003, cameraPosition=(
        302.417, 49.0995, 91.113), cameraTarget=(0, 49.0995, 91.113))
    s.Line(point1=(60.0, 46.0), point2=(60.0, -46.0))
    s.VerticalConstraint(entity=g[459], addUndoState=False)
    s.ParallelConstraint(entity1=g[4], entity2=g[459], addUndoState=False)
    p = mdb.models['Model-1'].parts['CT G5']
    f1, e1 = p.faces, p.edges
    p.ShellExtrude(sketchPlane=f1[2], sketchUpEdge=e1[8], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s, depth=9.0, flipExtrudeDirection=OFF)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Shell extrude-4'].setValues(flipExtrudeDirection=True)
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13310.8, 
        farPlane=18379.8, width=4502.64, height=2140.06, viewOffsetX=2417.05, 
        viewOffsetY=985.785)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13146.8, 
        farPlane=18543.8, width=6439.32, height=3060.54, viewOffsetX=209.235, 
        viewOffsetY=31.9479)
    p = mdb.models['Model-1'].parts['CT G5']
    s1 = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=110.109, 
        farPlane=680.842, width=3618.86, height=1720.01, cameraPosition=(
        395.475, 545.305, -1353.62), cameraTarget=(0, 545.305, -1353.62))
    session.viewports['Viewport: 1'].view.fitView()
    s2.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    s = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=337.584, 
        farPlane=453.367, width=594.239, height=282.436, cameraPosition=(
        395.475, 48.0128, 9.51805), cameraTarget=(0, 48.0128, 9.51805))
    session.viewports['Viewport: 1'].view.fitView()
    s1.Line(point1=(-60.0, 46.0), point2=(-60.0, -46.0))
    s1.VerticalConstraint(entity=g[915], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[5], entity2=g[915], addUndoState=False)
    s1.Line(point1=(-180.0, -46.0), point2=(-180.0, 46.0))
    s1.VerticalConstraint(entity=g[916], addUndoState=False)
    s1.ParallelConstraint(entity1=g[486], entity2=g[916], addUndoState=False)
    s1.Line(point1=(-300.0, 46.0), point2=(-300.0, -46.0))
    s1.VerticalConstraint(entity=g[917], addUndoState=False)
    s1.ParallelConstraint(entity1=g[490], entity2=g[917], addUndoState=False)
    s1.Line(point1=(-420.0, -46.0), point2=(-420.0, 46.0))
    s1.VerticalConstraint(entity=g[918], addUndoState=False)
    s1.ParallelConstraint(entity1=g[485], entity2=g[918], addUndoState=False)
    s1.Line(point1=(-540.0, 46.0), point2=(-540.0, -46.0))
    s1.VerticalConstraint(entity=g[919], addUndoState=False)
    s1.ParallelConstraint(entity1=g[491], entity2=g[919], addUndoState=False)
    s1.Line(point1=(-660.0, -46.0), point2=(-660.0, 46.0))
    s1.VerticalConstraint(entity=g[920], addUndoState=False)
    s1.ParallelConstraint(entity1=g[484], entity2=g[920], addUndoState=False)
    s1.Line(point1=(-912.0, 46.0), point2=(-912.0, -46.0))
    s1.VerticalConstraint(entity=g[921], addUndoState=False)
    s1.ParallelConstraint(entity1=g[492], entity2=g[921], addUndoState=False)
    s1.Line(point1=(-1164.0, -46.0), point2=(-1164.0, 46.0))
    s1.VerticalConstraint(entity=g[922], addUndoState=False)
    s1.ParallelConstraint(entity1=g[483], entity2=g[922], addUndoState=False)
    s1.Line(point1=(-1416.0, 46.0), point2=(-1416.0, -46.0))
    s1.VerticalConstraint(entity=g[923], addUndoState=False)
    s1.ParallelConstraint(entity1=g[493], entity2=g[923], addUndoState=False)
    s1.Line(point1=(-1668.0, 46.0), point2=(-1668.0, -46.0))
    s1.VerticalConstraint(entity=g[924], addUndoState=False)
    s1.ParallelConstraint(entity1=g[482], entity2=g[924], addUndoState=False)
    s1.Line(point1=(-1788.0, 46.0), point2=(-1788.0, -46.0))
    s1.VerticalConstraint(entity=g[925], addUndoState=False)
    s1.ParallelConstraint(entity1=g[494], entity2=g[925], addUndoState=False)
    s1.Line(point1=(-1908.0, 46.0), point2=(-1908.0, -46.0))
    s1.VerticalConstraint(entity=g[926], addUndoState=False)
    s1.ParallelConstraint(entity1=g[481], entity2=g[926], addUndoState=False)
    s1.Line(point1=(-2028.0, 46.0), point2=(-2028.0, -46.0))
    s1.VerticalConstraint(entity=g[927], addUndoState=False)
    s1.ParallelConstraint(entity1=g[467], entity2=g[927], addUndoState=False)
    s1.Line(point1=(-2148.0, -46.0), point2=(-2148.0, 46.0))
    s1.VerticalConstraint(entity=g[928], addUndoState=False)
    s1.ParallelConstraint(entity1=g[488], entity2=g[928], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14270.5, 
        farPlane=14879.5, width=3422.51, height=1626.68, cameraPosition=(14575, 
        -63.7617, 2787.18), cameraTarget=(0, -63.7617, 2787.18))
    s1.undo()
    s1.undo()
    s1.undo()
    s1.Line(point1=(-2148.0, 46.0), point2=(-2148.0, -46.0))
    s1.VerticalConstraint(entity=g[926], addUndoState=False)
    s1.ParallelConstraint(entity1=g[488], entity2=g[926], addUndoState=False)
    s1.Line(point1=(-2268.0, -46.0), point2=(-2268.0, 46.0))
    s1.VerticalConstraint(entity=g[927], addUndoState=False)
    s1.ParallelConstraint(entity1=g[495], entity2=g[927], addUndoState=False)
    s1.Line(point1=(-2388.0, 46.0), point2=(-2388.0, -46.0))
    s1.VerticalConstraint(entity=g[928], addUndoState=False)
    s1.ParallelConstraint(entity1=g[480], entity2=g[928], addUndoState=False)
    s1.Line(point1=(-2508.0, -46.0), point2=(-2508.0, 46.0))
    s1.VerticalConstraint(entity=g[929], addUndoState=False)
    s1.ParallelConstraint(entity1=g[496], entity2=g[929], addUndoState=False)
    s1.Line(point1=(-2628.0, 46.0), point2=(-2628.0, -46.0))
    s1.VerticalConstraint(entity=g[930], addUndoState=False)
    s1.ParallelConstraint(entity1=g[479], entity2=g[930], addUndoState=False)
    s1.Line(point1=(-2808.0, -46.0), point2=(-2808.0, 46.0))
    s1.VerticalConstraint(entity=g[931], addUndoState=False)
    s1.ParallelConstraint(entity1=g[497], entity2=g[931], addUndoState=False)
    s1.Line(point1=(-2988.0, 46.0), point2=(-2988.0, -46.0))
    s1.VerticalConstraint(entity=g[932], addUndoState=False)
    s1.ParallelConstraint(entity1=g[478], entity2=g[932], addUndoState=False)
    s1.Line(point1=(-3168.0, -46.0), point2=(-3168.0, 46.0))
    s1.VerticalConstraint(entity=g[933], addUndoState=False)
    s1.ParallelConstraint(entity1=g[498], entity2=g[933], addUndoState=False)
    s1.Line(point1=(-3453.0, 46.0), point2=(-3453.0, -46.0))
    s1.VerticalConstraint(entity=g[934], addUndoState=False)
    s1.ParallelConstraint(entity1=g[477], entity2=g[934], addUndoState=False)
    s1.Line(point1=(-3738.0, -46.0), point2=(-3738.0, 46.0))
    s1.VerticalConstraint(entity=g[935], addUndoState=False)
    s1.ParallelConstraint(entity1=g[499], entity2=g[935], addUndoState=False)
    s1.Line(point1=(-4023.0, 46.0), point2=(-4023.0, -46.0))
    s1.VerticalConstraint(entity=g[936], addUndoState=False)
    s1.ParallelConstraint(entity1=g[476], entity2=g[936], addUndoState=False)
    s1.Line(point1=(-4308.0, -46.0), point2=(-4308.0, 46.0))
    s1.VerticalConstraint(entity=g[937], addUndoState=False)
    s1.ParallelConstraint(entity1=g[500], entity2=g[937], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13897.2, 
        farPlane=15252.8, width=7808.14, height=3711.13, cameraPosition=(14575, 
        69.703, 882.366), cameraTarget=(0, 69.703, 882.366))
    session.viewports['Viewport: 1'].view.fitView()
    s1.Line(point1=(-4548.0, -46.0), point2=(-4548.0, 46.0))
    s1.VerticalConstraint(entity=g[938], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[701], entity2=g[938], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13618, 
        farPlane=15532, width=12549.7, height=5964.75, cameraPosition=(14575, 
        -180.829, 8988.41), cameraTarget=(0, -180.829, 8988.41))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14211.1, 
        farPlane=14938.9, width=4120.6, height=1958.48, cameraPosition=(14575, 
        20.3578, 3015), cameraTarget=(0, 20.3578, 3015))
    s1.Line(point1=(-1908.0, 46.0), point2=(-1908.0, -46.0))
    s1.VerticalConstraint(entity=g[939], addUndoState=False)
    s1.ParallelConstraint(entity1=g[481], entity2=g[939], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14081.9, 
        farPlane=15068, width=6380.27, height=3032.48, cameraPosition=(14575, 
        -4.25125, 1819.26), cameraTarget=(0, -4.25125, 1819.26))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14211.1, 
        farPlane=14938.9, width=4120.6, height=1958.48, cameraPosition=(14575, 
        7.3672, 4585.24), cameraTarget=(0, 7.3672, 4585.24))
    s1.delete(objectList=(g[704], g[849], g[938], c[3046]))
    s1.Line(point1=(-4488.0, 46.0), point2=(-4488.0, -46.0))
    s1.VerticalConstraint(entity=g[940], addUndoState=False)
    s1.ParallelConstraint(entity1=g[475], entity2=g[940], addUndoState=False)
    s1.Line(point1=(-4668.0, -46.0), point2=(-4668.0, 46.0))
    s1.VerticalConstraint(entity=g[941], addUndoState=False)
    s1.ParallelConstraint(entity1=g[501], entity2=g[941], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14127, 
        farPlane=15022.9, width=5780.74, height=2747.53, cameraPosition=(14575, 
        -32.293, 3297.39), cameraTarget=(0, -32.293, 3297.39))
    session.viewports['Viewport: 1'].view.fitView()
    s1.Line(point1=(-4968.0, 46.0), point2=(-4968.0, -46.0))
    s1.VerticalConstraint(entity=g[942], addUndoState=False)
    s1.ParallelConstraint(entity1=g[487], entity2=g[942], addUndoState=False)
    s1.Line(point1=(-5088.0, -46.0), point2=(-5088.0, 46.0))
    s1.VerticalConstraint(entity=g[943], addUndoState=False)
    s1.ParallelConstraint(entity1=g[474], entity2=g[943], addUndoState=False)
    s1.Line(point1=(-5208.0, 46.0), point2=(-5208.0, -46.0))
    s1.VerticalConstraint(entity=g[944], addUndoState=False)
    s1.ParallelConstraint(entity1=g[502], entity2=g[944], addUndoState=False)
    s1.Line(point1=(-5328.0, -46.0), point2=(-5328.0, 46.0))
    s1.VerticalConstraint(entity=g[945], addUndoState=False)
    s1.ParallelConstraint(entity1=g[473], entity2=g[945], addUndoState=False)
    s1.Line(point1=(-5448.0, 46.0), point2=(-5448.0, -46.0))
    s1.VerticalConstraint(entity=g[946], addUndoState=False)
    s1.ParallelConstraint(entity1=g[503], entity2=g[946], addUndoState=False)
    s1.Line(point1=(-5568.0, -46.0), point2=(-5568.0, 46.0))
    s1.VerticalConstraint(entity=g[947], addUndoState=False)
    s1.ParallelConstraint(entity1=g[472], entity2=g[947], addUndoState=False)
    s1.Line(point1=(-5688.0, 46.0), point2=(-5688.0, -46.0))
    s1.VerticalConstraint(entity=g[948], addUndoState=False)
    s1.ParallelConstraint(entity1=g[504], entity2=g[948], addUndoState=False)
    s1.Line(point1=(-5808.0, -46.0), point2=(-5808.0, 46.0))
    s1.VerticalConstraint(entity=g[949], addUndoState=False)
    s1.ParallelConstraint(entity1=g[471], entity2=g[949], addUndoState=False)
    s1.Line(point1=(-6045.6, 46.0), point2=(-6045.6, -46.0))
    s1.VerticalConstraint(entity=g[950], addUndoState=False)
    s1.ParallelConstraint(entity1=g[505], entity2=g[950], addUndoState=False)
    s1.Line(point1=(-6283.2, 46.0), point2=(-6283.2, -46.0))
    s1.VerticalConstraint(entity=g[951], addUndoState=False)
    s1.ParallelConstraint(entity1=g[470], entity2=g[951], addUndoState=False)
    s1.Line(point1=(-6520.8, -46.0), point2=(-6520.8, 46.0))
    s1.VerticalConstraint(entity=g[952], addUndoState=False)
    s1.ParallelConstraint(entity1=g[506], entity2=g[952], addUndoState=False)
    s1.Line(point1=(-6758.4, 46.0), point2=(-6758.4, -46.0))
    s1.VerticalConstraint(entity=g[953], addUndoState=False)
    s1.ParallelConstraint(entity1=g[507], entity2=g[953], addUndoState=False)
    s1.Line(point1=(-6996.0, -46.0), point2=(-6996.0, 46.0))
    s1.VerticalConstraint(entity=g[954], addUndoState=False)
    s1.ParallelConstraint(entity1=g[469], entity2=g[954], addUndoState=False)
    s1.Line(point1=(-7116.0, -46.0), point2=(-7116.0, 46.0))
    s1.VerticalConstraint(entity=g[955], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[814], entity2=g[955], addUndoState=False)
    s1.undo()
    session.viewports['Viewport: 1'].view.setValues(width=8138.69, height=3868.23, 
        cameraPosition=(14575, -15.6959, 3574.33), cameraTarget=(0, -15.6959, 
        3574.33))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G5']
    p.features['Shell extrude-4'].setValues(sketch=s1)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G5']
    f, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f[269], sketchUpEdge=e[295], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 46.0, 
        6754.632))
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=13638.04, gridSpacing=340.95, transform=t)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['CT G5']
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13910.6, 
        farPlane=15239.4, width=7650.37, height=3636.14, cameraPosition=(14575, 
        41, 3643.03), cameraTarget=(0, 41, 3643.03))
    s.Line(point1=(1791.6, 46.0), point2=(1791.6, -46.0))
    s.VerticalConstraint(entity=g[499], addUndoState=False)
    s.ParallelConstraint(entity1=g[51], entity2=g[499], addUndoState=False)
    s.Line(point1=(4611.6, 46.0), point2=(4611.6, -46.0))
    s.VerticalConstraint(entity=g[500], addUndoState=False)
    s.ParallelConstraint(entity1=g[50], entity2=g[500], addUndoState=False)
    p = mdb.models['Model-1'].parts['CT G5']
    f1, e1 = p.faces, p.edges
    p.ShellExtrude(sketchPlane=f1[269], sketchUpEdge=e1[295], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s, depth=11.0, 
        flipExtrudeDirection=ON)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11798.1, 
        farPlane=20094.6, width=5778.73, height=2746.57, cameraPosition=(
        -327.24, 1340.48, 19536.9), cameraUpVector=(-0.477976, 0.773054, 
        -0.417044), cameraTarget=(-186.541, -245.102, 3771.74), 
        viewOffsetX=187.77, viewOffsetY=28.6705)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12262.8, 
        farPlane=19630, width=608.612, height=289.267, viewOffsetX=189.902, 
        viewOffsetY=-147.854)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12331.5, 
        farPlane=19416.4, width=612.021, height=290.887, cameraPosition=(
        -2726.98, 3814.4, 18822.9), cameraUpVector=(-0.408417, 0.686112, 
        -0.602035), cameraTarget=(-197.135, -238.153, 3714.94), 
        viewOffsetX=190.966, viewOffsetY=-148.682)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11995.7, 
        farPlane=19752.2, width=5092.65, height=2420.48, viewOffsetX=81.2746, 
        viewOffsetY=-380.872)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12007.9, 
        farPlane=20108.8, width=5097.83, height=2422.95, cameraPosition=(
        -25.8817, 180.767, 19702.2), cameraUpVector=(-0.260956, 0.89933, 
        -0.350867), cameraTarget=(-95.5777, -146.991, 3860.44), 
        viewOffsetX=81.3572, viewOffsetY=-381.259)
    session.viewports['Viewport: 1'].view.setValues(session.views['Back'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10915.7, 
        farPlane=18234.3, width=216.093, height=102.707, viewOffsetX=-10.2655, 
        viewOffsetY=2.11111)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10908.4, 
        farPlane=18241.6, width=276.59, height=131.46, viewOffsetX=-2.66732, 
        viewOffsetY=-1.17777)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10912.5, 
        farPlane=18237.8, width=276.694, height=131.51, cameraPosition=(
        -597.816, 45.5829, 18205.9), cameraUpVector=(0.0237105, 0.999719, 
        0.00065295), cameraTarget=(0.0333557, 40.915, 3643.18), 
        viewOffsetX=-2.66832, viewOffsetY=-1.17822)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10902.5, 
        farPlane=18247.7, width=426.293, height=202.613, viewOffsetX=22.6971, 
        viewOffsetY=6.6303)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10920.2, 
        farPlane=18225.5, width=426.985, height=202.942, cameraPosition=(
        -1762.14, 403.064, 18104.5), cameraUpVector=(0.128336, 0.99169, 
        -0.00898056), cameraTarget=(-0.464539, 44.1015, 3640.78), 
        viewOffsetX=22.734, viewOffsetY=6.64106)
    p = mdb.models['Model-1'].parts['CT G5']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#fffffffc #3ff ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['CT G5']
    p.SectionAssignment(region=region, sectionName='S3/4', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['CT G5']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3 ]', ), )
    region = regionToolset.Region(faces=faces)
    p = mdb.models['Model-1'].parts['CT G5']
    p.SectionAssignment(region=region, sectionName='S1-1/4', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10882.9, 
        farPlane=18263, width=840.466, height=399.465, viewOffsetX=114.433, 
        viewOffsetY=25.625)
    session.viewports['Viewport: 1'].partDisplay.setValues(shellScaleFactor=1.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10909.9, 
        farPlane=18235.9, width=590.824, height=280.812, viewOffsetX=51.4189, 
        viewOffsetY=8.90416)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        datumPlanes=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10890.6, 
        farPlane=18255, width=854.914, height=406.332, viewOffsetX=147.67, 
        viewOffsetY=17.073)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13091, 
        farPlane=18584.9, width=7171.7, height=3408.64, viewOffsetX=659.291, 
        viewOffsetY=365.89)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p1 = mdb.models['Model-1'].parts['CT G2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    del mdb.models['Model-1'].parts['CT G2']
    p = mdb.models['Model-1'].parts['CT G5']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G5']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G4', 
        objectToCopy=mdb.models['Model-1'].parts['CT G5'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G3', 
        objectToCopy=mdb.models['Model-1'].parts['CT G4'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models['Model-1'].parts['CT G5']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G2', 
        objectToCopy=mdb.models['Model-1'].parts['CT G5'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G6']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G1', 
        objectToCopy=mdb.models['Model-1'].parts['CT G6'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['CT G1']
    p.features['Shell extrude-2'].setValues(flipExtrudeDirection=True)
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G1']
    p.features['Shell extrude-3'].setValues(flipExtrudeDirection=True)
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13268.6, 
        farPlane=18407.3, width=5721.77, height=2719.5, viewOffsetX=1969.6, 
        viewOffsetY=324.332)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13217.5, 
        farPlane=18458.4, width=6398.14, height=3040.97, viewOffsetX=33.4151, 
        viewOffsetY=27.2124)
    p1 = mdb.models['Model-1'].parts['CT G5']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13263.4, 
        farPlane=18412.5, width=5790.03, height=2751.94, viewOffsetX=49.2234, 
        viewOffsetY=-3.64636)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12654.7, 
        farPlane=19403, width=5524.3, height=2625.64, cameraPosition=(-6990.16, 
        6740.05, 16421.7), cameraUpVector=(0.871706, 0.451819, -0.189705), 
        cameraTarget=(-132.828, -73.0308, 3875.8), viewOffsetX=46.9643, 
        viewOffsetY=-3.47901)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12148.9, 
        farPlane=19580.9, width=5303.48, height=2520.69, cameraPosition=(
        6419.65, 3023.09, -10558.3), cameraUpVector=(0.1288, 0.784088, 
        0.607137), cameraTarget=(103.511, -176.324, 3608.99), 
        viewOffsetX=45.087, viewOffsetY=-3.33994)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13626.9, 
        farPlane=18049, width=856.091, height=406.891, viewOffsetX=1913.77, 
        viewOffsetY=1094.29)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13469.5, 
        farPlane=18067.5, width=846.207, height=402.194, cameraPosition=(
        8431.72, 9076.81, 13447.7), cameraUpVector=(-0.560765, 0.573082, 
        -0.597596), cameraTarget=(-222.518, -133.252, 3902.02), 
        viewOffsetX=1891.68, viewOffsetY=1081.65)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13292.5, 
        farPlane=18244.5, width=3250.36, height=1544.86, viewOffsetX=1752.9, 
        viewOffsetY=742.413)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10395.9, 
        farPlane=17673.7, width=2542.04, height=1208.21, cameraPosition=(
        -1468.53, -7022.23, 15906), cameraUpVector=(-0.809652, 0.498778, 
        -0.309328), cameraTarget=(1032.35, -1437.68, 1297.79), 
        viewOffsetX=1370.91, viewOffsetY=580.628)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10201.7, 
        farPlane=17139.4, width=2494.56, height=1185.64, cameraPosition=(
        -3754.83, 380.173, -9766.69), cameraUpVector=(0.0296317, 0.901515, 
        0.431731), cameraTarget=(3259.5, -772.199, 4386.49), 
        viewOffsetX=1345.3, viewOffsetY=569.782)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10329.5, 
        farPlane=17011.6, width=1019.02, height=484.331, viewOffsetX=1103.79, 
        viewOffsetY=568.27)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10279.4, 
        farPlane=17294.7, width=1014.08, height=481.984, cameraPosition=(
        -2177.76, 697.292, -10214.6), cameraUpVector=(-0.0160997, 0.891838, 
        0.452068), cameraTarget=(3094.81, -819.045, 4642.8), 
        viewOffsetX=1098.44, viewOffsetY=565.516)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=10065.5, 
        farPlane=17508.7, width=3922.08, height=1864.12, viewOffsetX=-12.5323, 
        viewOffsetY=271.432)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=11257.6, 
        farPlane=18713.9, width=1973.36, height=937.919, cameraPosition=(
        -2715.03, 1078.38, -11060.5), cameraUpVector=(-0.0292426, 0.909168, 
        0.415402), cameraTarget=(220.696, -24.7676, 3557.54))
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(15685.8, 
        -110.153, 3950.81), cameraUpVector=(0, 1, 0))
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13278.3, 
        farPlane=18477.5, width=5679.4, height=2699.36, cameraPosition=(
        8994.58, 9033.9, 13161.4), cameraTarget=(-149.472, -110.153, 4017.37))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13332.3, 
        farPlane=18518, width=5702.49, height=2710.34, cameraPosition=(8994.58, 
        9115.74, 13161.4), cameraTarget=(-149.472, -28.3132, 4017.37))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13311.9, 
        farPlane=18500.7, width=5693.77, height=2706.19, cameraPosition=(
        8948.25, 9129.43, 13161.4), cameraTarget=(-195.804, -14.6267, 4017.37))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14613.1, 
        farPlane=17296.7, width=6250.33, height=2970.72, cameraPosition=(
        -12682.7, 9129.43, 271.771), cameraUpVector=(0.782546, 0.57735, 
        0.232999), cameraTarget=(-288.766, -14.6267, 3961.97))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13685.7, 
        farPlane=18224.1, width=16343.3, height=7767.8, viewOffsetX=4995.24, 
        viewOffsetY=222.119)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14375.8, 
        farPlane=16282.8, width=790.772, height=375.846, viewOffsetX=-2812.43, 
        viewOffsetY=-524.136)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14332.4, 
        farPlane=18502.2, width=788.383, height=374.71, cameraPosition=(
        -10892.9, 8439.96, -5324.27), cameraUpVector=(0.705049, 0.62017, 
        0.34394), cameraTarget=(-772.059, 532.339, 3043.79), 
        viewOffsetX=-2803.93, viewOffsetY=-522.552)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13075.7, 
        farPlane=18600.2, width=8274.16, height=3932.62, viewOffsetX=-1588.56, 
        viewOffsetY=-530.521)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15015.2, 
        farPlane=19134.7, width=9501.43, height=4515.93, cameraPosition=(
        -11533.1, 9033.9, 13039.4), cameraUpVector=(0.725737, 0.57735, 
        -0.374129), cameraTarget=(-38.9375, -110.153, 7113.99), 
        viewOffsetX=-1824.18, viewOffsetY=-609.211)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14951.4, 
        farPlane=19198.4, width=8532.18, height=4055.26, viewOffsetX=1021.18, 
        viewOffsetY=-402.244)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12648.5, 
        farPlane=16816.9, width=7218.04, height=3430.66, cameraPosition=(
        -11533.1, 9033.9, 6779.07), cameraTarget=(-38.9375, -110.153, 853.657), 
        viewOffsetX=863.9, viewOffsetY=-340.29)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13188.1, 
        farPlane=16277.4, width=1704.63, height=810.194, viewOffsetX=-235.191, 
        viewOffsetY=155.304)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13298.6, 
        farPlane=18377.3, width=4724.43, height=2245.47, viewOffsetX=368.566, 
        viewOffsetY=215.313)
    p = mdb.models['Model-1'].parts['CT G4']
    s1 = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14263.8, 
        farPlane=14662.7, width=2202.66, height=1046.9, cameraPosition=(
        14463.2, 51.2819, 1073.28), cameraTarget=(0, 51.2819, 1073.28))
    s2.delete(objectList=(g[4], g[447], g[459], g[463], g[489], g[510], g[915], 
        c[1481], c[1482], c[2954], c[2955]))
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G4']
    p.features['Shell extrude-4'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13187.8, 
        farPlane=18488.1, width=6791.24, height=3227.81, viewOffsetX=1147.59, 
        viewOffsetY=642.334)
    p1 = mdb.models['Model-1'].parts['CT G3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['CT G3']
    s = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14337, 
        farPlane=14589.5, width=1342.67, height=638.158, cameraPosition=(
        14463.2, 45.901, 657.544), cameraTarget=(0, 45.901, 657.544))
    s1.delete(objectList=(g[4], g[447], g[459], g[463], g[489], g[510], g[915], 
        c[1481], c[1482], c[2954]))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G3']
    p.features['Shell extrude-4'].setValues(sketch=s1)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G3']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G3']
    p.regenerate()
    p1 = mdb.models['Model-1'].parts['CT G2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['CT G4']
    s = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14210.6, 
        farPlane=14936, width=4120.6, height=1958.48, cameraPosition=(14573.3, 
        134.931, 2013.49), cameraTarget=(0, 134.931, 2013.49))
    s2.Line(point1=(-60.0, 46.0), point2=(-60.0, -46.0))
    s2.VerticalConstraint(entity=g[1636], addUndoState=False)
    s2.PerpendicularConstraint(entity1=g[5], entity2=g[1636], addUndoState=False)
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G4']
    p.features['Shell extrude-4'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p1 = mdb.models['Model-1'].parts['CT G3']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    del mdb.models['Model-1'].parts['CT G3']
    p = mdb.models['Model-1'].parts['CT G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    del mdb.models['Model-1'].parts['CT G2']
    p = mdb.models['Model-1'].parts['CT G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['CT G4']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14347.5, 
        farPlane=14799.1, width=2511.79, height=1193.83, cameraPosition=(
        14573.3, 59.1425, 1279.05), cameraTarget=(0, 59.1425, 1279.05))
    s1.delete(objectList=(g[4], g[398], g[447], c[1480], c[1481]))
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G4']
    p.features['Shell extrude-2'].setValues(sketch=s1)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12562.6, 
        farPlane=19340.6, width=5373.28, height=2553.87, cameraPosition=(
        6697.51, 6580.04, 16566.9), cameraUpVector=(-0.549243, 0.682513, 
        -0.482191))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13453, 
        farPlane=18388.5, width=5754.15, height=2734.89, cameraPosition=(
        -1738.81, 13099.4, 12596.9), cameraUpVector=(0.968531, -0.16732, 
        -0.18426), cameraTarget=(-212.223, -63.7144, 3922.53))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15549.7, 
        farPlane=16646.5, width=6650.95, height=3161.13, cameraPosition=(
        -16011.8, 1736.59, 3565.04), cameraUpVector=(0.441673, 0.897153, 
        0.00640221), cameraTarget=(-286.422, -122.784, 3875.58))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15220.9, 
        farPlane=16975.2, width=10415.1, height=4950.21, viewOffsetX=-1591.22, 
        viewOffsetY=-128.928)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13320.5, 
        farPlane=18355.4, width=5034.26, height=2392.73, viewOffsetX=-242.456, 
        viewOffsetY=-136.48)
    p = mdb.models['Model-1'].parts['CT G4']
    s = p.features['Shell extrude-4'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-4'], filter=COPLANAR_EDGES)
    s2.delete(objectList=(g[469], g[809], g[823], g[954], c[3110], c[3111]))
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G4']
    p.features['Shell extrude-4'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G3', 
        objectToCopy=mdb.models['Model-1'].parts['CT G4'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='CT G2', 
        objectToCopy=mdb.models['Model-1'].parts['CT G4'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].parts['CT G4']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s1 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s1, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    s1.Line(point1=(-1189.2, 46.0), point2=(-1189.2, -46.0))
    s1.VerticalConstraint(entity=g[1748], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[306], entity2=g[1748], addUndoState=False)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G4']
    p.features['Shell extrude-2'].setValues(sketch=s1)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G4']
    p.regenerate()
    p1 = mdb.models['Model-1'].parts['CT G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13219.6, 
        farPlane=18456.3, width=5654.29, height=2687.43, viewOffsetX=-2.29761, 
        viewOffsetY=-1.41461)
    p = mdb.models['Model-1'].parts['CT G1']
    s = p.features['Shell extrude-2'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell extrude-2'], filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14164.4, 
        farPlane=14982.2, width=4663.43, height=2216.48, cameraPosition=(
        14573.3, 43.0728, 5026.8), cameraTarget=(0, 43.0728, 5026.8))
    s2.delete(objectList=(g[319], g[381], g[410], c[1332], c[1333]))
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['CT G1']
    p.features['Shell extrude-2'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    p = mdb.models['Model-1'].parts['CT G1']
    p.regenerate()
    mdb.save()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['CT G1']
    a.Instance(name='CT G1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G2']
    a.Instance(name='CT G2-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G3']
    a.Instance(name='CT G3-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G4']
    a.Instance(name='CT G4-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G5']
    a.Instance(name='CT G5-1', part=p, dependent=ON)
    p1 = a.instances['CT G2-1']
    p1.translate(vector=(29.04, 0.0, 0.0))
    p1 = a.instances['CT G3-1']
    p1.translate(vector=(58.08, 0.0, 0.0))
    p1 = a.instances['CT G4-1']
    p1.translate(vector=(87.12, 0.0, 0.0))
    p1 = a.instances['CT G5-1']
    p1.translate(vector=(116.16, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13632.3, 
        farPlane=18083.7, width=571.911, height=271.823, viewOffsetX=-2037.12, 
        viewOffsetY=-1239.12)
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G1-1']
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G5-1']
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G4-1']
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G3-1']
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G2-1']
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G1']
    a1.Instance(name='CT G1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G2']
    a1.Instance(name='CT G2-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G3']
    a1.Instance(name='CT G3-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G4']
    a1.Instance(name='CT G4-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G5']
    a1.Instance(name='CT G5-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G6']
    a1.Instance(name='CT G6-1', part=p, dependent=ON)
    p1 = a1.instances['CT G2-1']
    p1.translate(vector=(29.04, 0.0, 0.0))
    p1 = a1.instances['CT G3-1']
    p1.translate(vector=(58.08, 0.0, 0.0))
    p1 = a1.instances['CT G4-1']
    p1.translate(vector=(87.12, 0.0, 0.0))
    p1 = a1.instances['CT G5-1']
    p1.translate(vector=(116.16, 0.0, 0.0))
    p1 = a1.instances['CT G6-1']
    p1.translate(vector=(145.2, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13384.5, 
        farPlane=18342.1, width=3884.98, height=1846.49, viewOffsetX=-728.564, 
        viewOffsetY=-445.226)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13540.9, 
        farPlane=18145.8, width=1435.86, height=682.45, viewOffsetX=-1746.15, 
        viewOffsetY=-981.445)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G1-1', ), vector=(50.0, 50.0, 0.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G1-1', ), vector=(-50.0, 0.0, 50.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13465.3, 
        farPlane=18205.6, width=2026.62, height=963.234, viewOffsetX=-1600.89, 
        viewOffsetY=-993.862)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G2-1', ), vector=(-40.0, 0.0, 40.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G1-1', ), vector=(-600.0, 0.0, 600.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12925.3, 
        farPlane=18743.6, width=4366.23, height=2075.22, viewOffsetX=-529.067, 
        viewOffsetY=-454.516)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G2-1', ), vector=(-480.0, 0.0, 48.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13051.4, 
        farPlane=18617.4, width=2384.38, height=1133.27, viewOffsetX=-1557.85, 
        viewOffsetY=-848.6)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G3-1', ), vector=(-360.0, 0.0, 360.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12608.5, 
        farPlane=19034.2, width=7131.37, height=3389.47, viewOffsetX=665.868, 
        viewOffsetY=85.4631)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G3-1', ), vector=(-360.0, 0.0, 360.0))
    a = mdb.models['Model-1'].rootAssembly
    a.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G1-1']
    a = mdb.models['Model-1'].rootAssembly
    a.deleteFeatures(('CT G2-1', 'CT G3-1', 'CT G4-1', 'CT G5-1', 'CT G6-1', ))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G1']
    a1.Instance(name='CT G1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G2']
    a1.Instance(name='CT G2-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G3']
    a1.Instance(name='CT G3-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G4']
    a1.Instance(name='CT G4-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G5']
    a1.Instance(name='CT G5-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G6']
    a1.Instance(name='CT G6-1', part=p, dependent=ON)
    p1 = a1.instances['CT G2-1']
    p1.translate(vector=(29.04, 0.0, 0.0))
    p1 = a1.instances['CT G3-1']
    p1.translate(vector=(58.08, 0.0, 0.0))
    p1 = a1.instances['CT G4-1']
    p1.translate(vector=(87.12, 0.0, 0.0))
    p1 = a1.instances['CT G5-1']
    p1.translate(vector=(116.16, 0.0, 0.0))
    p1 = a1.instances['CT G6-1']
    p1.translate(vector=(145.2, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13392.1, 
        farPlane=18334.4, width=3351.62, height=1592.99, viewOffsetX=-991.911, 
        viewOffsetY=-532.729)
    a = mdb.models['Model-1'].rootAssembly
    a.deleteFeatures(('CT G2-1', 'CT G1-1', 'CT G3-1', 'CT G5-1', 'CT G4-1', 
        'CT G6-1', ))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G1']
    a1.Instance(name='CT G1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G2']
    a1.Instance(name='CT G2-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G3']
    a1.Instance(name='CT G3-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G4']
    a1.Instance(name='CT G4-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G5']
    a1.Instance(name='CT G5-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['CT G6']
    a1.Instance(name='CT G6-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13112.3, 
        farPlane=18565.6, width=7778.38, height=3696.99, viewOffsetX=914.835, 
        viewOffsetY=-196.86)
    a = mdb.models['Model-1'].rootAssembly
    a.deleteFeatures(('CT G1-1', 'CT G2-1', 'CT G3-1', 'CT G4-1', 'CT G5-1', 
        'CT G6-1', ))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G1']
    a1.Instance(name='CT G1-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13083.7, 
        farPlane=18594.1, width=8156.34, height=3876.62, viewOffsetX=415.17, 
        viewOffsetY=117.643)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=12674, 
        farPlane=19011.4, width=9094.24, height=4322.4, viewOffsetX=1601.27, 
        viewOffsetY=836.671)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G1-1', ), vector=(-600.0, 0.0, 600.0))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G2']
    a1.Instance(name='CT G2-1', part=p, dependent=ON)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G2-1', ), vector=(-480.0, 0.0, 480.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14178.1, 
        farPlane=20340.2, width=7913.68, height=3761.29, viewOffsetX=512.723, 
        viewOffsetY=205.94)
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G3']
    a1.Instance(name='CT G3-1', part=p, dependent=ON)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G3-1', ), vector=(-360.0, 0.0, 360.0))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G4']
    a1.Instance(name='CT G4-1', part=p, dependent=ON)
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G5']
    a1.Instance(name='CT G5-1', part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    del a.features['CT G5-1']
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G4-1', ), vector=(-240.0, 0.0, 240.0))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G5']
    a1.Instance(name='CT G5-1', part=p, dependent=ON)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G5-1', ), vector=(-120.0, 0.0, 120.0))
    a1 = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['CT G6']
    a1.Instance(name='CT G6-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14611.4, 
        farPlane=19893.3, width=1821.73, height=865.851, viewOffsetX=-1717.77, 
        viewOffsetY=-1093.62)
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    session.viewports['Viewport: 1'].view.setValues(session.views['Back'])
    session.viewports['Viewport: 1'].view.setValues(session.views['Top'])
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14577, 
        farPlane=19958.9, width=2485.4, height=1181.29, viewOffsetX=-1181.47, 
        viewOffsetY=-640.093)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14427.5, 
        farPlane=20707.1, width=2459.92, height=1169.17, cameraPosition=(
        9732.03, 7419.24, 16343.5), cameraUpVector=(-0.451971, 0.703893, 
        -0.547957), cameraTarget=(-258.173, -92.8725, 4429.4), 
        viewOffsetX=-1169.35, viewOffsetY=-633.529)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13679.4, 
        farPlane=21403.1, width=11852.5, height=5633.37, viewOffsetX=-2904.61, 
        viewOffsetY=-2101)
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14202.1, 
        farPlane=20277.3, width=936.988, height=445.341, viewOffsetX=1907.16, 
        viewOffsetY=838.161)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14473.7, 
        farPlane=20257, width=954.912, height=453.86, cameraPosition=(10481.4, 
        7296.38, 15516), cameraUpVector=(-0.498071, 0.704695, -0.505302), 
        cameraTarget=(-325.311, -185.831, 4360.92), viewOffsetX=1943.64, 
        viewOffsetY=854.195)
    session.viewports['Viewport: 1'].assemblyDisplay.geometryOptions.setValues(
        datumPlanes=OFF)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14386.9, 
        farPlane=20324.2, width=2149.11, height=1021.45, viewOffsetX=1993.55, 
        viewOffsetY=780.855)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14279, 
        farPlane=20374.4, width=2132.99, height=1013.79, cameraPosition=(
        11026.1, 5889.14, 15749), cameraUpVector=(-0.454746, 0.763883, 
        -0.457918), cameraTarget=(-357.358, -210.556, 4329.08), 
        viewOffsetX=1978.59, viewOffsetY=774.997)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14394.3, 
        farPlane=20259, width=663.609, height=315.406, viewOffsetX=2206.81, 
        viewOffsetY=855.335)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14328.1, 
        farPlane=20255.4, width=660.557, height=313.956, cameraPosition=(
        10738.9, 6025.59, 15899.7), cameraUpVector=(-0.466017, 0.756267, 
        -0.459226), cameraTarget=(-363.169, -258.302, 4304.01), 
        viewOffsetX=2196.66, viewOffsetY=851.402)
    session.viewports['Viewport: 1'].view.setValues(session.views['Left'])
    session.viewports['Viewport: 1'].view.setValues(session.views['Top'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15519.3, 
        farPlane=16168.1, width=3220.68, height=1530.75, viewOffsetX=301.615, 
        viewOffsetY=3460.22)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G5-1', ), vector=(240.0, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15539.4, 
        farPlane=16148, width=3430.7, height=1630.58, viewOffsetX=260.562, 
        viewOffsetY=3470.81)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 4231.86), cameraTarget=(-239.4, 46, 4231.86), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 4492.15), cameraTarget=(-239.4, 46, 4492.15), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 4728.93), cameraTarget=(-239.4, 46, 4728.93), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 4933.8), cameraTarget=(-239.4, 46, 4933.8), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 5142.03), cameraTarget=(-239.4, 46, 5142.03), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 5315), cameraTarget=(-239.4, 46, 5315), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 5489.65), cameraTarget=(-239.4, 46, 5489.65), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 5672.69), cameraTarget=(-239.4, 46, 5672.69), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 5870.85), cameraTarget=(-239.4, 46, 5870.85), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6072.36), cameraTarget=(-239.4, 46, 6072.36), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6226.85), cameraTarget=(-239.4, 46, 6226.85), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6401.5), cameraTarget=(-239.4, 46, 6401.5), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6579.5), cameraTarget=(-239.4, 46, 6579.5), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6807.88), cameraTarget=(-239.4, 46, 6807.88), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15523.5, 
        farPlane=16163.9, width=3427.19, height=1628.91, cameraPosition=(
        -239.4, 15889.7, 6999.32), cameraTarget=(-239.4, 46, 6999.32), 
        viewOffsetX=260.295, viewOffsetY=3467.25)
    session.viewports['Viewport: 1'].view.setValues(width=3427.19, height=1628.91, 
        cameraPosition=(26.2641, 46, 19304.3), cameraUpVector=(0, 1, 0), 
        cameraTarget=(26.2641, 46, 3460.55), viewOffsetX=0, viewOffsetY=0)
    session.viewports['Viewport: 1'].view.setValues(session.views['Bottom'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=14893.9, 
        farPlane=16792.6, width=10651.6, height=5062.58, viewOffsetX=226.75, 
        viewOffsetY=1114.12)
    session.viewports['Viewport: 1'].view.setValues(session.views['Top'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15448.3, 
        farPlane=16238.2, width=4105.18, height=1951.15, viewOffsetX=223.06, 
        viewOffsetY=2773.27)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G4-1', ), vector=(480.0, 0.0, 0.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G3-1', ), vector=(720.0, 0.0, 0.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G2-1', ), vector=(960.0, 0.0, 0.0))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.translate(instanceList=('CT G1-1', ), vector=(1200.0, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15251, 
        farPlane=16435.5, width=7248.3, height=3445.04, viewOffsetX=505.094, 
        viewOffsetY=3347.52)
    mdb.save()
    mdb.save()
    session.viewports['Viewport: 1'].view.setValues(nearPlane=15438.4, 
        farPlane=16248, width=4221.5, height=2006.43, viewOffsetX=550.653, 
        viewOffsetY=2795.59)
    p = mdb.models['Model-1'].parts['CT G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p1 = mdb.models['Model-1'].parts['CT G5']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p1 = mdb.models['Model-1'].parts['CT G4']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        datumPointLabels=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        datumPlanes=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=13471.5, 
        farPlane=18203.8, width=1825.02, height=794.497, viewOffsetX=1402.37, 
        viewOffsetY=814.35)
    mdb.save()
    mdb.save()
def GirderShell1():
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
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(-10.0, 0.0), point2=(0.0, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(10.0, 0.0))
    s.HorizontalConstraint(entity=g[3], addUndoState=False)
    s.ParallelConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(0.0, 20.0))
    s.VerticalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[4], addUndoState=False)
    s.Line(point1=(0.0, 20.0), point2=(-10.0, 20.0))
    s.HorizontalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(0.0, 20.0), point2=(10.0, 20.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[6], addUndoState=False)
    s.EqualLengthConstraint(entity1=g[2], entity2=g[5])
    s.EqualLengthConstraint(entity1=g[5], entity2=g[3], addUndoState=False)
    s.EqualLengthConstraint(entity1=g[3], entity2=g[6], addUndoState=False)
    s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-3.69686889648438, 
        -3.1705150604248), value=10.0)
    s.ObliqueDimension(vertex1=v[1], vertex2=v[3], textPoint=(3.75900268554688, 
        8.57904052734375), value=20.0)
    p = mdb.models['Model-1'].Part(name='G1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['G1']
    p.BaseShellExtrude(sketch=s, depth=40.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['G1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((29000.0, 0.3), ))
    mdb.models['Model-1'].HomogeneousShellSection(name='Web', preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=0.25, 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    mdb.models['Model-1'].HomogeneousShellSection(name='Flange', preIntegrate=OFF, 
        material='Steel', thicknessType=UNIFORM, thickness=0.35, 
        thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    p = mdb.models['Model-1'].parts['G1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1d ]', ), )
    region = p.Set(faces=faces, name='Flange')
    p = mdb.models['Model-1'].parts['G1']
    p.SectionAssignment(region=region, sectionName='Flange', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['G1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    region = p.Set(faces=faces, name='Web')
    p = mdb.models['Model-1'].parts['G1']
    p.SectionAssignment(region=region, sectionName='Web', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].parts['G1'].sectionAssignments[0].setValues(
        offsetType=TOP_SURFACE, offsetField='', offset=0.0)
    session.viewports['Viewport: 1'].partDisplay.setValues(renderShellThickness=ON)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=80.1213, 
        farPlane=133.354, width=64.1602, height=32.6048, cameraPosition=(
        2.09447, 29.6578, 124.906), cameraUpVector=(-0.264498, 0.822531, 
        -0.503472), cameraTarget=(-0.00461483, 8.47763, 21.527))
    p = mdb.models['Model-1'].parts['G1']
    f = p.faces
    p.RepairFaceNormals(faceList = f[3:5])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=77.6961, 
        farPlane=135.409, width=62.2182, height=31.6179, cameraPosition=(
        56.9607, 36.1383, 106.191), cameraUpVector=(-0.386581, 0.818979, 
        -0.424062), cameraTarget=(0.607108, 8.54988, 21.3183))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=75.9594, 
        farPlane=137.145, width=82.8822, height=42.1188, viewOffsetX=3.56744, 
        viewOffsetY=-0.176565)
    p = mdb.models['Model-1'].parts['G1']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=20.0)
    session.viewports['Viewport: 1'].view.fitView()
    p = mdb.models['Model-1'].parts['G1']
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1f ]', ), )
    d1 = p.datums
    p.PartitionFaceByDatumPlane(datumPlane=d1[5], faces=pickedFaces)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=80.062, 
        farPlane=139.672, width=71.5544, height=36.3623, viewOffsetX=7.11179, 
        viewOffsetY=0.811227)
    p = mdb.models['Model-1'].parts['G1']
    f1, e = p.faces, p.edges
    t = p.MakeSketchTransform(sketchPlane=f1[3], sketchUpEdge=e[12], 
        sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0.0, 10.0, 
        30.0))
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=89.44, gridSpacing=2.23, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models['Model-1'].parts['G1']
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=39.0607, 
        farPlane=74.0764, width=83.0119, height=42.1848, cameraPosition=(
        56.5685, 11.6447, 20.9528), cameraTarget=(0, 11.6447, 20.9528))
    s1.Line(point1=(10.0, 10.0), point2=(10.0, -10.0))
    s1.VerticalConstraint(entity=g[18], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[4], entity2=g[18], addUndoState=False)
    p = mdb.models['Model-1'].parts['G1']
    f, e1 = p.faces, p.edges
    p.ShellExtrude(sketchPlane=f[3], sketchUpEdge=e1[12], sketchPlaneSide=SIDE1, 
        sketchOrientation=RIGHT, sketch=s1, depth=5.0, 
        flipExtrudeDirection=OFF)
    s1.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].HomogeneousShellSection(name='Stiffener', 
        preIntegrate=OFF, material='Steel', thicknessType=UNIFORM, 
        thickness=0.1, thicknessField='', nodalThicknessField='', 
        idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, numIntPts=5)
    p = mdb.models['Model-1'].parts['G1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Stiffener')
    p = mdb.models['Model-1'].parts['G1']
    p.SectionAssignment(region=region, sectionName='Stiffener', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)


