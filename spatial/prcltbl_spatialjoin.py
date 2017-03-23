# This script will perform spatial joins between county parcel centroids and political/environmental polygon features

# Import system modules
import arcpy, os, time

start = time.time()

# Dictionary containing joining features
def shpDict(x):
    return {
        'uga': 'W:\\geodata\\political\\PSRC_region.gdb\uga',
        'juris': 'W:\\geodata\\political\\PSRC_region.gdb\psrc_region',
        'zipcode': 'W:\\geodata\\political\\zipcode.shp',
        'schooldist': 'J:\\Projects\\UrbanSim\\NEW_DIRECTORY\\GIS\\Shapefiles\\Political\\school_districts_WA.shp',
        'urbcen': 'W:\\geodata\\political\\urbcen.shp',
        'micen': 'W:\\geodata\\political\\micen.shp',
        'taz': 'W:\\geodata\\forecast\\taz2010_to_tad2010.shp',
        'faz': 'W:\\geodata\\forecast\\FAZ_2010.shp',
        'tract': 'W:\\geodata\\census\\Tract\\tract2010.shp',
        'blockgp': 'W:\\geodata\\census\\Blockgroup\\blockgrp2010.shp',
        'block': 'W:\\geodata\\census\\Block\\block2010.shp'
    }[x]

def oldFieldsDict(x):
    return {
        'uga': ['Join_Count'],
        'juris': [],
        'zipcode': ['ZCTA5CE10'],
        'schooldist': ['NAME'],
        'urbcen': ['NAME'],
        'micen': [],
        'taz': [],
        'faz': [],
        'tract': ['GEOID10'],
        'blockgp': ['GEOID10'],
        'block': ['GEOID10']
    }[x]
 
def newFieldsDict(x):
    return {
        'uga': ['IN_UGA'],
        'juris': [],
        'zipcode': ['ZIP'],
        'schooldist': ['DISTNAME'],
        'urbcen': ['URBCEN'],
        'micen': [],
        'taz': [],
        'faz': [],
        'tract': ['TRACT10'],
        'blockgp': ['BLOCKGRP10'],
        'block': ['BLOCK10']
    }[x]   

def delFieldsDict(x):
    return {
        'uga': ["TARGET_FID", "Shape_Leng", "Shape_Area"],
        'juris': ["TARGET_FID", "Join_Count", "CITYNAME", "CITYFIPS", "CNTYFIPS", "ANNXNAME", "BRBNO", "ORDNO", "EFF_DATE", "ACRES", "APPR_DATE", "wtrshed", "FEAT_TYPE", "RGEO_CLASS", "CLASS_DESC", "Shape_STArea__", "Shape_STLength__", "Shape_Length", "Shape_Area", "acres_gis"], 
        'zipcode': ["TARGET_FID", "Join_Count", "STATEFP10", "GEOID10"],
        'schooldist': ["TARGET_FID", "Join_Count", "STATEFP", "UNSDLEA", "GEOID", "LSAD", "LOGRADE", "HIGRADE", "MTFCC", "SDTYP", "FUNCSTAT", "ALAND", "AWATER", "INTPTLAT", "INTPTLON", "Shape_Leng", "Shape_Area"], 
        'urbcen': ["TARGET_FID", "Join_Count", "ID", "AREA_FEET", "PERIMETER_", "PARKING", "POPDEN1996", "PLANPOP96", "JOBS1994", "PLANJOBS94", "HOUSEUNITS", "HUPLAN", "FLOORSPC", "ACRES", "HECTARES", "AREA", "PERIMETER", "ADOPTDATE"],
        'micen': ["TARGET_FID", "Join_Count", "COUNT_", "COUNTY", "POP00", "EMP00", "Shape_Leng", "Acres"],
        'taz': ["Join_Count", "Join_Count_1", "TARGET_FID", "TARGET_FID_1", "Shape_Leng", "Shape_Area"],
        'faz': ["TARGET_FID", "Join_Count", "nFAZ10", "County"],
        'tract': ["TARGET_FID", "Join_Count", "STATEFP10", "COUNTYFP10", "TRACTCE10", "NAME10", "NAMELSAD10", "MTFCC10", "FUNCSTAT10", "ALAND10", "AWATER10", "INTPTLAT10", "INTPTLON10", "NAME_VAL"],
        'blockgp': ["TARGET_FID", "Join_Count", "STATEFP10", "COUNTYFP10", "TRACTCE10", "BLKGRPCE10", "NAMELSAD10", "MTFCC10", "FUNCSTAT10", "ALAND10", "AWATER10", "INTPTLAT10", "INTPTLON10", "Population"],
        'block': ["OBJECTID_1", "OBJECTID_12", "TARGET_FID", "Join_Count", "STATEFP10", "COUNTYFP10", "TRACTCE10", "BLOCKCE10", "NAME10", "MTFCC10", "UR10", "UACE10", "FUNCSTAT10", "ALAND10", "AWATER10", "INTPTLAT10", "INTPTLON10", "Block_Pop", "TAZ_POP", "TAZ_ID", "totArea", "PLACE", "JURIS_1", "JURISTYPE", "Centr_X", "Cntr_Y", "acres"]
    }[x] 
    
# Environment inputs  
counties = ['Kitsap', 'Pierce', 'Snohomish', 'King']
shp0 = ['kitptfnl15testCopy.shp','pieptfnl15testCopy.shp', 'snoptfnl15testCopy.shp', 'kinptfnl15testCopy.shp']
joinFeaturesList = ['uga', 'juris', 'zipcode', 'schooldist', 'urbcen', 'micen', 'taz', 'faz', 'tract', 'blockgp', 'block']
target = ["overlay"+str(i) for i in range(1, len(joinFeaturesList)+1)]

rootDir = 'J:\\Projects\\UrbanSim\\NEW_DIRECTORY\\GIS\\Shapefiles\\Parcels'
homeDir = '2015_test'
shp0Dir = 'parcels_table'
outshpDir = 'spatial_overlay'

# Iterate for number of counties
for c in range(len(counties)):    
    # Set environment workspaces
    workspace = os.path.join(rootDir, counties[c], homeDir, shp0Dir)
    outWorkspace = os.path.join(rootDir, counties[c], homeDir, outshpDir, "spatial_overlay.gdb")
    arcpy.env.workspace = outWorkspace
    
    nums = range(0, len(joinFeaturesList))
    
    # Iterate for number of join features
    for n in nums:
        if n == 0:
            targetFeatures = os.path.join(workspace, shp0[c])
        else:
            targetFeatures = os.path.join(outWorkspace, target[n-1])
        outfc = os.path.join(outWorkspace, target[n])
        joinFeatures = shpDict(joinFeaturesList[n]) 
        
        # Spatial Join
        arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc, join_operation = "JOIN_ONE_TO_ONE", join_type = "KEEP_ALL")  
        
        # Rename fields
        oldFields = oldFieldsDict(joinFeaturesList[n])
        newFields = newFieldsDict(joinFeaturesList[n])
        
        for i in range(len(oldFields)):
            arcpy.AlterField_management(outfc, oldFields[i], newFields[i])
        
        # Delete fields
        arcpy.DeleteField_management(outfc, delFieldsDict(joinFeaturesList[n]))
        print "Spatial joined " + counties[c] + " " + joinFeaturesList[n]

end = time.time()
print(str((end-start)/60) + " minutes")
        













