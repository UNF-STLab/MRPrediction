import numpy as np
import math
import os
import PyML
import itertools

def readKMFromFile(fileName):
	f = open(fileName, 'r')
	km=np.zeros((100,100))
	linecnt=0
	ids=[]
	for line in f:
		fields=line.split(',')
		print str(fields[0])
		ids.append(str(fields[0]))
		for i in range(1,len(fields)):
			km[linecnt][i-1]=float(fields[i])
		linecnt+=1
	f.close()
	return km,ids

def cosineNormKM(km):
	kmNorm=np.zeros((100,100))
	for i in range(km.shape[0]):
		for j in range(km.shape[1]):
			kmNorm[i][j]= km[i][j]/math.sqrt(km[i][i]*km[j][j])   
			
	return  kmNorm

def computeResults(km,ids,labelFile):
        wstr=''         
        filename='tmpkmfile'
	labels=PyML.Labels(labelFile)
        f=open(filename,'w')    
        for i in range(km.shape[0]):
                wstr=ids[i] 
                for j in range(km.shape[1]):
                        wstr+=','+str(km[i][j])      
                wstr+='\n'        
                f.write(wstr)
        f.close()
        kdata=PyML.KernelData(filename)
        kdata.attachLabels(labels)
        s=PyML.SVM(C=10)
        r=s.nCV(kdata,numFolds=10)
        return r
        #os.remove(tmpkmfile)

def createParmCombKM(km1,km2,km3,km4,ids,labels):
	#mu=[0,0.5,1]
	results={}
	mu=[0,0.5,1,2]
	paraCombs=itertools.combinations_with_replacement(mu,4)
	for i in paraCombs:
		print i
		combKM=np.add(np.add(np.multiply(i[0],km1),np.multiply(i[1],km2)),np.add(np.multiply(i[2],km3),np.multiply(i[3],km4)))
		r=computeResults(combKM,ids,labels)		 
		results[i[0],i[1],i[2],i[3]]=r
	print results

def addTwoKMs(km1,km2,ids,labels):
	combKM=np.add(km1,km2)
	r1=computeResults(km1,ids,labels)
	r2=computeResults(km2,ids,labels)
	r=computeResults(combKM,ids,labels)
	
	print r1
	print r2
	print r

def writeKMToFile(km,ids,fileName):
	f=open(fileName,'w')
	for i in range(len(ids)):
		wstr=str(ids[i])
		for num in km[i]:
			wstr+=','+str(num)
		wstr+='\n'
		f.write(wstr)
	f.close()


def addAndSaveKMs():
	for lamda in range(1,10):
		for k in range(3,6):
			km1,ids1=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.'+str(lamda))
			km1=cosineNormKM(km1)
			km2,ids2=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_'+str(k))
			km2=cosineNormKM(km2)
			addedKM=np.add(km1,km2)
			normAddedKM=cosineNormKM(addedKM)
			fileName='/s/bach/h/proj/saxs/upuleegk/Soot/addRWKAndGraphlet/kmAdd_rwk_cfg_lamda_0.'+str(lamda)+'graphlet_k_'+str(k)
			writeKMToFile(normAddedKM,ids1,fileName)

#addAndSaveKMs()
def addAndSaveThreeKMs():
	
	km1,ids1=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_3')
	km1=cosineNormKM(km1)
	km2,ids2=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_4')
	km2=cosineNormKM(km2)
	km3,ids3=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_5')
	km3=cosineNormKM(km3)
	addedKM1=np.add(km1,km2)
	addedKM1=cosineNormKM(addedKM1)
	addedKM2=np.add(addedKM1,km3)
	addedKM2=cosineNormKM(addedKM2)
	fileName='/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_3_4_5'
	writeKMToFile(addedKM2,ids1,fileName)

addAndSaveThreeKMs()
"""
km1,ids1=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.5')
km1=cosineNormKM(km1)
#print km1[0][1]
km2,ids2=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/mod_graphlet_km_size_5')
km2=cosineNormKM(km2)
#print km2[0][1]
km3,ids3=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/kmAfterRemovingMultiEdgesFromDDs/km_rw_dd_10_lamda_0.4_paramk_0.5')
km3=cosineNormKM(km3)
km4,ids4=readKMFromFile('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/DDKMs/dd_graphlet_km_size_4')
km4=cosineNormKM(km4)
#createParmCombKM(km1,km2,km3,km4,ids1,'/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/mulClassLabelFinal1_comma')
addTwoKMs(km1,km2,ids1,'/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/perClassLabelFinal1_comma')
"""
