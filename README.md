Bridge Building with Python and Abaqus

Three scripts are necessary to run the program in Abaqus.
  1. InputPreprocessor.py
        - Reads an input .csv file of the correct format and outputs a dictionary with necessary data for later calculations. 
        - Uses dictionary of data (System_info) to run geometry calculations for girder sketch nodes, splice coordinates, and bracing coordinates.
        - This module is imported into the other two scripts for use, so this file needs to be in the same directory as the other two scripts.
  3. InputDebug.py
        - Intended to be used prior to running AbaqusMacro.py as a safety net and visualization tool to verify the bridge data you will run in Abaqus. It will check for DataType errors, UnacceptedEntry strings, ListLengthErrors, and DataErrors that do not make logical sense for bridge geometry. Some data type errors may be caught during the execution of the InputPreprocessor.py functions.
        - Checks that outputs from InputPreprocessor.py for data errors and plots defined bridge bracings to allow for visual check.
        - This code is NOT compatible with Python 2.7, so it will NOT run with Abaqus. It is intended to be run in a seperate IDE, like Spyder.
        - Can change file name, input row, and debugging setting.
  5. AbaqusMacro.py
        - Run within Abaqus, this generates the geometry of the bridge, runs FEA in Abaqus, and outputs the FEA results into an excel file in the working directory.
        - Analysis is limited to 1000 nodes if using the student edition.
        - This code is compatible with Python 2.7, because Abaqus is only compatible with Python 2.7.
        - Can change file name, input row, and Abaqus working directory (in order to get results).

Refer to example input files to ensure data format is correct prior to use. 

Example Input File: https://docs.google.com/spreadsheets/d/1d6-8EyLCfyEOkocTmbgUMpCe0gZMhizHeagAkf8dsB4/edit?usp=sharing

Documentation: https://docs.google.com/document/d/10zO6yMPpG-RnKnAKklPowEqYQDxbSeN2/edit?usp=sharing&ouid=116375287709933268163&rtpof=true&sd=true

Presentation: https://docs.google.com/presentation/d/181gSlfImbQCvOoHU36N8nUIlTq_se1nZ1AS3RKY53z8/edit?usp=sharing
