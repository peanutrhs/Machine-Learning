#Imports
from cmath import e
import enum
from http.client import PRECONDITION_FAILED
from logging.handlers import DEFAULT_SOAP_LOGGING_PORT
from re import A
from urllib.request import parse_keqv_list
from xml.etree.ElementTree import tostring
import numpy as np
from numpy import genfromtxt, transpose
import matplotlib.pyplot as plt
import random
import seaborn as sb
import pandas as pd
import math as mth
#IMPORT DATA
train = genfromtxt('mnist_train.csv',delimiter=',')
train = np.array(train)
np.delete(train,0,0) # delete the label row in the training set.
test = genfromtxt('mnist_test.csv',delimiter=',')
test = np.array(test)
np.delete(test,0,0) # delete the label row in the test set.
batchTrain = np.zeros((1000,785))
for x in range(0,1000):
    batchTrain[x] = train[x]

#INITIALIZE ALL VARIABLE AND MATRICES
eta = [0.2] # eta for each different eta
# replace the first column of train to be 1 (bias)
    # This is the input layer


# build weights matrix
numHiddenUnits = 20
trainAccuracy = []
testAccuracy = []
inputToHiddenWeights = np.random.default_rng().uniform(low=-0.05, high = 0.05, size = (785,numHiddenUnits))
hiddenToOutputWeights = np.random.default_rng().uniform(low = -0.05, high = 0.05, size = (numHiddenUnits+1,10))
DeltaHiddenOutputWeights = np.zeros((10,numHiddenUnits+1))# output-to-hidden layer , using for updating actual hiddenweights
DeltaHiddenInputWeights = np.zeros((numHiddenUnits,785)) # hidden-to-Input weights, using to update inputToHiddenWeights
HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
correctOutput = 0  # for recording number of correct
correctTest = 0
HiddenLayer[:,0] =1  #add bias to Hidden Layer nodes
epoch = 0
trueValues = [i[0] for i in train]  
# normalize training set
i = 1
for i , x in enumerate(train):
    train[i] = train[i]/255
    
i = 1
# normalize test set
for i , x in enumerate(test):
    test[i] = test[i]/255
#do a confusion matrix...
confusionMatrixTest = np.zeros((10,10),dtype=int)
falsePositive = 0
falseNegative = 0
truePositive = 0
trueNegative = 0
#identity matrix aka ground-truth matrix. This is what is known to be true. i.e. (0 -9) 10 vector
# a 0 would be [1,0,0,0,0,0,0,0,0,0], a 1 [0,1,0,0,0,0,0,0,0,0]
groundTruth = np.identity(10,dtype = int); #this is a 10 X 10 I matrix   
trueValues = np.array(trueValues).astype(int)
trueValues = trueValues.reshape(60000,1) # need to change to 60,000 during full run (training size)
testTrueValues = [i[0] for i in test]
testTrueValues = np.array(testTrueValues).astype(int)
testTrueValues = testTrueValues.reshape(10000,1)
momentum = 0.9 # change during experimemts
train[:,0] = 1 # bias for input

while(epoch < 50):
    correctOutput = 0
    print("starting Epoch ",epoch)
    for i in range(0,len(train)-1): # train[i] = (1,785), hiddenLayer = (785,20), inputToHiddenWeights = (20,785)
        # Hidden Layer before activation 
        hiddenLayerSum = np.dot(np.transpose(train[i]),inputToHiddenWeights) # calculate hiddenLayer => (785,20)
        
        #squash hidden layer
        for j in range(0,hiddenLayerSum.size):
            hiddenLayerSum[j] = 1/(1+ np.exp(-hiddenLayerSum[j])) # => (20,1)
            HiddenLayer[j+1] = hiddenLayerSum[j] #putting into hiddenLayer
        
        for k in range(0,hiddenLayerSum.size):
            outputLayerSum = np.dot(np.transpose(hiddenToOutputWeights),HiddenLayer) # => (10,1)
        #squash output Layer
        for l in range(0,outputLayerSum.size):
            outputLayerSum[l] = 1/(1 + np.exp(-outputLayerSum[l])) # => (10,1)
        #Calculate error terms: => 10 x 1 vector where 0.9 is in train[i] value, and 0.1 is not
        tk = np.reshape(groundTruth[trueValues[i]],(10,1)).astype(float)
        tk = np.select([tk==1,tk==0],[0.9,0.1],tk)
        prediction = np.argmax(outputLayerSum)
        #prediction = 5
        #trueValues[i] = 5
        sum = 0
        
        if(prediction!=trueValues[i]):
            outputError = np.zeros((10,1))
            hiddenError = np.zeros((numHiddenUnits,1))
            for m in range(0,len(outputError)):
                outputError[m] = outputLayerSum[m]*(1-outputLayerSum[m])*(tk[m]-outputLayerSum[m]) #producing outputError
            for n in range(0,len(hiddenToOutputWeights)-1):
                
                #for o in range(0,10):
                    #hiddenToOutputWeights => (21,10), outputError =>(10,1)
                    # row i, column j for A[i][j]
                sum = np.dot(hiddenToOutputWeights,outputError)
                sum = np.sum(sum)
                    
                #hiddenLayer => (21,1), hiddenError = > (21,1)
                hiddenError[n] = HiddenLayer[n+1]*(1-HiddenLayer[n+1])*sum #deltaOutput
            #eta*deltaJ*input +momentum*previousDelta
            
            DeltaHiddenOutputWeights = eta[0]*outputError*np.transpose(HiddenLayer) + (momentum*DeltaHiddenOutputWeights ) #weight updates for output weights
            DeltaHiddenInputWeights = eta[0]*hiddenError*train[i] + (momentum*DeltaHiddenInputWeights) #weight update to hidden weights
            
            hiddenToOutputWeights += DeltaHiddenOutputWeights .T #transpose, updating weights
            inputToHiddenWeights += DeltaHiddenInputWeights.T  #updating weights
    
        if(trueValues[i]==prediction):
            correctOutput = correctOutput +  1
            confusionRow = prediction
            col = trueValues[i]
            confusionMatrixTest[confusionRow][col] += 1
    trainAccuracy.append(correctOutput/len(train))
    epoch += 1
   
    print("correct: ",correctOutput)

    print(trainAccuracy)

plt.plot(trainAccuracy)
plt.plot(testAccuracy)
plt.title('Training & Test Plot')
plt.suptitle('eta = 0.1')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend('trainig','test')
plt.show()
        



  
   

    
