import PyML
import numpy as np


def evaluateWithCV():
	labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/perClassLabelFinal1_comma')
	results={}
	for i in range(1,10):
		kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/kmsForExatLabelEquality/km_rw_cfg_10_lamda_0.'+str(i)+'_paramk_0')
		#kdata.attachKernel(normalization = 'cosine')
		#kdata.attachKernel(normalization = 'tanimoto')
		#kdata.attachKernel(normalization ='dices')
		kdata.attachLabels(labels)
		#param=PyML.classifiers.modelSelection.Param(PyML.classifiers.svm.SVM(),'C',[0.1,1,10,100,1000])
		#m=PyML.classifiers.modelSelection.ModelSelector(param,numFolds=6)
		#r=m.train(kdata)
		#r=m.train(kdata,numFolds=6)
		#print r.getBalancedSuccessRate()


		s=PyML.SVM(C=10)
		r=s.nCV(kdata,numFolds=10)
		results[i]=r

	for i in results:
		print i
		print results[i]
		#print 'Sensitivity:'+str(results[i].getSensitivity())
                #print 'PPV:'+str(results[i].getPPV())
		print '===========' 

#evaluateWithCV()

def evaluateWithCVForOneLamda():
	#mrs=['per','add','mul','inv','inc','exc']
	mrs=['per']
	results={}
	for mr in mrs:
		print mr
		print "======="
        	labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/'+mr+'ClassLabelFinal1_comma')
		kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/kmAfterRemovingMultiEdgesFromDDs/km_graphlet_k_3')
        	kdata.attachKernel(normalization = 'cosine')
		#print kdata.getKernelMatrix()
		kdata.attachLabels(labels)
		#kdata.attachKernel('gaussian',gamma=0.01)
		s=PyML.SVM(C=10)
        	r=s.nCV(kdata,numFolds=10)
		print r[0].getConfusionMatrix()
		print r
		results[mr]=r
	for i in results:
		print i
		print results[i]
evaluateWithCVForOneLamda()

def selectSVMParamC():
	labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/invClassLabelFinal1_comma')
        kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.1')
	kdata.attachLabels(labels)
	param =PyML.modelSelection.Param(PyML.SVM(), 'C', [0.1, 1, 10, 100, 1000])
	m =PyML.modelSelection.ModelSelector(param)
	m.train(kdata)
	print m
#selectSVMParamC()

def combineTwoKMs():
	labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/addClassLabelFinal1_comma')
	print len(labels)	
        kdata_cfg=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.8')
	#print kdata_cfg.getKernelMatrix() 
	kdata_cfg.attachKernel(normalization = 'cosine')
	#kdata_cfg.attachLabels(labels)
	#kdata_cfg.normalize(1)
	#s=PyML.SVM(C=10)
        #r1=s.nCV(kdata_cfg,numFolds=10)
	km_cfg=kdata_cfg.getKernelMatrix()
	print km_cfg
	#data_dd=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_3')
	
        kdata_dd=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/kmAfterRemovingMultiEdgesFromDDs/km_rw_dd_10_lamda_0.9_paramk_0.5')
	kdata_dd.attachKernel(normalization = 'cosine')
	#kdata_dd.attachLabels(labels)
	#s=PyML.SVM(C=10)
        #r2=s.nCV(kdata_dd,numFolds=10)
	km_dd= kdata_dd.getKernelMatrix()
	print km_dd
	km=np.add(km_cfg,km_dd)
	print km.shape
	#print r1
	#print r2
	np.savetxt('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/combined/combined_km_cfg_rw_lamda_0.8_dd_rw_0.9',km,delimiter=',')
	#print len(km)
	print km
	
	"""	
        kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/combined/combined_km_cfg_0.5_dd_0.4')
	#kdata_cfg.attachKernel(normalization = 'cosine')
	kdata.attachLabels(labels)
        kdata.attachKernel('polynomial',degree=3)
        #kdata.attachKernel('gaussian',gamma=10)
	s=PyML.SVM(C=10)
        r=s.nCV(kdata,numFolds=10)
        print r
	"""
