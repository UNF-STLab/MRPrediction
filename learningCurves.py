import PyML
from PyML.utils import misc
import random
import numpy as np

  
def getPosNegPatternIDs(classLabelFileName):
	f = open(classLabelFileName, 'r')
        posIDs=[]
	negIDs=[]
	lineCnt=0
	for line in f:
                fields=line.strip('\n').split(',')
		if fields[1]=='1':
			posIDs.append(lineCnt)
		else:
			negIDs.append(lineCnt)
                lineCnt+=1
        f.close()
        return posIDs,negIDs

def getRandomSample(origSet,portion):
	numSamples=int(len(origSet)*portion)
	print numSamples
	random.shuffle(origSet)
	return origSet[0:numSamples]

def createStratifiedTrainSet(trainIDs,pos,neg,portion):
	posIDs=[]
	negIDs=[]
	for i in trainIDs:
		if i in pos:
			posIDs.append(i)
		if i in neg:
			negIDs.append(i)
	trainSet=getRandomSample(posIDs,portion)
	temp=getRandomSample(negIDs,portion)
	for i in temp:
		trainSet.append(i)
	return trainSet
def createBigTrainTestSets(pos,neg):
	#pos,neg=getPosNegPatternIDs(labelFile) 
	
	posTestIDs=getRandomSample(pos,0.1)
	negTestIDs=getRandomSample(neg,0.1)
	testIDs=posTestIDs
	for i in negTestIDs:
		testIDs.append(i)
	trainIDs=[]
	for i in pos:
		if i not in testIDs:
			trainIDs.append(i)
	for i in neg:
                if i not in testIDs:
                        trainIDs.append(i)
	return trainIDs,testIDs

def findBestCForLamda(origKData,trainIDs):
        cVals=[0.1,1,10,100,1000]
        cResults={}
        for val in cVals:
                s=PyML.SVM(C=val)
                trainingData = origKData.__class__(origKData, deepcopy = s.deepcopy,patterns = trainIDs)
                r=s.stratifiedCV(trainingData,numFolds=2)
                cResults[val]=r.getROC()
        bestC=[key for key,val in cResults.iteritems() if val == max(cResults.values())][0]
        maxROC=max(cResults.values())
        return bestC,maxROC

def findBestLamdaForTrainingSet(train,test,origLabelFileName,kmLoc):
        results={}
        cVals=[0.1,1,10,100,1000]
        for lamda in range(1,10):
                origkm=PyML.KernelData(kmLoc+'mod_km_cfg_1_10_0.'+str(lamda))
                origkm.attachKernel(normalization = 'cosine')
                labels=PyML.Labels(origLabelFileName)
                origkm.attachLabels(labels)
                """
                s=PyML.SVM(C=10)
                trainingData = origkm.__class__(origkm, deepcopy = s.deepcopy,patterns = train)
                r=s.stratifiedCV(trainingData,numFolds=10)
                """
                bestCForLamda,maxROC=findBestCForLamda(origkm,train)
                results[lamda,bestCForLamda]=maxROC
                #print results
        maxlamdaAndC=[key for key,val in results.iteritems() if val == max(results.values())][0]
        return  maxlamdaAndC 


def getResults(trainIDs,testIDs,origLabelFileName,kmLoc):
	lamdaAndC=findBestLamdaForTrainingSet(trainIDs,testIDs,origLabelFileName,kmLoc)
	labels=PyML.Labels(origLabelFileName)
	kdata=PyML.KernelData(kmLoc+'mod_km_cfg_1_10_0.'+str(lamdaAndC[0]))
	kdata.attachLabels(labels)
	s=PyML.SVM(C=lamdaAndC[1])
 	#trainIDsPortion=getRandomSample(trainIDs,trainPortion)
	r=s.trainTest(kdata,trainIDs,testIDs)
	return r.getROC()

def getValuesForLeariningCurve():
	origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/incClassLabelFinal1_comma'
        kmLoc='/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/'
        #labels=PyML.Labels(origLabelFileName)
        #kdata=PyML.KernelData(km)
        #kdata.attachLabels(labels)
	aucVals={}
	pos,neg=getPosNegPatternIDs(origLabelFileName)
	for i in range(10): 
		results=[]
		train,test=createBigTrainTestSets(pos,neg)
		trainPortion=0.1 
		while trainPortion<=1:
			for k in range(10):
				resultsForPortion=[] 	
				newTrainSet=createStratifiedTrainSet(train,pos,neg,trainPortion)
				r=getResults(newTrainSet,test,origLabelFileName,kmLoc)
				resultsForPortion.append(r)
			results.append(np.mean(resultsForPortion))
			trainPortion+=0.1
		aucVals[i]=results
	print aucVals

	for i in range(10):
		sum=0
		for j in aucVals:
			sum+= aucVals[j][i]
		#print i
		print sum/10
		#print"======"  
		 
getValuesForLeariningCurve()	
