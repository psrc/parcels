# This script downloads selected Kitsap County assessor and GIS files for use in the parcel database
# Occassional timeout error where existing connection is closed by the remote host 

import os
import urllib
import glob
import zipfile

# Select output directory
outDir = r'J:\Projects\UrbanSim\NEW_DIRECTORY\Databases\Access\Parcels\Kitsap\2018\dwnld_2018_02_07'

# Inputs
assrdata = ["Parcels", "Dwellings", "MH", "Other_res_imps", "Features"]
assrdata2 = ["Ext_features", "Comml_Imps", "Land_detail", "Cad_actions", "Plats"]
assrdata3 = ["Property_addresses", "Codes", "Valuations", "Land_influence"]

prclshps = ["siteaddr", "parcell"]#"parcels", 
listbls = [ "main", "building", "land"]#"flatats",

# dictionary containing url headers
def urlDict(x):
    return {
        'prclshps': 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/parcel/',
        'listbls': 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/atsinfo/',
        #'txt': 'http://www.kitsapgov.com/assr/data_download/',
        'txt': 'https://spf.kitsapgov.com/assessor/Documents/',
        #'docx': 'http://www.kitsapgov.com/assr/data_download/file_descriptions/'
        'docx': 'https://spf.kitsapgov.com/assessor/Documents/'
    }[x]

# function to download data
def downloadData(assessordata, dictterm, ext):
    urlpart = urlDict(dictterm)
    if ext == 'docx':
        assessordata = assessordata.lower()                
    assrFilePath = urlpart + assessordata + "." + ext
    urllib.urlretrieve(assrFilePath, os.path.join(outDir, (assessordata + "." + ext)))
    print assessordata + "." + ext + " downloaded"

# function to unzip files in output directory
def unzipFiles(directory):
    files = glob.glob((directory + '/*.zip'))
    for file in files:
        zip = zipfile.ZipFile((file))  
        zip.extractall(directory)
        print "extracted " + file
        
# download data
#allAssrdata = assrdata + assrdata2 + assrdata3
#for data in allAssrdata:
#    downloadData(data, 'docx', 'docx')
    
for data in assrdata:
    downloadData(data, 'txt', 'txt')

for data in assrdata2:
    downloadData(data, 'txt', 'txt')

for data in assrdata3:
    downloadData(data, 'txt', 'txt')  
    
for data in prclshps:
    downloadData(data, 'prclshps', 'zip')

for data in listbls:
    downloadData(data, 'listbls', 'zip')

# extract zip files to output directory
#unzipFiles(outDir)
    























