# This script downloads selected Snohomish County assessor and GIS files for use in the parcel database
#ftp://ftp.snoco.org/Assessor/PropertySales/Property_Class_Codes_2015-10-27.pdf


import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import glob
import zipfile

# Select output directory
outDir = r'C:\Users\Christy\Desktop\python_scripts\test'

# Inputs
assrroll = "assr_roll"
propChar = " "
propCharDoc = "Property Characteristics Extract"
propSales = "Property_Class_Codes*" #wildcard
shapes = "parcels"

# dictionary containing url headers
def urlDict(x):
    return {
        'assr_roll': 'ftp://ftp.snoco.org/Assessor/Assessor_roll/MS_Access/',
        'prop_char': 'ftp://ftp.snoco.org/Assessor/prop_characteristics/',
        'prop_sales': 'ftp://ftp.snoco.org/Assessor/PropertySales/',
        'gis': 'ftp://ftp.snoco.org/Assessor/shapefiles/'
    }[x]

# function to download data
def downloadData(assessordata, dictterm, ext):
    urlpart = urlDict(dictterm)
    if assessordata == propChar:
        url = urllib2.urlopen(urlpart).read()
        soup = BeautifulSoup(url, "lxml")
        soupstr = str(soup)
        searchObj = re.findall(r'(SnohomishCo.*TEXT.*AV)', soupstr)
        for obj in searchObj:
            assrFilePath = urlpart + obj + "." + ext
            urllib.urlretrieve(assrFilePath, os.path.join(outDir, (obj + "." + ext)))
            print obj + "." + ext + " downloaded" 
    else: 
        assrFilePath = urlpart + assessordata + "." + ext
        urllib.urlretrieve(assrFilePath, os.path.join(outDir, (assessordata + "." + ext)))
        print assessordata + "." + ext + " downloaded"

# function to unzip files in output directory
def unzipFiles(directory):
    listfiles = glob.glob((directory + '/*.zip'))
    for afile in listfiles:
        a = os.path.basename(afile)
        fldr = os.path.splitext(a)[0] 
        zip = zipfile.ZipFile((afile))  
        zip.extractall(os.path.join(directory, fldr))
        print "extracted " + afile

# download data
downloadData(assrroll, 'assr_roll', 'zip')
downloadData(propChar, 'prop_char', 'zip')
downloadData(propCharDoc, 'prop_char', 'doc')
downloadData(shapes, 'gis', 'zip')

# extract zip files to output directory
unzipFiles(outDir)
