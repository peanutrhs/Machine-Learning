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
    convertData(train)
    

   
       
      
    print(len(train))
    print((len(train[0])))