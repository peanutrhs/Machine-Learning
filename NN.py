import csv
from operator import ne
from re import T
import numpy as np
import math
from helperFunctions import *
import string
import os




if __name__ == "__main__":  # main function call
    conf_mat = np.zeros((6, 6))
    train = [] # traindata
    test = [] # testdata
    dir = os.listdir('.')  # get the 
    
    testdir = dir[0] + '/test.csv'
    traindir = dir[0] + '/train.csv'

    # Get the data and import into arrays
    getData(testdir,test)
    getData(traindir,train)
   
    # convert all text to a numerical value
    
    numHiddenUnits = 20
    # train (1461,81)
    train = np.array(train)
    train = np.delete(train,0,0) # delete the row header
    train[:,0] = 1 # set id to bias in train
    convertData(train)
    for row in range(0,len(train)):
        print(train[row])
    # create the truth with the assigned class. 
    truth = np.zeros((1460))
    createTruthValues(truth,train)
    train = np.delete(train,80,1) # delete the home values out of training set
    #print('train:',train)
    HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
    
    #  train[i] = (81,1460), hiddenLayer = (1460,20), inputToHiddenWeights = (20,1460)
    #print("train[0] shape: ", train[0].shape)
    inputToHiddenWeights = np.random.default_rng().uniform(low=-0.05, high = 0.05, size = (80,numHiddenUnits))
    hiddenToOutputWeights = np.random.default_rng().uniform(low = -0.05, high = 0.05, size = (numHiddenUnits+1,10))
    # train[i] => (80,) inputToHiddenWeights => (1460,20)
    #for i in range(0,len(train)):
     #   hiddenLayerSum = np.dot(train[i],inputToHiddenWeights)
    #print("hiddenLayerSum: ")
    #print(hiddenLayerSum)
    # forward propagation

    # apply activation function

    # apply activation function (sigmoid) to sum of weights times inputs to each output unit

    # iterpret the output layer as a classification
       
      
    print(len(train))
    print((len(train[0])))