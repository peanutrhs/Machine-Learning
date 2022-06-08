from email.mime import base
from multiprocessing import pool
import string
import csv
import stringprep

from numpy import mat

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

# Linear feet of street connected to property
def convertLotFrontageData(toConvert,max):
    if toConvert == 'NA': 
        return 0
    else:
        return int(toConvert)/max

# Max lot size in square feet
def getLotAreaMax(matrix): # bring in entire set
    max = 0
    lotArea = 4
    for row in range(0,len(matrix)):
        if int(matrix[row][lotArea]) > max:
            max = int(matrix[row][lotArea])
    return max
            
    

# Lot size in square feet
def convertLotAreaData(toConvert,max):
    return int(toConvert)/max



# Type of road access to property
def convertStreetData(toConvert):
    total = 2
    if toConvert == 'Grvl': # Gravel
        return 1/total
    else:                   # Paved
        return 2/total

# Type of alley access to property
def convertAlleyData(toConvert):
    if toConvert == 'NA':
        return 0
    elif toConvert == 'Grvl':
        return 1/2
    else:
        return 1

# General shape of property
def convertLotShapeData(toConvert):
    if toConvert == 'Reg': # Regular
        return 1	
    elif toConvert == 'IR1': # Slightly irregular
        return 3/4
    elif toConvert == 'IR2': # Moderately Irregular
        return 2/4
    else:
        return 1/4

# Flatness of the property
def convertLandContourData(toConvert):
    if toConvert == 'Lvl': #	Near Flat/Level
        return 1	
    elif toConvert == 'Bnk': # Banked - Quick and significant rise from street grade to building
        return 3/4
    elif toConvert == 'HLS': # Hillside - Significant slope from side to side
        return 2/4
    else:
        return 1/4

# Type of utilities available
def convertUtilitiesData(toConvert):
    total = 2
    if toConvert == 'AllPub': # All public Utilities (E,G,W,& S)
        return 2/total
    else:                     #Electricity and Gas Only
        return 1/total

# Lot configuration
def convertLotConfigData(toConvert):
    if toConvert == 'Inside': #	Inside lot
        return 1
    elif toConvert == 'Corner': #	Corner lot
        return 4/5
    elif toConvert == 'CulDSac': # Cul-de-sac
        return 3/5
    elif toConvert == 'FR2': # Frontage on 2 sides of property
        return 2/5
    else:
        return 1/5

# Slope of property
def convvertSlopeData(toConvert):
    if toConvert == 'Gtl': # Gentle slope
        return 1
    if toConvert == 'Mod': # Moderate Slope
        return 2/3	
    else:
        return 1/3

# Physical locations within Ames city limits
def convertNeighborhoodData(toConvert): # by most popular
    total = 25
    if toConvert == 'Blmngtn': # Bloomington Heights
        return 1
    elif toConvert == 'Blueste': # Bluestem #124K - $150K
        return 24/total
    elif toConvert == 'BrDale': # Briardale $180K
        return 23/total
    elif toConvert == 'BrkSide': # Brookside $180K
        return 22/total
    elif toConvert == 'ClearCr': # Clear Creek $350K
        return 21/total
    elif toConvert == 'CollgCr': # College Creek
        return 20/total
    elif toConvert == 'Crawfor': # Crawford $110K
        return 19/total
    elif toConvert == 'Edwards': # Edwards $235K
        return 18/total
    elif toConvert == 'Gilbert': # Gilbert $279K
        return 17/total
    elif toConvert == 'IDOTRR': # Iowa DOT and Rail Road
        return 16/total
    elif toConvert == 'MeadowV': # Meadow Village $166K
        return 5/total
    elif toConvert == 'Mitchel': # Mitchell 
        return 14/total
    elif toConvert == 'NAmes': # North Ames $221K
        return 13/total
    elif toConvert == 'NoRidge': # Northridge $419K
        return 12/total
    elif toConvert == 'NPkVill': # Northpark Villa $858K
        return 11/total
    elif toConvert == 'NridgHt': # Northridge Heights $130K
        return 10/total
    elif toConvert == 'NWAmes': # Northwest Ames $278K
        return 9/total
    elif toConvert == 'OldTown': # Old Town  $315K
        return 8/total
    elif toConvert == 'SWISU': # South & West of Iowa State University
        return 7/total
    elif toConvert == 'Sawyer': # Sawyer $262K
        return 6/total
    elif toConvert == 'SawyerW': # Sawyer West $173K
        return 5/total
    elif toConvert == 'Somerst': # Somerset
        return 4/total
    elif toConvert == 'StoneBr': # Stone Brook $140K
        return 3/total
    elif toConvert == 'Timber': # Timberland $430K
        return 2/total
    else:
        return 1/total
    
