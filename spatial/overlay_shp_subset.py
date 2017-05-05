# This script will create a new file gdb then subset each overlay feature by county and export county feature to new file gdb
# overlay features such as 'uga', 'micen', 'urbcen', and 'school districts' are not processed

import arcpy, os

# Dictionary containing joining features
shpDict = {
        'juris': 'W:\\geodata\\political\\PSRC_region.gdb\\psrc_region',
        'zipcode': 'W:\\geodata\\political\\zipcode.shp',
        'taz': 'J:\\Staff\\Christy\\baseyear\\shapes\\overlay_shapes.gdb\\taz2010_to_tad2010',
        'faz': 'W:\\geodata\\forecast\\FAZ_2010.shp',
        'tract': 'W:\\geodata\\census\\Tract\\tract2010.shp',
        'blockgp': 'W:\\geodata\\census\\Blockgroup\\blockgrp2010.shp',
        'block': 'W:\\geodata\\census\\Block\\block2010.shp'
        }

shpName = {
        'juris': 'psrc_region',
        'zipcode': 'zipcode',
        'taz': 'taz2010_to_tad2010',
        'faz': 'FAZ_2010',
        'tract': 'tract2010',
        'blockgp': 'blockgrp2010',
        'block': 'block2010'
        }

# Dictionary functions    
def shpCountyField(x):
    return{
        'juris': "CNTYNAME",
        'zipcode': "COUNTY",
        'taz': "COUNTY",
        'faz': "County",
        'tract': "COUNTYFP10",
        'blockgp': "COUNTYFP10",
        'block': "COUNTYFP10"
    }[x]
    
def shpCountyValue(x):
    return{
        'juris': ['King', 'Kitsap', 'Pierce', 'Snohomish'],
        'zipcode': ['033', '035', '053', '061'],
        'taz': ['033', '035', '053', '061'],
        'faz': ['King', 'Kitsap', 'Pierce', 'Snohomish'],
        'tract': ['033', '035', '053', '061'],
        'blockgp': ['033', '035', '053', '061'],
        'block': ['033', '035', '053', '061']
    }[x]    
 
# Environment inputs       
rootDir = 'J:\\Projects\\UrbanSim\\NEW_DIRECTORY\\GIS\\Shapefiles\\Parcels'
homeDir = '2015'
fgdbDir = 'spatial_overlay'
fgdbName = 'layers.gdb'

counties = ['King', 'Kitsap', 'Pierce', 'Snohomish']

# Create new file gdb
for c in range(len(counties)):
    fgdbPath = os.path.join(rootDir, counties[c], homeDir, fgdbDir)
    arcpy.CreateFileGDB_management(fgdbPath, fgdbName)
    print "Created" + counties[c] + " file gdb"

# loop through each overlay feature that can be subsetted, subset by county, export to file gdb
overlayShp = shpDict.keys()

for f in overlayShp:
    inFeature = shpDict[f]
    nameFeature  =  shpName[f]                  
    countyValues = shpCountyValue(f) 
    countyField = shpCountyField(f) 
    for c in range(len(countyValues)): 
        countyValues[c] = str(countyValues[c])
        countyField = str(countyField)          
        outFeature = os.path.join(rootDir, counties[c], homeDir, fgdbDir, fgdbName, nameFeature)
        whereClause = countyField + "= '" + countyValues[c] + "'"
        arcpy.Select_analysis(inFeature, outFeature,  whereClause) 
        print "Exported " + counties[c] + " " + f                                                         
                               
                                