# This script will perform spatial joins between county parcel centroids and political/environmental polygon features

# Import system modules
import arcpy, os, time

start = time.time()

# Dictionary containing joining features
def shpDictWhole(x):
    return {
        'uga': 'W:\\geodata\\political\\PSRC_region.gdb\uga',
        'schooldist': 'J:\\Staff\\Christy\\baseyear\\shapes\\overlay_shapes.gdb\school_districts',
        'urbcen': 'W:\\geodata\\political\\urbcen.shp',
        'micen': 'W:\\geodata\\political\\micen.shp',
    }[x]
    
def shpDict(x):
    return {
        'juris': 'psrc_region',
        'zipcode': 'zipcode',
        'taz': 'taz2010_to_tad2010',
        'faz': 'FAZ_2010',
        'tract': 'tract2010',
        'blockgp': 'blockgrp2010',
        'block': 'block2010'
    }[x]

def oldFieldsDict(x):
    return {
        'uga': ['Join_Count'],
        'juris': [],
        'zipcode': [], 
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
        'zipcode': [],
        'schooldist': ['DISTNAME'],
        'urbcen': ['URBCEN'],
        'micen': [],
        'taz': [],
        'faz': [],
        'tract': ['TRACT10'],
        'blockgp': ['BLOCKGRP10'],
        'block': ['BLOCK10']
    }[x]   

def keepFieldsDict(x):
    return{
        'uga': ['IN_UGA'],
        'juris': ['CNTYNAME', 'JURIS'],
        'zipcode': ['ZIP'],
        'schooldist': ['DISTNAME', 'DistrictID'],
        'urbcen': ['URBCEN'],
        'micen': ['MIC'],
        'taz': ['TAZ', 'TAD'],
        'faz': ['FAZ10', 'LARGE_AREA'],
        'tract': ['TRACT10'],
        'blockgp': ['BLOCKGRP10'],
        'block': ['BLOCK10']
    }[x]
    
# Environment inputs  
counties = ['Kitsap', 'Pierce', 'Snohomish']#, 'King'
shp0 = ['kitptfnl15testCopy.shp','pieptfnl15testCopy.shp', 'snoptfnl15testCopy.shp']#, 'kinptfnl15testCopy.shp'
subsettedFc = ['juris', 'zipcode',  'taz', 'faz', 'tract', 'blockgp', 'block']
wholeFc = ['uga', 'schooldist', 'urbcen', 'micen']
joinFeaturesList = subsettedFc + wholeFc

target = ["overlay"+str(i) for i in range(1, len(joinFeaturesList)+1)]

rootDir = 'J:\\Projects\\UrbanSim\\NEW_DIRECTORY\\GIS\\Shapefiles\\Parcels'
homeDir = '2015'
shp0Dir = 'parcels_table'
outshpDir = 'spatial_overlay'
joinFeaturesGdb = 'layers.gdb'

# Iterate for number of counties
for c in range(len(counties)):    
    # Set environment workspaces
    workspace = os.path.join(rootDir, counties[c], homeDir, shp0Dir)
    outWorkspace = os.path.join(rootDir, counties[c], homeDir, outshpDir, "spatial_overlay.gdb")
    arcpy.env.workspace = outWorkspace
    
    nums = range(0, len(joinFeaturesList))
    
    keepFieldsList = []
    requiredFieldsList = ["OBJECTID", "Shape"]
    
    # Iterate for number of join features
    for n in nums:
        if n == 0:
            targetFeatures = os.path.join(workspace, shp0[c])
        else:
            targetFeatures = os.path.join(outWorkspace, target[n-1])       
        # List current target feature fields
        keepFieldsList = [f.name for f in arcpy.ListFields(targetFeatures)]
        outfc = os.path.join(outWorkspace, target[n])
        if joinFeaturesList[n] in subsettedFc:
            joinFeatures = os.path.join(rootDir, counties[c], homeDir, outshpDir, joinFeaturesGdb, shpDict(joinFeaturesList[n])) 
        else:
            joinFeatures = shpDictWhole(joinFeaturesList[n])
        # Spatial join; exclude 'closest' match option for 'uga', 'urbcen' and 'micen' features
        if joinFeaturesList[n] in subsettedFc + ['schooldist']:
            arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc, join_operation = "JOIN_ONE_TO_ONE", join_type = "KEEP_ALL", match_option = "CLOSEST")
        else:
            arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outfc, join_operation = "JOIN_ONE_TO_ONE", join_type = "KEEP_ALL")        
        # Rename fields
        oldFields = oldFieldsDict(joinFeaturesList[n])
        newFields = newFieldsDict(joinFeaturesList[n])       
        for i in range(len(oldFields)):
            arcpy.AlterField_management(outfc, oldFields[i], newFields[i])        
        # Extend list of 'keep' fields
        if n == 0:
            keepFieldsList.extend(requiredFieldsList)
        keepFieldsList.extend(keepFieldsDict(joinFeaturesList[n]))
        # Re-list target features fields
        fields = arcpy.ListFields(outfc)
        dropFields = [f.name for f in fields if f.name not in keepFieldsList]                
        # Delete fields
        arcpy.DeleteField_management(outfc, dropFields)       
        print "Spatial joined " + counties[c] + " " + joinFeaturesList[n]

end = time.time()
print(str(((end-start)/60)/60) + " hours")