# Proximity to various conditions
def convertCondData(toConvert):# use for all Condition data
    if toConvert == 'Artery': #	Adjacent to arterial street
        return 1
    elif toConvert == 'Feedr': # Adjacent to feeder street
        return 8/9	
    elif toConvert == 'Norm': #	Normal
        return 7/9	
    elif toConvert == 'RRNn': #	Within 200' of North-South Railroad
        return 6/9
    elif toConvert == 'RRAn': #	Adjacent to North-South Railroad
        return 5/9
    elif toConvert == 'PosN': # Near positive off-site feature--park, greenbelt, etc.
        return 4/9
    elif toConvert == 'PosA': #	Adjacent to postive off-site feature
        return 3/9
    elif toConvert == 'RRNe': #	Within 200' of East-West Railroad
        return 2/9
    else:
        return 1/9

# Style of dwelling
def convertStyleDwellingData(toConvert):
    if toConvert == '1Story': #	One story
        return 1
    elif toConvert == '1.5Fin': # One and one-half story: 2nd level finished
        return 7/8
    elif toConvert == '1.5Unf': # One and one-half story: 2nd level unfinished
        return 6/8
    elif toConvert == '2Story': # Two story
        return 5/8
    elif toConvert == '2.5Fin': # Two and one-half story: 2nd level finished
        return 4/8
    elif toConvert == '2.5Unf': # Two and one-half story: 2nd level unfinished
        return 3/8
    elif toConvert == 'SFoyer': # Split Foyer
        return 2/8
    else:
        return 1/8

# Rates the overall material and finish of the house
def convertOverAllQualityData(toConvert): # to keep the numbers small
    total = 10
    return int(toConvert)/total

# Rates the overall condition of the house
def convertOverAllConditionData(toConvert): # to keep the numbers small
    total = 9
    return int(toConvert)/total
    
# Original construction date
def convertYearBuildData(toConvert):
    total = 8
    if toConvert == 'NA':
        return 0
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

# Remodel date (same as construction date if no remodeling or additions)
def convertYearRemodelData(toConvert):
    total = 8
    if toConvert == 'NA':
        return 0
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

# Type of roof
def convertRoofStyleData(toConvert):
    if toConvert == 'Flat': # Flat
        return 1
    elif toConvert == 'Gable': # Gable
        return 5/6
    elif toConvert == 'Gambrel': # Gabrel (Barn)
        return 4/6
    elif toConvert == 'Hip': # Hip
        return 3/6
    elif toConvert == 'Mansard': # Mansard
        return 2/6
    else:
        return 1/6

# Roof material
def convertRoofMaterialData(toConvert):
    if toConvert == 'ClyTile': # Clay or Tile
        return 1
    elif toConvert == 'CompShg': #	Standard (Composite) Shingle
        return 7/8
    elif toConvert == 'Membran': #	Membrane
        return 6/8
    elif toConvert == 'Metal': # Metal
        return 5/8
    elif toConvert == 'Roll': #	Roll
        return 4/8
    elif toConvert == 'Tar&Grv': #	Gravel & Tar
        return 3/8
    elif toConvert == 'WdShake': #	Wood Shakes
        return 2/8
    else:
        return 1/8

