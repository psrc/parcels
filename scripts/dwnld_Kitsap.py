import os
import urllib

outDir = r'C:\Users\Christy\Desktop\python_scripts\test'

assrdata = ["Parcels", "Dwellings", "MH", "Other_res_imps", "Features", "Ext_features", "Comml_Imps", "Land_detail", "Cad_actions", "Plats", "Property_addresses", "Codes", "Valuations", "Land_influence"]
#assrdata = ["Parcels", "Dwellings", "MH", "Other_res_imps", "Features"]
#assrdata = ["Ext_features", "Comml_Imps", "Land_detail", "Cad_actions", "Plats", "Property_addresses", "Codes", "Valuations", "Land_influence"]
#extension = [".txt", ".docx"] # depending on extension file is stored in separate places, and assrdata will be lowercase

def downloadData(assessordata, ext):
    if ext == 'txt':
        urlpart = 'http://www.kitsapgov.com/assr/data_download/'
    if ext == 'docx':
        urlpart = 'http://www.kitsapgov.com/assr/data_download/file_descriptions/'
        assessordata = assessordata.lower()    
    assrFilePath = urlpart + assessordata + "." + ext
    urllib.urlretrieve(assrFilePath, os.path.join(outDir, (assessordata + "." + ext)))
    print assessordata + "." + ext + " downloaded"

for data in assrdata:
    downloadData(data, 'docx')
    
for data in assrdata:
    downloadData(data, 'txt')
























