appraisal_account_cols = ['parcel_number',
        'appraisal_account_type',
        'business_name',
        'value_area_id',
        'land_economic_area',
        'buildings',
        'group_acct_number',
        'land_gross_acres',
        'land_net_acres',
        'land_gross_square_feet',
        'land_net_square_feet',
        'land_gross_front_feet',
        'land_width',
        'land_depth',
        'submerged_area_square_feet',
        'appraisal_date',
        'waterfront_type',
        'view_quality',
        'utility_electric',
        'utility_sewer',
        'utility_water',
        'street_type',
        'latitude',
        'longitude']

improvement_cols = ['parcel_number', 
       'building_id', 
       'property_type', 
       'neighborhood', 
       'neighborhood_extension', 
       'square_feet', 
       'net_square_feet', 
       'percent_complete', 
       'condition', 
       'quality', 
       'primary_occupancy_code', 
       'primary_occupancy_description', 
       'mobile_home_serial_number', 
       'mobile_home_total_length', 
       'mobile_home_make', 
       'attic_finished_square_feet', 
       'basement_square_feet', 
       'basement_finished_square_feet', 
       'carport_square_feet', 
       'balcony_square_feet', 
       'porch_square_feet', 
       'attached_garage_square_feet', 
       'detatched_garage_square_feet', 
       'fireplaces', 
       'basement_garage_door']

improvement_builtas_cols = ['parcel_number', 
        'building_id', 
        'built_as_number', 
        'built_as_id', 
        'built_as_description', 
        'built_as_square_feet', 
        'hvac', 
        'hvac_description', 
        'exterior', 
        'interior', 
        'stories', 
        'story_height', 
        'sprinkler_square_feet', 
        'roof_cover', 
        'bedrooms', 
        'bathrooms', 
        'units', 
        'class_code', 
        'class_description', 
        'year_built', 
        'year_remodeled', 
        'adjusted_year_built', 
        'physical_age', 
        'built_as_length', 
        'built_as_width', 
        'mobile_home_model']

land_attribute_cols = ['parcel_number', 
        'attribute', 
        'attribute_description']

improvement_detail_cols = ['parcel_number', 
        'building_id', 
        'detail_type', 
        'detail_description', 
        'units']