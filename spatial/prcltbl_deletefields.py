# This script will delete selected shapefile fields (containing words: 'OBJECT*', 'Shape_*', and '*area*'). Run before spatial joins script.

# Import system modules
import arcpy, os, time

start = time.time()

# Environment inputs  
counties = ['Kitsap', 'Pierce', 'Snohomish', 'King']
shp0 = ['kitptfnl15testCopy.shp','pieptfnl15testCopy.shp', 'snoptfnl15testCopy.shp', 'kinptfnl15testCopy.shp']

rootDir = 'J:\\Projects\\UrbanSim\\NEW_DIRECTORY\\GIS\\Shapefiles\\Parcels'
homeDir = '2015_test'
shp0Dir = 'parcels_table'

# Iterate for number of counties
for c in range(len(counties)): 
    
    # Set environment workspace
    workspace = os.path.join(rootDir, counties[c], homeDir, shp0Dir)
    arcpy.env.workspace = workspace
    
    fc = os.path.join(rootDir, counties[c], homeDir, shp0Dir, shp0[c])
    
    # Populate list with selected field names
    removeFields = [f.name for f in arcpy.ListFields(fc, "OBJECT*") + arcpy.ListFields(fc, "Shape_*") + arcpy.ListFields(fc, "*area*")]    
    
    # Delete fields
    arcpy.DeleteField_management(fc, removeFields)
    
    print("Deleted " + counties[c] + " fields")

end = time.time()
print(str((end-start)/60) + " minutes")