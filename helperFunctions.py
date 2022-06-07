
# Assigns a classification according to house prices
def get_class(to_check):
    input_v = int(to_check)
    if input_v <= 50000:
        return 0
    if 50000 < input_v <= 100000:
        return 1
    if 100000 < input_v <= 150000:
        return 2
    if 150000 < input_v <= 200000:
        return 3
    if 200000 < input_v <= 250000:
        return 4
    if input_v > 250000:
        return 5

# Identifies the general zoning classification of the sale
def convertMSZoningData(toConvert): # Converts text to a float value
  total = 5
  if toConvert == 'C (all)': # Commercial
      return 1/total
  elif toConvert == 'FV': # Floating Village Residential
      return 2/total
  elif toConvert == 'RH':# Residential High Density
      return 5/total
  elif toConvert == 'RL':# Residential Low Density
      return 3/total
  elif toConvert == 'RM': # Residential Medium Density
      return 4/total
  else :# found an outlier, just give this a bad number.
    print("error converting in convertMSZoningData",toConvert)
    return -1

# Type of road access to property
def convertStreetData(toConvert):
    total = 2
    if toConvert == 'Grvl': # Gravel
        return 1/total
    else:                   # Paved
        return 2/total

# Type of utilities available
def convertUtilitiesData(toConvert):
    total = 2
    if toConvert == 'AllPub': # All public Utilities (E,G,W,& S)
        return 2/total
    else:                     #Electricity and Gas Only
        return 1/total

# Physical locations within Ames city limits
def convertNeighborhoodData(toConvert): # by most popular
    total = 25
    if toConvert == 'Blmngtn': # Bloomington Heights
        return 21/total
    elif toConvert == 'Blueste': # Bluestem #124K - $150K
        return 12/total
    elif toConvert == 'BrDale': # Briardale $180K
        return 11/total
    elif toConvert == 'BrkSide': # Brookside $180K
        return 10/total
    elif toConvert == 'ClearCr': # Clear Creek $350K
        return 9/total
    elif toConvert == 'CollgCr': # College Creek
        return 23/total
    elif toConvert == 'Crawfor': # Crawford $110K
        return 2/total
    elif toConvert == 'Edwards': # Edwards $235K
        return total/total
    elif toConvert == 'Gilbert': # Gilbert $279K
        return 13/total
    elif toConvert == 'IDOTRR': # Iowa DOT and Rail Road
        return 1/total
    elif toConvert == 'MeadowV': # Meadow Village $166K
        return 8/total
    elif toConvert == 'Mitchel': # Mitchell 
        return 24/total
    elif toConvert == 'NAmes': # North Ames $221K
        return 7/total
    elif toConvert == 'NoRidge': # Northridge $419K
        return 6/total
    elif toConvert == 'NPkVill': # Northpark Villa $858K
        return 5/total
    elif toConvert == 'NridgHt': # Northridge Heights $130K
        return 14/total
    elif toConvert == 'NWAmes': # Northwest Ames $278K
        return 4/total
    elif toConvert == 'OldTown': # Old Town  $315K
        return 19/total
    elif toConvert == 'SWISU': # South & West of Iowa State University
        return 19/total
    elif toConvert == 'Sawyer': # Sawyer $262K
        return 13/total
    elif toConvert == 'SawyerW': # Sawyer West $173K
        return 22/total
    elif toConvert == 'Somerst': # Somerset
        return 18/total
    elif toConvert == 'StoneBr': # Stone Brook $140K
        return 3/total
    elif toConvert == 'Timber': # Timberland $430K
        return 16/total
    elif toConvert == 'Veenker': # Veenker $279K
        return 10/total
    else:
        print("error converting in neighborhood: ",toConvert)
        return -1

# Rates the overall condition of the house
def convertOverAllConditionData(toConvert): # to keep the numbers small
    total = 9
    return int(toConvert)/total
    
# Rates the overall material and finish of the house
def convertOverAllQualityData(toConvert): # to keep the numbers small
    total = 10
    return int(toConvert)/total

# Identifies the type of dwelling involved in the sale
def convertMSSubClassData(toConvert):
    total = 16
    if toConvert == '20':  # 1-STORY 1946 & NEWER ALL STYLES
        return 11/total
    elif toConvert == '30': # 1-STORY 1945 & OLDER
        return 7/total
    elif toConvert == '40': # 1-STORY W/FINISHED ATTIC ALL AGES     
        return 6/total
    elif toConvert == '45': # 1-1/2 STORY - UNFINISHED ALL AGES
        return 5/total
    elif toConvert == '50': # 1-1/2 STORY FINISHED ALL AGES
        return 4/total
    elif toConvert == '60': # 2-STORY 1946 & NEWER
        return 14/total
    elif toConvert == '70': # 2-STORY 1945 & OLDER
        return 3/total
    elif toConvert == '75': # 2-1/2 STORY ALL AGES
        return 12/total
    elif toConvert == '80': # SPLIT OR MULTI-LEVEL
        return 10/total
    elif toConvert == '85': # SPLIT FOYER
        return 2/total
    elif toConvert == '90': # DUPLEX - ALL STYLES AND AGES
        return 15/total
    elif toConvert == '120': # 1-STORY PUD (Planned Unit Development) - 1946 & NEWER
        return 9/total
    elif toConvert == '150': # 1-1/2 STORY PUD - ALL AGES
        return 1/total
    elif toConvert == '160': # 2-STORY PUD - 1946 & NEWER
        return 13/total
    elif toConvert == '180': # PUD - MULTILEVEL - INCL SPLIT LEV/FOYER
        return 8/total
    elif toConvert == '190': # 2 FAMILY CONVERSION - ALL STYLES AND AGES
        return 16/total
    else:
        print("error converting in MSSubClass: ",toConvert)
        return -1
# Type of dwelling
def convertBldgTypeData(toConvert):
    total = 5
    if toConvert == '1Fam': #	Single-family Detached	
        return 3/total
    elif toConvert == '2fmCon': # Two-family Conversion; originally built as one-family dwelling
        return 4/total
    elif toConvert == 'Duplex': # Duplex
        return 5/total
    elif toConvert == 'TwnhsE':	# Townhouse End Unit
        return 2/total
    elif toConvert == 'Twnhs': # Townhouse Inside Unit
        return 1/total
    else:
        print('error converting in BldgTypeData',toConvert)
        return -1

# Original construction date
def convertYearBuildData(toConvert):
    total = 8
    built = int(toConvert)
    if built < 1960:
        return 1/total
    elif 1960 < built < 1970:
        return 2/total
    elif 1970 < built < 1980:
        return 3/total
    elif 1980 < built < 1990:
        return 4/total
    elif 1990 < built < 2000:
        return 5/total
    elif 2000 < built < 2010:
        return 6/total
    elif 2010 < built < 2020:
        return 7/total
    else: # newest home
        return  8/total

# Type of heating
def convertTypeOfHeatData(toConvert):
    total = 6

    if toConvert == 'Floor': # Floor Furnace
        return 1/total
    elif toConvert == 'GasA': # Gas forced warm air furnace
        return 2/total
    elif toConvert == 'GasW': # Gas hot water or steam heat
        return 3/total
    elif toConvert == 'Grav': #	Gravity furnace	
        return 4/total
    elif toConvert == 'OthW': #	Hot water or steam heat other than gas
        return 5/total
    elif toConvert == 'Wall': #	Wall furnace
        return 6/total
    else:
        print('error converting in TypeOfHeat: ',toConvert)
        return -1