# Exterior covering on house
def convertExeriorCoveringData(toConvert):
    if toConvert == 'AsbShng': # Asbestos Shingles
        return 1
    elif toConvert == 'AsphShn': #	Asphalt Shingles
        return 16/17
    elif toConvert == 'BrkComm': #	Brick Common
        return 15/17
    elif toConvert == 'BrkFace': #	Brick Face
        return 14/17
    elif toConvert == 'CBlock': # Cinder Block
        return 13/17
    elif toConvert == 'CemntBd': #	Cement Board
        return 12/17
    elif toConvert == 'HdBoard': #	Hard Board
        return 11/17
    elif toConvert == 'ImStucc': # Imitation Stucco
        return 10/17
    elif toConvert == 'MetalSd': #	Metal Siding
        return 9/17
    elif toConvert == 'Other': # Other
        return 8/17
    elif toConvert == 'Plywood': #	Plywood
        return 7/17
    elif toConvert == 'PreCast': #	PreCast
        return 6/17	
    elif toConvert == 'Stone': # Stone
        return 5/17
    elif toConvert == 'Stucco': # Stucco
        return 4/17
    elif toConvert == 'VinylSd': # Vinyl Siding
        return 3/17
    elif toConvert == 'Wd Sdng': #	Wood Siding
        return 2/17
    else: 
        return 1/17

# Masonry veneer type
def convertMasonryVeneerTypeData(toConvert):
    if toConvert == 'BrkCmn': #	Brick Common
        return 1
    elif toConvert == 'BrkFace': # Brick Face
        return 4/5
    elif toConvert == 'CBlock': # Cinder Block
        return 3/4
    elif toConvert == 'None': #	None
        return 2/4
    else:
        return 1/4

# Get max masonry veneer in square feet
def getMasonryVeneerMax(matrix):
    max = 0
    MasonryVeneer = 26
    for row in range(0,len(matrix)):
        if matrix[row][MasonryVeneer] == 'NA':
            matrix[row][MasonryVeneer] = 0
        if int(matrix[row][MasonryVeneer]) > max:
            max = int(matrix[row][MasonryVeneer])
    return max

# Masonry veneer area in square feet
def convertMasonryVeneerAreaData(toConvert,max):
    return int(toConvert)/max

# Evaluates the quality of the material on the exterior 
def convertExternalQualData(toConvert):
    total = 5
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 4/total
    elif toConvert == 'TA': # Average/Typical
        return 3/total
    elif toConvert == 'Fa': # Fair
        return 2/total
    elif toConvert == 'Po': # Poor
        return 1/total
    else:
        print('error converting in ExternalQualData: ',toConvert)

# Evaluates the present condition of the material on the exterior
def convertExteriorCondData(toConvert):
    total = 5
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 4/total
    elif toConvert == 'TA': # Average/Typical
        return 3/total
    elif toConvert == 'Fa': # Fair
        return 2/total
    elif toConvert == 'Po': # Poor
        return 1/total
    else:
        print('error converting in ExternalMaterialData: ',toConvert)
    
# Type of foundation
def converrtTypeFoundationData(toConvert):
    if toConvert == 'BrkTil': #	Brick & Tile
        return 1
    elif toConvert == 'CBlock': # Cinder Block
        return 5/6
    elif toConvert == 'PConc': # Poured Contrete
        return 4/6	
    elif toConvert == 'Slab': #	Slab
        return 3/6
    elif toConvert == 'Stone': # Stone
        return 2/6
    else:
        return 1/6

# Evaluates the height of the basement
def convertBasementQualData(toConvert):
    if toConvert == 'Ex': #	Excellent (100+ inches)
        return 1	
    elif toConvert == 'Gd': # Good (90-99 inches)
        return 5/6
    elif toConvert == 'TA': # Typical (80-89 inches)
        return 4/6
    elif toConvert == 'Fa': # Fair (70-79 inches)
        return 3/6
    elif toConvert == 'Po': # Poor (<70 inches)
        return 2/6
    else:
        return 1/6

# Evaluates the general condition of the basement
def convertBasementCondData(toConvert):
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 5/6
    elif toConvert == 'TA': # Typical - slight dampness allowed
        return 4/6
    elif toConvert == 'Fa': # Fair - dampness or some cracking or settling
        return 3/6
    elif toConvert == 'Po': # Poor - Severe cracking, settling, or wetness
        return 2/6
    else:
        return 1/6

