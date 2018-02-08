# This script downloads selected Pierce County assessor and GIS files for use in the parcel database

import os
import urllib
import glob
import zipfile

# Select output directory
outDir = r'J:\Projects\UrbanSim\NEW_DIRECTORY\Databases\Access\Parcels\Pierce\2018\dwnld_2018_02_07'

# Inputs
assrdata = ["appraisal_account", "improvement", "improvement_builtas", "improvement_detail", "land_attribute", "sale", "seg_merge", 
            "tax_account", "tax_description"]
shapes = "Tax-Parcels-3159d197629543c99e288ac5ec61878e_0-fgdb"

# dictionary containing url headers
def urlDict(x):
    return {
        'assrdata': 'https://online.co.pierce.wa.us/datamart/',
        'assrdesc': 'https://online.co.pierce.wa.us/cfapps/atr/datamart/metadata/',
        'gis': 'http://gisdata-piercecowa.opendata.arcgis.com/datasets/tax-parcels/'
    }[x]

# function to download data
def downloadData(assessordata, dictterm, ext):
    print "downloading " + dictterm
    urlpart = urlDict(dictterm)               
    assrFilePath = urlpart + assessordata + "." + ext
    urllib.urlretrieve(assrFilePath, os.path.join(outDir, (assessordata + "." + ext)))
    print assessordata + "." + ext + " downloaded"

# function to unzip files in output directory
def unzipFiles(directory):
    print "extracting zip files"
    listfiles = glob.glob((directory + '/*.zip'))
    for afile in listfiles:
        a = os.path.basename(afile)
        fldr = os.path.splitext(a)[0] 
        zip = zipfile.ZipFile((afile))  
        zip.extractall(os.path.join(directory, fldr))
        print "extracted " + afile

# download data
for data in assrdata:        
    downloadData(data, 'assrdata', 'zip')

for data in assrdata:
    downloadData(data, 'assrdesc', 'pdf')
    
downloadData(shapes, 'gis', 'zip')

# extract zip files to output directory
unzipFiles(outDir)