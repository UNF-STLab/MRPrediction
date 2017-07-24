import PyML
from PyML.utils import misc
import random
import numpy as np

def createStratifiedTestTrainFolds(classifier, data, numFolds = 5, **args) :
    """perform k-fold stratified cross-validation; in each fold the number of
    patterns from each class is proportional to the relative fraction of the
    class in the dataset

    :Parameters:
      - `classifier` - a classifier template
      - `data` - a dataset
      - `numFolds` - number of cross validation folds (default = 5)
      
    :Returns:
      a Results object.

    :Keywords:
      - `numFolds` - number of cross-validation folds -- overrides the numFolds parameter
      - `seed` - random number generator seed
      - `trainingAllFolds` - a list of patterns that are to be used as training
        examples in all CV folds.
      - `intermediateFile` - a file name to save intermediate results under
        if this argument is not given, not intermediate results are saved
      - `foldsToPerform` - number of folds to actually perform (in case you're doing
        n fold CV, and want to save time, and only do some of the folds)
    """

    if 'numFolds' in args :
        numFolds = args['numFolds']
    if 'seed' in args :
        random.seed(args['seed'])
    if 'trainingAllFolds' in args :
        trainingAllFolds = args['trainingAllFolds']
    else :
        trainingAllFolds = []
    foldsToPerform = numFolds
    if 'foldsToPerform' in args :
        foldsToPerform = args['foldsToPerform']
    if foldsToPerform > numFolds :
        raise ValueError, 'foldsToPerform > numFolds'

    trainingAllFoldsDict = misc.list2dict(trainingAllFolds)

    labels = data.labels
    p = [[] for i in range(labels.numClasses)] 
    classFoldSize = [int(labels.classSize[k] / numFolds) for k in range(labels.numClasses)]

    for i in range(len(data)):
        if i not in trainingAllFoldsDict :
            p[labels.Y[i]].append(i)
    for k in range(labels.numClasses):
        random.shuffle(p[k])

    trainingPatterns = [[] for i in range(foldsToPerform)]
    testingPatterns = [[] for i in range(foldsToPerform)]
    for fold in range(foldsToPerform) :
        for k in range(labels.numClasses) :
            classFoldStart = classFoldSize[k] * fold
            if fold < numFolds-1:
                classFoldEnd = classFoldSize[k] * (fold + 1)
            else:
                classFoldEnd = labels.classSize[k]
            testingPatterns[fold].extend(p[k][classFoldStart:classFoldEnd])
            if fold > 0:
                trainingPatterns[fold].extend(p[k][0:classFoldStart] +
                                              p[k][classFoldEnd:labels.classSize[k]])
            else:
                trainingPatterns[fold].extend(p[k][classFoldEnd:labels.classSize[k]])

    if len(trainingPatterns) > 0 :
        for fold in range(len(trainingPatterns)) :
            trainingPatterns[fold].extend(trainingAllFolds)
        
    #return cvFromFolds(classifier, data, trainingPatterns, testingPatterns, **args)
    return trainingPatterns, testingPatterns

def findBestCForLamda(origKData,trainIDs):
	cVals=[0.1,1,10,100,1000] 
	cResults={}
	for val in cVals:
		s=PyML.SVM(C=val)
                trainingData = origKData.__class__(origKData, deepcopy = s.deepcopy,patterns = trainIDs)
                r=s.stratifiedCV(trainingData,numFolds=10) 
		cResults[val]=r.getROC()
	bestC=[key for key,val in cResults.iteritems() if val == max(cResults.values())][0]
	maxROC=max(cResults.values())
	return bestC,maxROC 
def findBestLamdaForTrainingSet(train,test,origLabelFileName,kmLoc):
	results={}
	cVals=[0.1,1,10,100,1000]
	for lamda in range(1,10):	
		origkm=PyML.KernelData(kmLoc+'km_cfg_dd_together_1_10_lamda_0.'+str(lamda)+'_paramk_0.5')
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

def findBestLamdaAndkForTrainingSet(train,test,origLabelFileName,kmLoc):
        results={}
        cVals=[0.1,1,10,100,1000]
        for lamda in range(1,10):
		for k in range(3,6):
                	origkm=PyML.KernelData(kmLoc+'kmAdd_rwk_cfg_lamda_0.'+str(lamda)+'graphlet_k_'+str(k))
                	#no need to normalize since these matrices are already normalized
			#origkm.attachKernel(normalization = 'cosine')
                	labels=PyML.Labels(origLabelFileName)
                	origkm.attachLabels(labels)
                	"""
                	s=PyML.SVM(C=10)
                	trainingData = origkm.__class__(origkm, deepcopy = s.deepcopy,patterns = train)
                	r=s.stratifiedCV(trainingData,numFolds=10)
                	"""
                	bestCForLamda,maxROC=findBestCForLamda(origkm,train)
                	results[lamda,k,bestCForLamda]=maxROC
                	#print results
        maxlamdakAndC=[key for key,val in results.iteritems() if val == max(results.values())][0]
        return  maxlamdakAndC