# generic condition
def convertCondData(toConvert):
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 5/6
    elif toConvert == 'TA': # Typical - slight dampness allowed
        return 4/6
    elif toConvert == 'Fa': # Fair - dampness or some cracking or settling
        return 3/6
    elif toConvert == 'Po': # Poor - Severe cracking, settling, or wetness
        return 2/6
    else:
        return 1/6    

# Refers to walkout or garden level walls
def convertBasementExposureData(toConvert):
    if toConvert == 'Gd': #	Good Exposure
        return 1
    elif toConvert == 'Av': # Average Exposure (split levels or foyers typically score average or above)
        return 4/5	
    elif toConvert == 'Mn': # Mimimum Exposure
        return 3/5
    elif toConvert == 'No': # No Exposure
        return 2/5
    else:
        return 1/5
    
# Rating of basement finished area
def convertBasementFinishTypeData(toConvert): # to be used for indx 33 & 35
    if toConvert == 'GLQ': # Good Living Quarters
        return 1
    elif toConvert == 'ALQ': # Average Living Quarters
        return 6/7
    elif toConvert == 'BLQ': # Below Average Living Quarters
        return 5/7	
    elif toConvert == 'Rec': # Average Rec Room
        return 4/7
    elif toConvert == 'LwQ': #	Low Quality
        return 3/7
    elif toConvert == 'Unf': # Unfinshed
        return 2/7
    else:
        return 1/7

# Return max Sqft finished Basement
def getMaxSqFtFinishedBasement(matrix):
    max = 0
    SqFtFinishedBasement = 34
    for row in range(0,len(matrix)):
        if int(matrix[row][SqFtFinishedBasement]) > max:
            max = int(matrix[row][SqFtFinishedBasement])
    return max

# Type 1 finished square feet
def convertSqFtFinishedBasementData(toConvert,max): # to be used for ind 34 & 36
    return int(toConvert)/max

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

# Heating quality and condition
def convertHeatingQualAndCondData(toConvert):
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 4/5
    elif toConvert == 'TA': # Average/Typical
        return 3/5
    elif toConvert == 'Fa': # Fair
        return 2/5
    else:
        return 1/5

# Central air conditioning 
def convertACData(toConvert):
    if toConvert == 'Y':
        return 1
    if toConvert == 'N':
        return 1/2
    else:
        print('error converting in ACData: ',toConvert)
        return -1

# Electrical system
def convertElectricalSystemData(toConvert):
    if toConvert == 'SBrkr': # Standard Circuit Breakers & Romex
        return 1
    elif toConvert == 'FuseA': # Fuse Box over 60 AMP and all Romex wiring (Average)
        return 4/5	
    elif toConvert == 'FuseF': # 60 AMP Fuse Box and mostly Romex wiring (Fair)
        return 3/5
    elif toConvert == 'FuseP': # 60 AMP Fuse Box and mostly knob & tube wiring (poor)
        return 2/5
    else:
        return 1/5

# Get max sqft with index argument
def getMaxSqFt(matrix,column):
    max = 0
    
    for row in range(0,len(matrix)):
        if matrix[row][column] == 'NA':
            matrix[row][column] = 0
        if int(matrix[row][column]) > max:
            max = int(matrix[row][column])
    return max


# Convert square feet
def convertSqFtData(toConvert,max):
    if max <= 0:
        return 0
    else:
        return int(toConvert)/max

# Kitchen quality 
def convertKitchenQualityData(toConvert):
    total = 5
    if toConvert == 'Ex': #	Excellent
        return 5/total
    elif toConvert == 'Gd': # Good
        return 4/total
    elif toConvert == 'TA': # Typical/Average
        return 3/total
    elif toConvert == 'Fa': # Fair
        return 2/total
    elif toConvert == 'Po': # Poor
        return  1/total
    else:
        print('error converting in KitchenQualityData: ',toConvert)
        return -1
# Home functionality (Assume typical unless deductions are warranted)
def convertFunctionalityData(toConvert):
    total = 8
    if toConvert == 'Typ': # Typical Functionality
        return 1
    elif toConvert == 'Min1': #	Minor Deductions 1
        return 7/total
    elif toConvert == 'Min2': #	Minor Deductions 2
        return 6/total
    elif toConvert == 'Mod': # Moderate Deductions
        return 5/total
    elif toConvert == 'Maj1': #	Major Deductions 1
        return 4/total
    elif toConvert == 'Maj2': #	Major Deductions 2
        return 3/total
    elif toConvert == 'Sev': # Severely Damaged
        return 2/total
    elif toConvert == 'Sal': #	Salvage only
        return 1/total
    else:
        print('error converting in functionalityData: ',toConvert)
        return -1

