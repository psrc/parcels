# This script downloads selected Kitsap County assessor and GIS files for use in the parcel database

import os
import urllib

# Select output directory
outDir = r'C:\Users\Christy\Desktop\python_scripts\test'

# Inputs
assrdata = ["Parcels", "Dwellings", "MH", "Other_res_imps", "Features"]
assrdata2 = ["Ext_features", "Comml_Imps", "Land_detail", "Cad_actions", "Plats"]
assrdata3 = ["Property_addresses", "Codes", "Valuations", "Land_influence"]

prclshps = ["parcels", "siteaddr", "parcell"]
listbls = ["flatats", "main", "building", "land"]

# function to download data
def downloadData(assessordata, ext):
    if ext == 'txt':
        urlpart = 'http://www.kitsapgov.com/assr/data_download/'
    if ext == 'docx':
        urlpart = 'http://www.kitsapgov.com/assr/data_download/file_descriptions/'
        assessordata = assessordata.lower()
    if ext == 'zip': 
        if assessordata == prclshps:
            urlpart = 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/parcel/'
        if assessordata == listbls:
            urlpart = 'ftp://kcftp2.co.kitsap.wa.us/gis/datacd/arcview/layers/atsinfo/'           
    assrFilePath = urlpart + assessordata + "." + ext
    urllib.urlretrieve(assrFilePath, os.path.join(outDir, (assessordata + "." + ext)))
    print assessordata + "." + ext + " downloaded"

# download data
allAssrdata = assrdata + assrdata2 + assrdata3
for data in allAssrdata:
    downloadData(data, 'docx')
    
for data in assrdata:
    downloadData(data, 'txt')

for data in assrdata2:
    downloadData(data, 'txt')

for data in assrdata3:
    downloadData(data, 'txt')  
    
for data in prclshps:
    downloadData(data, 'zip')

for data in listbls:
    downloadData(data, 'zip')
    