def findBestGraphletSizeForTrainingSet(train,test,origLabelFileName,kmLoc):
        results={}
        cVals=[0.1,1,10,100,1000]
        for lamda in range(3,6):
                origkm=PyML.KernelData(kmLoc+'mod_graphlet_km_size_'+str(lamda))
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
		
def conductNestedCVForLamda(seed):
	origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/excClassLabelFinal1_comma'
        kmLoc='/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/combined/usingBothcfgAnndDDEdgesTogether/'
	labels=PyML.Labels(origLabelFileName)
        kdata=PyML.KernelData(kmLoc+'km_cfg_dd_together_1_10_lamda_0.1_paramk_0.5')
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        train,test=createStratifiedTestTrainFolds(s,kdata,numFolds=10,seed=seed)
        #print 'train'
        #print train
        #print 'test'
        #print test
	results=[]
	maxLamdaVals={}
	BSRVals=[]
	AUCVals=[]
        origLabels=open(origLabelFileName,'r').readlines()
	for i in range(10):
		maxLamdaAndC=findBestLamdaForTrainingSet(train[i],test[i],origLabelFileName,kmLoc)
		maxLamdaVals[i]= maxLamdaAndC
		maxLamdakdata=PyML.KernelData(kmLoc+'km_cfg_dd_together_1_10_lamda_0.'+str(maxLamdaAndC[0])+'_paramk_0.5')
		maxLamdakdata.attachKernel(normalization = 'cosine')
		maxLamdakdata.attachLabels(labels)
		newS=PyML.SVM(C=maxLamdaAndC[1])
		r=newS.trainTest(maxLamdakdata,train[i],test[i])
		BSRVals.append(r.getBalancedSuccessRate())
		AUCVals.append(r.getROC())
		results.append(r)
	#print results
	print maxLamdaVals
	print np.mean(BSRVals)
	print np.mean(AUCVals)
	return maxLamdaVals,np.mean(BSRVals),np.mean(AUCVals),results

def conductNestedCVForGraphletSize(seed):
        origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/excClassLabelFinal1_comma'
        kmLoc='/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/'
        labels=PyML.Labels(origLabelFileName)
        kdata=PyML.KernelData(kmLoc+'mod_graphlet_km_size_3')
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        train,test=createStratifiedTestTrainFolds(s,kdata,numFolds=10,seed=seed)
        #print 'train'
        #print train
        #print 'test'
        #print test
        results=[]
        maxLamdaVals={}
        BSRVals=[]
        AUCVals=[]
        origLabels=open(origLabelFileName,'r').readlines()
        for i in range(10):
                maxLamdaAndC=findBestGraphletSizeForTrainingSet(train[i],test[i],origLabelFileName,kmLoc)
                maxLamdaVals[i]= maxLamdaAndC
                maxLamdakdata=PyML.KernelData(kmLoc+'mod_graphlet_km_size_'+str(maxLamdaAndC[0]))
                maxLamdakdata.attachKernel(normalization = 'cosine')
                maxLamdakdata.attachLabels(labels)
                newS=PyML.SVM(C=maxLamdaAndC[1])
                r=newS.trainTest(maxLamdakdata,train[i],test[i])
                BSRVals.append(r.getBalancedSuccessRate())
                AUCVals.append(r.getROC())
                results.append(r)
        #print results
        print maxLamdaVals
        print np.mean(BSRVals)
        print np.mean(AUCVals)
        return maxLamdaVals,np.mean(BSRVals),np.mean(AUCVals)