# Garage quality
def convertGarageQuality(toConvert):
    total = 6
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 5/total
    elif toConvert == 'TA': # Typical/Average
        return 4/total
    elif toConvert == 'Fa': # Fair
        return 3/total
    elif toConvert == 'Po': # Poor
        return 2/total
    else:
        return 1/total

# convert to int
def convertToInt(toConvert):
    if toConvert == 'NA':
        return 0
    else:
        return int(toConvert)

# Garage location
def convertGarageLocData(toConvert):
    if toConvert == '2Types': #	More than one type of garage
        return 1
    elif toConvert == 'Attchd': # Attached to home
        return 6/7
    elif toConvert == 'Basment': # Basement Garage
        return 5/7
    elif toConvert == 'BuiltIn': #	Built-In (Garage part of house - typically has room above garage)
        return 4/7
    elif toConvert == 'CarPort': # Car Port
        return 3/7
    elif toConvert ==  'Detchd': #	Detached from home
        return 2/7
    else:
        return 1/7

# Garage condition 
def convertGarageCondData(toConvert):
    total = 6
    if toConvert == 'Ex': #	Excellent
        return 1
    elif toConvert == 'Gd': # Good
        return 5/total
    elif toConvert == 'TA': # Typical/Average
        return 4/total
    elif toConvert == 'Fa': # Fair
        return 3/total
    elif toConvert == 'Po': # Poor
        return 2/total
    else:
        return 1/total

# Interior finish of the garage
def convertInteriorFinishGarageData(toConvert):
    if toConvert == 'Fin': # Finished
        return 1
    elif toConvert == 'RFn': # Rough Finished
        return 3/4	
    elif toConvert == 'Unf': # Unfinished
        return 2/4
    else:
        return 1/4

# paved drive
def convertPavedDriveData(toConvert):
    if toConvert == 'Y':
        return 1
    else:
        return 1/2

# Fence Quality
def convertFenceQualData(toConvert):
    if toConvert == 'GdPrv': #	Good Privacy
        return 1
    elif toConvert == 'MnPrv': # Minimum Privacy
        return 4/5
    elif toConvert == 'GdWo': #	Good Wood
        return 3/5
    elif toConvert == 'MnWw': #	Minimum Wood/Wire
        return 2/5
    else:
        return 1/5

# Miscellaneous feature not covered in other categories
def convertMiscFeatureData(toConvert):
    if toConvert == 'Elev': # Elevator
        return 1
    elif toConvert == 'Gar2': #	2nd Garage (if not described in garage section)
        return 5/6
    elif toConvert == 'Othr': #	Other
        return 4/6
    elif toConvert == 'Shed': #	Shed (over 100 SF)
        return 3/6
    elif toConvert == 'TenC': #	Tennis Court
        return 2/6
    else:
        return 1/6

# Condition of sale
def convertSaleCondData(toConvert):
    if toConvert == 'Normal': #	Normal Sale
        return 1
    elif toConvert == 'Abnorml': # Abnormal Sale -  trade, foreclosure, short sale
        return 5/6
    elif toConvert == 'AdjLand': # Adjoining Land Purchase
        return 4/6
    elif toConvert == 'Alloca': # Allocation - two linked properties with separate deeds, typically condo with a garage unit	
        return 3/6
    elif toConvert == 'Family': # Sale between family members
        return 2/6
    elif toConvert == 'Partial': #	Home was not completed when last assessed (associated with New Homes)
        return 1/6
    else:
        return 0