#combineTwoKMs()
def getIncorrectPredictedProgsForBestLamda(classLabelFile,kmFileOfBestLamda):
	labels=PyML.Labels(classLabelFile)
	kdata=PyML.KernelData(kmFileOfBestLamda)
	kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        r=s.nCV(kdata,numFolds=10)
	
	incorrectEx=set()
	for i in r:
		print i
		print 'Sensitivity:'+str(i.getSensitivity())  
		print 'PPV:'+str(i.getPPV())
		for j in range(0,10):
			patternIDs=i.getPatternID(j)
			givenLabels=i.getGivenLabels(j)
			predictedLabels=i.getPredictedLabels(j)
			for k in range(0,len(patternIDs)):
				if givenLabels[k]!=predictedLabels[k]:
					incorrectEx.add(patternIDs[k])
					#print str(patternIDs[k])+':'+str(givenLabels[k])+':'+str(predictedLabels[k]) 
		
	return incorrectEx	 
	#print len(incorrectEx)

#getIncorrectPredictedProgsForBestLamda('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/addClassLabelFinal1_comma','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingAssandIfLabelsTo0.5/CFGKMs/mod_km_cfg_1_10_0.4')

def calcLabelBasedMeasures():
	mrs=['per','add','mul','inv','inc','exc']
	cfgkms=[0.5,0.8,0.4,0.1,0.9,0.7]
	sumPrec=0
	sumRecall=0
	f1=0
	sumtp=0
	sumfp=0
	sumfn=0
	for k in range(len(mrs)):
		labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/'+mrs[k]+'ClassLabelFinal1_comma')
        	kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingAssandIfLabelsTo0.5/CFGKMs/mod_km_cfg_1_10_'+str(cfgkms[k]))
        	kdata.attachLabels(labels)
        	s=PyML.SVM(C=10)
        	r=s.stratifiedCV(kdata,numFolds=10)
		confMat=r.getConfusionMatrix()
		tp=confMat[1][1]
		sumtp+=tp
		#print tp
		fp=confMat[0][1]
		sumfp+=fp	
		fn=confMat[1][0]
		sumfn+=fn	
		prec=float(tp)/(tp+fp)
		recall=float(tp)/(tp+fn)
		f1+=(2*prec*recall)/(prec+recall)
		#print prec
		sumPrec+=prec
		sumRecall+=recall
		#for i in range(0,10): 
			#print r.getConfusionMatrix(i)
		#patternIDs=i.getPatternID(j)
                #givenLabels=i.getGivenLabels(j)
		#predictedLabels=i.getPredictedLabels(j)
	macroPrec=sumPrec/6
	macroRecall=sumRecall/6
	macroF1=f1/6
	microPrec=float(sumtp)/(sumtp+sumfp)
	microRecall=float(sumtp)/(sumtp+sumfn)
	microF1=(2*microPrec*microRecall)/(microPrec+microRecall)
	print 'macroPrec: '+str(macroPrec)
	print 'macroRecall: '+str(macroRecall)
	print 'macroF1: '+str(macroF1)
	print 'microPrec: '+str(microPrec)
	print 'microRecall: '+str(microRecall)
	print 'microF1: '+str(microF1)

#calcLabelBasedMeasures()

"""
cfgSet=getIncorrectPredictedProgsForBestLamda('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/invClassLabelFinal1_comma','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/add_new/CFGKMs/mod_km_1_10_0.5')
ddSet=getIncorrectPredictedProgsForBestLamda('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/addClassLabelFinal1_comma','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/add_new/DDKMs/mod_km_dd_1_10_0.9')
print cfgSet
print ddSet
print 'Intersection'
print cfgSet.intersection(ddSet)
print 'Difference'
print cfgSet.difference(ddSet)
"""

def modelSelect():

	labels=PyML.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/per/per_class_label_comma')
        results={}
        for i in range(1,10):
                kdata=PyML.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/per/mod_km_per_1_10_0.'+str(i))
                kdata.attachLabels(labels)
                break
		param=PyML.classifiers.modelSelection.Param(PyML.classifiers.svm.SVM(),'C',[0.1,1,10,100,1000])
                m=PyML.classifiers.modelSelection.ModelSelector(param,numFolds=6)
                r=m.train(kdata,numFolds=6)
               	r=m.nCV(kdata,numFolds=6) 
                results[i]=r
		
	for i in results:
                print i
                print results[i]
                print '==========='

#modelSelect()

def imkcode():
	kdata=pyml.KernelData('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/per/mod_km_per_1_10_0.1')
        print len(kdata)
        #cc.saveLabels("./labels.dat")
        labels=pyml.Labels('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/per/per_class_label_comma')
        print len(labels)
        kdata.attachLabels(labels)

        #sd = cc.makeSparseDataSet(feats,vals)

        #PyML code
        s=pyml.SVM(C=10)
        r=s.nCV(kdata,numFolds=2)
        print r

imkcode
