# This script downloads selected King County assessor and GIS files for use in the parcel database

import os
import urllib
import glob
import zipfile

# Select output directory
outDir = r'J:\Projects\UrbanSim\NEW_DIRECTORY\Databases\Access\Parcels\King\2018\dwnld_2018_02_07'

# Inputs
assrdata = 'http://aqua.kingcounty.gov/extranet/assessor/cd.zip'
shapes = ['parcel_SHP', 'parcel_address_SHP']#'parcel_SHP', 

# function to download data
def downloadAssessorData(assessordata):      
    urllib.urlretrieve(assessordata, os.path.join(outDir, "cd.zip"))
    print "assessor data downloaded"

# function to download shapefiles
def downloadGISData(shapefiles):
    urlpart = 'ftp://ftp.kingcounty.gov/gis-web/GISData/'
    assrFilePath = urlpart + shapefiles + ".zip"
    urllib.urlretrieve(assrFilePath, os.path.join(outDir, (shapefiles + ".zip")))
    print shapefiles + ".zip downloaded"

# function to list and extract zip files in output directory
def unzipFiles(directory):
    files = glob.glob((directory + '/*.zip'))
    for file in files:
        zip = zipfile.ZipFile((file))  
        zip.extractall(directory)
        print "extracted " + file

# download assessor files
print "downloading assessor data"
downloadAssessorData(assrdata)

# download shapefiles
print "downloading parcel shapefiles"
for shape in shapes:
    downloadGISData(shape)

# extract zip files to output directory    
#print "extracting zip files"
#unzipFiles(outDir)
   


      