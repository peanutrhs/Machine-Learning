import csv
from operator import ne
from re import T
import numpy as np
import math
from helperFunctions import *
import string

if __name__ == "__main__":  # main function call
    conf_mat = np.zeros((6, 6))
    train = [] # traindata
    test = [] # testdata

    with open('test.csv', newline='\n') as csvfile:  # read in from test.csv for test data
        csv_reader = csv.reader(csvfile, delimiter=',') # reads in
        for row in csv_reader:  # append stuff from each row/data point
            test.append(row)  # append
    with open('train.csv', newline='\n') as csvfile: # same as above but for train
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            train.append(row)
    # for any columns that have a 'NA' in it, replace with a zero.
    for row in range(0, len(train)):
        for feature in range(0, 80):
            if train[row][feature] == 'NA':
                train[row][feature] = 0
    # convert all text to a numerical value
    zone = 2
    street = 5
    utilities = 9
    neighborhood = 12
    condition = 18
    quality = 19
    mSclass = 1
    bldgType = 15
    built = 19
    heating = 39

    for row in range(1,len(train)):
        train[row][zone] = convertMSZoningData(train[row][zone]) # zones
        train[row][street] = convertStreetData(train[row][street]) # street paved
        train[row][utilities] = convertUtilitiesData(train[row][utilities])
        train[row][neighborhood] = convertNeighborhoodData(train[row][neighborhood])
        train[row][condition] = convertOverAllConditionData(train[row][condition])
        train[row][quality] = convertOverAllQualityData(train[row][quality])
        train[row][mSclass] = convertMSSubClassData(train[row][mSclass])
        train[row][bldgType] = convertBldgTypeData(train[row][bldgType])
        year = str(train[row][built])
        year = year.translate(str.maketrans('','',string.punctuation))
        train[row][built] = convertYearBuildData(year)
        train[row][heating] = convertTypeOfHeatData(train[row][heating])


        
    print("train MSZoning:")
    for row in range(0,len(train)):
        print(train[row][heating])
        
    print(len(train))
    print((len(train[0])))