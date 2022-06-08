import csv
from operator import ne
from re import T
import numpy as np
import math

from sklearn import preprocessing
from helperFunctions import *
import string
import os
import random
from scipy.special import softmax
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(precision=5)
from sklearn import preprocessing



if __name__ == "__main__":  # main function call
    conf_mat = np.zeros((6, 6))
    train = [] # traindata
    test = [] # testdata
    dir = os.listdir('.')  # get the 
    
    testdir = dir[0] + '/test.csv'
    traindir = dir[0] + '/train.csv'
    eta = [0.001] # eta for each different eta
    # Get the data and import into arrays
    getData(testdir,test)
    getData(traindir,train)
    
    # convert all text to a numerical value
    trainAccuracy = []
    testAccuracy = []
    numHiddenUnits = 40
    HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
    # train (1461,81)
    train = np.array(train)
    train = np.delete(train,0,0) # delete the row header
    train[:,0] = 1 # set id to bias in train
    convertData(train)
    train = train.astype(float)
    groundTruth = np.identity(6,dtype = int); #this is a 5 X 5 I matrix  
    # create the truth with the assigned class. 
    truth = np.zeros((1460)).astype(int)
    
    falsePositive = 0
    falseNegative = 0
    truePositive = 0
    trueNegative = 0
    createTruthValues(truth,train)
    
    train = np.delete(train,80,1) # delete the home values out of training set
    #print('train:',train)
    HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
    momentum = 0.8 # change during experimemts
    #  train[i] = (80,1460), hiddenLayer = (1460,20), inputToHiddenWeights = (20,1460)
    #print("train[0] shape: ", train[0].shape)
    inputToHiddenWeights = np.random.default_rng().uniform(low=-0.05, high = 0.05, size = (80,numHiddenUnits))
    # 5 is for number of classes
    hiddenToOutputWeights = np.random.default_rng().uniform(low = -0.05, high = 0.05, size = (numHiddenUnits+1,5))
    DeltaHiddenOutputWeights = np.zeros((5,numHiddenUnits+1))# output-to-hidden layer , using for updating actual hiddenweights
    DeltaHiddenInputWeights = np.zeros((numHiddenUnits,80)) # hidden-to-Input weights, using to update inputToHiddenWeights
    # train[i] => (80,) inputToHiddenWeights => (1460,20)
   
    epoch = 0
    while(epoch <50):
        print("starting Epoch ",epoch)
        correctOutput = 0
        confusionMatrixTest = np.zeros((5,5),dtype=int)
        for i in range(0,len(train)):
            # Hidden Layer before activation 
            hiddenLayerSum = np.dot(np.transpose(train[i]),inputToHiddenWeights) # hiddenLayerSum (1,20)
            
            #squash hidden layer
            for j in range(0,hiddenLayerSum.size):
                hiddenLayerSum[j] = 1/(1+ np.exp(-hiddenLayerSum[j])) # => (20,1)
                HiddenLayer[j+1] = hiddenLayerSum[j] #putting into hiddenLayer

            for k in range(0,hiddenLayerSum.size):
                outputLayerSum = np.dot(np.transpose(hiddenToOutputWeights),HiddenLayer) # => (5,1)
            
            #squash output Layer
            for l in range(0,outputLayerSum.size):
                outputLayerSum[l] = 1/(1 + np.exp(-outputLayerSum[l])) # => (5,1)
            # iterpret the output layer as a classification
            tk = np.reshape(groundTruth[truth[i]],(6,1)).astype(float)
            tk = np.select([tk==1,tk==0],[0.9,0.1],tk)
            prediction = np.argmax(outputLayerSum)
            #print('Prediction: ', prediction, ' truth[',i,']: ',truth[i])
            if prediction != truth[i]:
                outputError = np.zeros((5,1))
                hiddenError = np.zeros((numHiddenUnits,1))
                for m in range(0,len(outputError)):
                    outputError[m] = outputLayerSum[m]*(1-outputLayerSum[m])*(tk[m]-outputLayerSum[m]) #producing outputError
                for n in range(0,len(hiddenToOutputWeights)-1):
                    sum = np.dot(hiddenToOutputWeights,outputError)
                    sum = np.sum(sum)
                    #hiddenLayer => (21,1), hiddenError = > (21,1)
                    hiddenError[n] = HiddenLayer[n+1]*(1-HiddenLayer[n+1])*sum #deltaOutput
                    
                DeltaHiddenOutputWeights = eta[0]*outputError*np.transpose(HiddenLayer) + (momentum*DeltaHiddenOutputWeights ) #weight updates for output weights
                DeltaHiddenInputWeights = eta[0]*hiddenError*train[i] + (momentum*DeltaHiddenInputWeights) #weight update to hidden weights
                hiddenToOutputWeights += DeltaHiddenOutputWeights .T #transpose, updating weights
                inputToHiddenWeights += DeltaHiddenInputWeights.T  #updating weights
            if(truth[i]==prediction):
                
                correctOutput +=  1
                confusionRow = prediction
                confusioncol = truth[i]
                confusionMatrixTest[confusionRow][confusioncol] += 1
        trainAccuracy.append(correctOutput/len(train))
        print("confusion Matrix: ")
        print(confusionMatrixTest)
        print("correctOutput: ",correctOutput)
        print("trainAccuracy: ")
        print(trainAccuracy)
        epoch += 1
        
    #---------------------------------------TEST-------------------------------------#