#This should be used when selecting C with any kernel matrix (used for initial evaluation of the two kernels)
def conductNestedCVForC(seed):
        origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/perClassLabelFinal1_comma'
        km='/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_3_4_5'
        labels=PyML.Labels(origLabelFileName)
        kdata=PyML.KernelData(km)
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        train,test=createStratifiedTestTrainFolds(s,kdata,numFolds=10,seed=seed)
        #print 'train'
        #print train
        #print 'test'
        #print test
        results=[]
        maxCVals={}
        BSRVals=[]
        AUCVals=[]
        origLabels=open(origLabelFileName,'r').readlines()
        for i in range(10):
                maxCAndROC=findBestCForLamda(kdata,train[i])
		maxCVals[i]= maxCAndROC[0]
                newS=PyML.SVM(C=maxCAndROC[0])
                r=newS.trainTest(kdata,train[i],test[i])
                BSRVals.append(r.getBalancedSuccessRate())
                AUCVals.append(r.getROC())
                results.append(r)
        #print results
        print maxCVals
        print np.mean(BSRVals)
        print np.mean(AUCVals)
        return maxCVals,np.mean(BSRVals),np.mean(AUCVals)


def conductNestedCVForAddedKMs(seed):
        origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/mulClassLabelFinal1_comma'
        kmLoc='/s/bach/h/proj/saxs/upuleegk/Soot/addRWKAndGraphlet/'
        labels=PyML.Labels(origLabelFileName)
        kdata=PyML.KernelData(kmLoc+'kmAdd_rwk_cfg_lamda_0.1graphlet_k_3')
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        train,test=createStratifiedTestTrainFolds(s,kdata,numFolds=10,seed=seed)
        #print 'train'
        #print train
        #print 'test'
        #print test
        results=[]
        maxLamdaVals={}
        BSRVals=[]
        AUCVals=[]
	sensVals=[]
	specVals=[]
	confMats=[]
        origLabels=open(origLabelFileName,'r').readlines()
        for i in range(10):
                maxLamdaAndC=findBestLamdaAndkForTrainingSet(train[i],test[i],origLabelFileName,kmLoc)
                maxLamdaVals[i]= maxLamdaAndC
                maxLamdakdata=PyML.KernelData(kmLoc+'kmAdd_rwk_cfg_lamda_0.'+str(maxLamdaAndC[0])+'graphlet_k_'+str(maxLamdaAndC[1]))
                #no need to normalize since these matrces are already normalized
		#maxLamdakdata.attachKernel(normalization = 'cosine')
                maxLamdakdata.attachLabels(labels)
                newS=PyML.SVM(C=maxLamdaAndC[2])
                r=newS.trainTest(maxLamdakdata,train[i],test[i])
                BSRVals.append(r.getBalancedSuccessRate())
                AUCVals.append(r.getROC())
                results.append(r)
		sensVals.append(r.getSensitivity())
		print r.getConfusionMatrix()
		spc=r.getConfusionMatrix()[0][0]/(r.getConfusionMatrix()[0][1]+r.getConfusionMatrix()[0][0])
		specVals.append(spc)
        #print results
        print maxLamdaVals
        print np.mean(BSRVals)
        print np.mean(AUCVals)
        return maxLamdaVals,np.mean(BSRVals),np.mean(AUCVals),np.mean(sensVals),np.mean(specVals)





#conductNestedCV()
iterations=10
myseed=1
finalLamdaCVals=[]
finalBSRs=[]
finalAUCs=[]
finalSens=[]
finalSpec=[]
finalr=[]	
for i in range(iterations):
	lamdaCVals,bsr,auc,r=conductNestedCVForLamda(myseed+i)
	#lamdaCVals,bsr,auc=conductNestedCVForGraphletSize(myseed+i)
	#lamdaCVals,bsr,auc,sens,spec=conductNestedCVForAddedKMs(myseed+i)
	#lamdaCVals,bsr,auc=conductNestedCVForC(myseed+i)
	finalLamdaCVals.append(lamdaCVals)
	finalBSRs.append(bsr)
	finalAUCs.append(auc)
	finalr.append(r)
	#finalSens.append(sens)
	#finalSpec.append(spec)
print finalLamdaCVals
print finalBSRs
print finalAUCs
print np.mean(finalBSRs)
print np.mean(finalAUCs)
#print np.mean(finalSens)
#print np.mean(finalSpec)
print finalr 

f=open('excPreds','w')
for r in finalr:
	#print r
	for ri in r:
		print ri	
		patIDs= PyML.evaluators.resultsObjects.ClassificationResults.getPatternID(ri) 
        	pred= PyML.evaluators.resultsObjects.ClassificationResults.getPredictedLabels(ri)

		print patIDs
		f.write(str(patIDs))
		print pred
		f.write(str(pred))
		#for i in range(0,len(patIDs)):
        	#        for j in range(0,len(list(patIDs[i]))):
                #        	print list(patIDs[i])[j]+':'+list(pred[i])[j]
	
