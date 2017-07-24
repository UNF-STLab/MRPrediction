import PyML
from PyML.utils import misc
import random
import numpy as np

def trainTest():
	origLabelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/perTrainingAndMutatedSAXSFunClassLabels'
        kmLoc='/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/kmsWithMutSAXSFuns/'
        labels=PyML.Labels(origLabelFileName)
        print labels
	kdata=PyML.KernelData(kmLoc+'rwk_km_cfg_1_10_0.2')
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        train=list(xrange(100))
	print train
	test=list(xrange(100,314))
	print test
	r=s.trainTest(kdata, train, test)
	print r
	progNames= r.getPatternID()
	preds=r.getPredictedLabels()
	for i in range(len(progNames)):
		print progNames[i]+":" +preds[i]

	"""
	,test=createStratifiedTestTrainFolds(s,kdata,numFolds=10,seed=seed)
        #print 'train'
        #print train
        #print 'test'
        #print test
        results=[]
        maxLamdaVals={}
        BSRVals=[]
        AUCVals=[]
        origLabels=open(origLabelFileName,'r').readlines()
	"""

trainTest()