testtruth = np.zeros((1461)).astype(int)
createTruthValues(testtruth,test)
test = np.array(test)
test = np.delete(test,0,0) # delete the row header
test[:,0] = 1 # set id to bias in train
convertData(test)
test = test.astype(float)
correctOutput = 0
confusionMatrixTest = np.zeros((5,5),dtype=int)
for i in range(0,len(test)):
# Hidden Layer before activation 
    hiddenLayerSum = np.dot(np.transpose(test[i]),inputToHiddenWeights) # hiddenLayerSum (1,20)
            
    #squash hidden layer
    for j in range(0,hiddenLayerSum.size):
        hiddenLayerSum[j] = 1/(1+ np.exp(-hiddenLayerSum[j])) # => (20,1)
        HiddenLayer[j+1] = hiddenLayerSum[j] #putting into hiddenLayer

        for k in range(0,hiddenLayerSum.size):
            outputLayerSum = np.dot(np.transpose(hiddenToOutputWeights),HiddenLayer) # => (5,1)
            
        #squash output Layer
        for l in range(0,outputLayerSum.size):
            outputLayerSum[l] = 1/(1 + np.exp(-outputLayerSum[l])) # => (5,1)
        # iterpret the output layer as a classification
            
        prediction = np.argmax(outputLayerSum)
        #print('Prediction: ', prediction, ' truth[',i,']: ',truth[i])
        if prediction != testtruth[i]:
            outputError = np.zeros((5,1))
            hiddenError = np.zeros((numHiddenUnits,1))
            for m in range(0,len(outputError)):
                outputError[m] = outputLayerSum[m]*(1-outputLayerSum[m])*(truth[m]-outputLayerSum[m]) #producing outputError
            for n in range(0,len(hiddenToOutputWeights)-1):
                sum = np.dot(hiddenToOutputWeights,outputError)
                sum = np.sum(sum)
            #hiddenLayer => (21,1), hiddenError = > (21,1)
            hiddenError[n] = HiddenLayer[n+1]*(1-HiddenLayer[n+1])*sum #deltaOutput
            if(testtruth[i]==prediction):
                correctOutput +=  1
                confusionRow = prediction
                confusioncol = testtruth[i]
                confusionMatrixTest[confusionRow][confusioncol] += 1
    testAccuracy.append(correctOutput/len(test))
    #---------------------------------------END TEST---------------------------------#
    plt.plot(trainAccuracy)
    plt.plot(testAccuracy)
    plt.title('Training & Test Plot')
    plt.suptitle('eta = 0.1')
    plt.ylabel('Accuracy')
    plt.xlabel('Epochs')
    plt.legend('trainig','test')
    plt.show()
