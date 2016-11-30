# This script downloads selected Kitsap County assessor and GIS files for use in the parcel database
# Occassional timeout error where existing connection is closed by the remote host 

import os
import urllib
import glob
import zipfile

# Select output directory
outDir = r'C:\Users\Christy\Desktop\python_scripts\test'

# Inputs
assrdata = ["Parcels", "Dwellings", "MH", "Other_res_imps", "Features"]
assrdata2 = ["Ext_features", "Comml_Imps", "Land_detail", "Cad_actions", "Plats"]
assrdata3 = ["Property_addresses", "Codes", "Valuations", "Land_influence"]

prclshps = ["parcels", "siteaddr", "parcell"]
listbls = ["flatats", "main", "building", "land"]

# dictionary containing urlparts
def urlzipDict(x):
    return {
        'prclshps': 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/parcel/',
        'listbls': 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/atsinfo/',
        'txt': 'http://www.kitsapgov.com/assr/data_download/',
        'docx': 'http://www.kitsapgov.com/assr/data_download/file_descriptions/'
    }[x]

# function to download assessor data
def downloadData(assessordata, alist, ext):
    urlpart = urlzipDict(alist)
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
allAssrdata = assrdata + assrdata2 + assrdata3
for data in allAssrdata:
    downloadData(data, 'docx', 'docx')
    
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

# list and extract zipfiles in output directory
unzipFiles(outDir)
    