# Type of sale
def convertSaleTypeData(toConvert):
    if toConvert == 'WD': #	Warranty Deed - Conventional
        return 1
    elif toConvert == 'CWD': #	Warranty Deed - Cash
        return 9/10
    elif toConvert == 'VWD': #	Warranty Deed - VA Loan
        return 8/10
    elif toConvert == 'New': # Home just constructed and sold
        return 7/10
    elif toConvert == 'COD': # Court Officer Deed/Estate
        return 6/10
    elif toConvert == 'Con': # Contract 15% Down payment regular terms
        return 5/10
    elif toConvert == 'ConLw': # Contract Low Down payment and low interest
        return 4/10
    elif toConvert == 'ConLI': # Contract Low Interest
        return 3/10
    elif toConvert == 'ConLD': # Contract Low Down
        return 2/10
    else:
        return 1/10



def convertData(matrix):
    mSclass = 1
    zone = 2
    lotFrontage = 3
    lotFrontageMax = getMaxSqFt(matrix,lotFrontage)
    lotArea = 4
    lotAreaMax = getLotAreaMax(matrix)
    street = 5
    alley = 6
    lotShape = 7
    landContour = 8
    utilities = 9
    lotConfig = 10
    landSlope = 11
    neighborhood = 12
    condition1 = 13
    condition2 = 14
    bldgType = 15
    houseStyle = 16
    overallQuality = 17
    overallCondition = 18
    built = 19
    remodeled = 20
    roofStyle = 21
    roofMaterial = 22
    exteriorCovering1 = 23
    exteriorCovering2 = 24
    msnVeneerType = 25
    msnVeneerArea = 26
    msnVeneerAreaMax = getMaxSqFt(matrix,msnVeneerArea)
    exteriorQual = 27
    exteriorCond = 28
    foundation = 29
    basementQual = 30
    basementCond = 31
    basementExp = 32
    basementFinishType1 = 33
    basementFinishSqft1 = 34
    basementFinishSqft1Max = getMaxSqFt(matrix,basementFinishSqft1)
    basementFinishType2 = 35
    basementFinishSqft2 = 36
    basementFinishSqft2Max = getMaxSqFt(matrix,basementFinishSqft2)
    unfinishedBaseSqft = 37
    unfinishedBaseSqftMax = getMaxSqFt(matrix,unfinishedBaseSqft)
    totalBasementSqft = 38
    totalBasementSqftMax = getMaxSqFt(matrix,totalBasementSqft)
    heating = 39
    heatingQual = 40
    AirCon = 41
    electrical = 42
    firstSqFt = 43
    firstSqFtMax = getMaxSqFt(matrix,firstSqFt)
    secondSqFt = 44
    secondSqFtMax = getMaxSqFt(matrix,secondSqFt)
    lowQualityFin = 45
    lowQualityFinMax = getMaxSqFt(matrix,lowQualityFin)
    groundLivingSqft = 46
    groundLivingSqftMax = getMaxSqFt(matrix,groundLivingSqft)
    kitchenQual = 53
    functionality = 55
    fireplaceQual = 57
    garageType = 58
    garageYearBuild = 59
    garageFinish = 60
    garageArea = 62
    garageAreaMax = getMaxSqFt(matrix,garageArea)
    garageQual = 63
    garageCond = 64
    pavedDrive = 65
    woodDeckSqft = 66
    woodDeckSqftMax = getMaxSqFt(matrix,woodDeckSqft)
    openPorchSqft = 67
    openPorchSqftMax = getMaxSqFt(matrix,openPorchSqft)
    enclosedPorchSqft = 68
    enclosedPorchSqftMax = getMaxSqFt(matrix,enclosedPorchSqft)
    SsnPorchSqft = 69
    SsnPorchSqftMax = getMaxSqFt(matrix,SsnPorchSqft)
    screenPorchSqft = 70
    screenPorchSqftMax = getMaxSqFt(matrix,screenPorchSqft)
    poolArea = 71
    poolAreaMax = getMaxSqFt(matrix,poolArea)
    fenceQual = 73
    miscFeature = 74
    saleCondition = 79
    
    masonryVeneerMax = getMasonryVeneerMax(matrix)
    
    for row in range(0,len(matrix)):
        matrix[row][mSclass] = convertMSSubClassData(matrix[row][mSclass])
        matrix[row][zone] = convertMSZoningData(matrix[row][zone]) # zones
        matrix[row][lotFrontage] = convertLotFrontageData(matrix[row][lotFrontage],lotFrontageMax)
        matrix[row][lotArea] = convertLotAreaData(matrix[row][lotArea],lotAreaMax)
        matrix[row][street] = convertStreetData(matrix[row][street]) # street paved
        matrix[row][alley] = convertAlleyData(matrix[row][alley])
        matrix[row][lotShape] = convertLotShapeData(matrix[row][lotShape])
        matrix[row][landContour] = convertLandContourData(matrix[row][landContour])
        matrix[row][utilities] = convertUtilitiesData(matrix[row][utilities])
        matrix[row][lotConfig] = convertLotConfigData(matrix[row][lotConfig])
        matrix[row][landSlope] = convvertSlopeData(matrix[row][landSlope])
        matrix[row][neighborhood] = convertNeighborhoodData(matrix[row][neighborhood])
        matrix[row][condition1] = convertCondData(matrix[row][condition1])
        matrix[row][condition2] = convertCondData(matrix[row][condition2])
        matrix[row][bldgType] = convertBldgTypeData(matrix[row][bldgType])
        matrix[row][houseStyle] = convertStyleDwellingData(matrix[row][houseStyle])
        matrix[row][overallQuality] = convertOverAllQualityData(matrix[row][overallQuality])
        matrix[row][overallCondition] = convertOverAllConditionData(matrix[row][overallCondition])
        year = str(matrix[row][built])
        year = year.translate(str.maketrans('','',string.punctuation))
        matrix[row][built] = convertYearBuildData(year)
        yearRemodeled = str(matrix[row][remodeled])
        yearRemodeled = yearRemodeled.translate(str.maketrans('','',string.punctuation))
        matrix[row][remodeled] = convertYearBuildData(yearRemodeled)
        matrix[row][roofStyle] = convertRoofStyleData(matrix[row][roofStyle])
        matrix[row][roofMaterial] = convertRoofMaterialData(matrix[row][roofMaterial])
        matrix[row][exteriorCovering1] = convertExeriorCoveringData(matrix[row][exteriorCovering1])
        matrix[row][exteriorCovering2] = convertExeriorCoveringData(matrix[row][exteriorCovering2])
        matrix[row][msnVeneerType] = convertMasonryVeneerTypeData(matrix[row][msnVeneerType])
        matrix[row][msnVeneerArea] = convertMasonryVeneerAreaData(matrix[row][msnVeneerArea],msnVeneerAreaMax)
        matrix[row][exteriorQual] = convertExternalQualData(matrix[row][exteriorQual])
        matrix[row][exteriorCond] = convertExteriorCondData(matrix[row][exteriorCond])
        matrix[row][foundation] = converrtTypeFoundationData(matrix[row][foundation])
        matrix[row][basementQual] = convertBasementQualData(matrix[row][basementQual])
        matrix[row][basementCond] = convertBasementCondData(matrix[row][basementCond])
        matrix[row][basementExp] = convertBasementExposureData(matrix[row][basementExp])
        matrix[row][basementFinishType1] = convertBasementFinishTypeData(matrix[row][basementFinishType1])
        matrix[row][basementFinishSqft1] = convertSqFtFinishedBasementData(matrix[row][basementFinishSqft1],basementFinishSqft1Max)
        matrix[row][basementFinishType2] = convertBasementFinishTypeData(matrix[row][basementFinishType2])
        matrix[row][basementFinishSqft2] = convertSqFtFinishedBasementData(matrix[row][basementFinishSqft2],basementFinishSqft2Max)
        matrix[row][unfinishedBaseSqft] = convertSqFtData(matrix[row][unfinishedBaseSqft],unfinishedBaseSqftMax)
        matrix[row][totalBasementSqft] = convertSqFtData(matrix[row][totalBasementSqft],totalBasementSqftMax)
        matrix[row][heating] = convertTypeOfHeatData(matrix[row][heating])
        matrix[row][heatingQual] = convertHeatingQualAndCondData(matrix[row][heatingQual])
        matrix[row][AirCon] = convertACData(matrix[row][AirCon])
        matrix[row][electrical] = convertElectricalSystemData(matrix[row][electrical])
        matrix[row][firstSqFt] = convertSqFtData(matrix[row][firstSqFt],firstSqFtMax)
        matrix[row][secondSqFt] = convertSqFtData(matrix[row][secondSqFt],secondSqFtMax)
        matrix[row][lowQualityFin] = convertSqFtData(matrix[row][lowQualityFin],lowQualityFinMax)
        matrix[row][groundLivingSqft] = convertSqFtData(matrix[row][groundLivingSqft],groundLivingSqftMax)
        matrix[row][47] = convertToInt(matrix[row][47])
        matrix[row][48] = convertToInt(matrix[row][48])
        matrix[row][49] = convertToInt(matrix[row][49])
        matrix[row][50] = convertToInt(matrix[row][50])
        matrix[row][51] = convertToInt(matrix[row][51])
        matrix[row][52] = convertToInt(matrix[row][52])
        matrix[row][kitchenQual] = convertKitchenQualityData(matrix[row][kitchenQual])
        matrix[row][54] = convertToInt(matrix[row][54])
        matrix[row][functionality] = convertFunctionalityData(matrix[row][functionality])
        matrix[row][56] = convertToInt(matrix[row][56])
        matrix[row][fireplaceQual] = convertCondData(matrix[row][fireplaceQual])
        matrix[row][garageType] = convertGarageLocData(matrix[row][garageType])
        garageYear = str(matrix[row][garageYearBuild])
        garageYear = garageYear.translate(str.maketrans('','',string.punctuation))
        matrix[row][garageYearBuild] = convertYearBuildData(garageYear)
        matrix[row][garageFinish] = convertInteriorFinishGarageData(matrix[row][garageFinish])
        matrix[row][61] = convertToInt(matrix[row][61])
        matrix[row][garageArea] = convertSqFtData(matrix[row][garageArea],garageAreaMax)
        matrix[row][garageQual] = convertGarageQuality(matrix[row][garageQual])
        matrix[row][garageCond] = convertGarageCondData(matrix[row][garageCond])
        matrix[row][pavedDrive] = convertPavedDriveData(matrix[row][pavedDrive])
        matrix[row][woodDeckSqft] = convertSqFtData(matrix[row][woodDeckSqft],woodDeckSqftMax)
        matrix[row][openPorchSqft] = convertSqFtData(matrix[row][openPorchSqft],openPorchSqftMax)
        matrix[row][enclosedPorchSqft] = convertSqFtData(matrix[row][enclosedPorchSqft],enclosedPorchSqftMax)
        matrix[row][SsnPorchSqft] = convertSqFtData(matrix[row][SsnPorchSqft],SsnPorchSqftMax)
        matrix[row][screenPorchSqft] = convertSqFtData(matrix[row][screenPorchSqft],screenPorchSqftMax)
        matrix[row][poolArea] = convertSqFtData(matrix[row][poolArea],poolAreaMax)
        matrix[row][72] = convertCondData(matrix[row][72])
        matrix[row][fenceQual] = convertFenceQualData(matrix[row][fenceQual])
        matrix[row][miscFeature] = convertMiscFeatureData(matrix[row][miscFeature])
        matrix[row][75] = convertToInt(matrix[row][75])
        matrix[row][76] = convertToInt(matrix[row][76])
        yearSold = str(matrix[row][built])
        yearSold = yearSold.translate(str.maketrans('','',string.punctuation))
        matrix[row][77] = convertYearBuildData(yearSold)
        matrix[row][78] = convertSaleTypeData(matrix[row][78])
        matrix[row][saleCondition] = convertSaleCondData(matrix[row][saleCondition])
        
        # for any columns that have a 'NA' in it, replace with a zero.
    for row in range(0, len(matrix)):
        for feature in range(0, 80):
            if matrix[row][feature] == 'NA':
                matrix[row][feature] = 0

def createTruthValues(truth,source):
    print('length of truth: ',len(truth))
    for row in range(0,len(truth)):
        truth[row] = get_class(source[row][80])

def getData(file,array):
    with open(file, newline='\n') as csvfile:  # read in from test.csv for test data
        csv_reader = csv.reader(csvfile, delimiter=',') # reads in
        for row in csv_reader:  # append stuff from each row/data point
            array.append(row)  # append

        