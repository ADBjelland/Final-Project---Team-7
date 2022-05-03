Bridge Building with Python and Abaqus

Three scripts are necessary to run the program in Abaqus.
  1. InputPreprocessor.py
        - Reads an input .csv file of the correct format and outputs a dictionary with necessary data for later calculations. 
        - Uses dictionary of data (System_info) to run geometry calculations for girder sketch nodes, splice coordinates, and bracing coordinates.
        - This module is imported into the other two scripts for use.
  3. InputDebug.py
        - Intended to be used prior to running AbaqusMacro.py.
        - Checks that outputs from InputPreprocessor.py for data errors and plots defined bridge bracings to allow for visual check.
        - Can change file name, input row, and debugging setting.
  5. AbaqusMacro.py
        - Run within Abaqus, this generates the geometry of the bridge and runs FEA in Abaqus.
        - Can change file name and input row.

Refer to example input files to ensure data format is correct prior to use. 

Documentation: https://docs.google.com/document/d/10zO6yMPpG-RnKnAKklPowEqYQDxbSeN2/edit?usp=sharing&ouid=116375287709933268163&rtpof=true&sd=true
Presentation: https://docs.google.com/presentation/d/181gSlfImbQCvOoHU36N8nUIlTq_se1nZ1AS3RKY53z8/edit?usp=sharing
