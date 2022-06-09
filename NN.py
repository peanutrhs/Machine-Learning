import csv
from operator import ne
from re import T
import numpy as np
from helperFunctions import *
import os
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt
import random
np.set_printoptions(precision=5)




if __name__ == "__main__":  # main function call
    Debug = False
    
    test = [] # testdata
    dir = os.listdir('.')  # get the 
    
    testdir = dir[0] + '/test.csv'
    traindir = dir[0] + '/train.csv'
    eta = [0.01] # eta for each different eta
    # Get the data and import into arrays
    getData(testdir,test)
    
    
    # convert all text to a numerical value
    trainAccuracy = []
    testAccuracy = []
    numHiddenUnits = 40
    HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
    # train (1461,81)
    
    
    groundTruth = np.identity(6,dtype = int); #this is a 5 X 5 I matrix  
    # create the truth with the assigned class. 
    truth = np.zeros((1460)).astype(int)
    
    
    
    HiddenLayer = np.zeros((numHiddenUnits+1,1)) # hold all my outputs from initial dot product
    momentum = 0.9 # change during experimemts
    #  train[i] = (80,1460), hiddenLayer = (1460,20), inputToHiddenWeights = (20,1460)
    
    inputToHiddenWeights = np.random.default_rng().uniform(low=-0.05, high = 0.05, size = (80,numHiddenUnits))
    # 5 is for number of classes
    hiddenToOutputWeights = np.random.default_rng().uniform(low = -0.05, high = 0.05, size = (numHiddenUnits+1,5))
    DeltaHiddenOutputWeights = np.zeros((5,numHiddenUnits+1))# output-to-hidden layer , using for updating actual hiddenweights
    DeltaHiddenInputWeights = np.zeros((numHiddenUnits,80)) # hidden-to-Input weights, using to update inputToHiddenWeights
    # train[i] => (80,) inputToHiddenWeights => (1460,20)
   
    epoch = 0 
    while(epoch <400):
        print("starting Epoch ",epoch)
        falsePositive = 0
        falseNegative = 0
        truePositive = 0
        trueNegative = 0
        train = [] # traindata
        getData(traindir,train)
        train = np.array(train)
        train = np.delete(train,0,0) # delete the row header
        train[:,0] = 1 # set id to bias in train
        if Debug:
            print("train: ",train)
        np.random.shuffle(train)
        convertData(train)
        if Debug:
            print("train Shuffled:")
            print(train)
        train = train.astype(float)
        createTruthValues(truth,train)
        train = np.delete(train,80,1) # delete the home values out of training set
        if Debug:
            print('train:',train)
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
            if  Debug:
                print('prediction:',prediction)
            #print('Prediction: ', prediction, ' truth[',i,']: ',truth[i])
            if prediction != truth[i]:
                if Debug:
                    print('truth[i]!=prediction')
                    print('prediction: ', prediction, ' truth[i]:',truth[i],' tk[prediction]:',tk[prediction])
                if tk[prediction] == 0.1:
                    trueNegative += 1
                else:
                    falsePositive += 1
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
                if Debug:
                    print('truth[i]==prediction')
                    print('prediction: ', prediction, ' truth[i]:',truth[i],' tk[prediction]:',tk[prediction])
                if tk[prediction] == 0.9:
                    truePositive += 1
                else:
                    falsePositive += 1
                correctOutput +=  1
                confusionRow = prediction
                confusioncol = truth[i]
                confusionMatrixTest[confusionRow][confusioncol] += 1
        trainAccuracy.append(correctOutput/len(train))
        if Debug:
            print("confusion Matrix: ")
            print(confusionMatrixTest)
        print("correctOutput: ",correctOutput)
        print("trainAccuracy: ")
        print(trainAccuracy)
        sensitivity = truePositive/(truePositive+falseNegative)
        accuracy = (truePositive+falsePositive)/(truePositive+falsePositive+trueNegative+falseNegative)
        specificity = trueNegative/(trueNegative + falsePositive)
        precision = truePositive/(truePositive + falsePositive)
        recall = truePositive/(truePositive + falseNegative)
        print('sensitivity: ',sensitivity)
        print('accuracy: ',accuracy)
        print('specificity: ',specificity)
        print('precision: ',precision)
        print('recall: ', recall)
        print('falsePositive: ',falsePositive)
        print('falseNegative:',falseNegative)
        print('truePositive: ',truePositive)
        print('trueNegative: ',trueNegative)
        epoch += 1
    maxAccuracy= 0.0
    for row in range(0,len(testAccuracy)):
        if testAccuracy[row]>  maxAccuracy:
            maxAccuracy = testAccuracy[row]
    print('maxAccuracy:',maxAccuracy)
    text = 'eta = ' + str(eta[0])
    if Debug:
        print(confusionMatrixTest)
    
    print("highest Accuracy is: ",maxAccuracy)
    plt.plot(trainAccuracy)
    plt.plot(testAccuracy)
    plt.title('Training & Test Plot')
    plt.suptitle(text)
    plt.ylabel('Accuracy')
    plt.xlabel('Epochs')
    plt.legend('trainig','test')
    plt.show()
    df_cm = pd.DataFrame(confusionMatrixTest,range(5),range(5))
    sb.set(font_scale = 1.4)
    sb.heatmap(df_cm,annot=True,annot_kws={"size":30})
    plt.show()     
