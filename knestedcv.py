import numpy as np 
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, train_test_split
import glob
import os
import sys
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.cross_validation import cross_val_predict


def readlabel(files):
	labels = []
	with open('/home/rahman/Documents/MRPred1/add/'+files, 'r') as f:
		first_line = f.readline()
		while first_line:
			first_line = first_line.strip('\n')
			labels.append(first_line)
			first_line = f.readline()
			
	return labels
#a=readlabel()


def readfile(files):
	f = open('/home/rahman/Documents/MRPred1/outputf/'+files, 'r')
	km=np.zeros((62,21))
	linecnt=0
	ids=[]
	for line in f:
		fields=line.split(',')
		#print str(fields[0])
		ids.append(str(fields[0]))
		for i in range(1,21):
			km[linecnt][i-1]=float(fields[i])
		linecnt+=1
	f.close()
	#print km
	#print ids
	return km


	



def labeldatasplit(a1,a2):
	labels = a1
	labels = map(int, labels)
	data=a2
	testdata,restdata,testlabel,restlabel=train_test_split(data,labels,train_size=0.33,stratify=labels)
	traindata,valdata,trainlabel,vallabel=train_test_split(restdata,restlabel,train_size=0.50,stratify=restlabel)
	#label1,rest=train_test_split(labels,train_size=0.33,stratify=labels)
	#label2,label3=train_test_split(rest,train_size=0.50,stratify=rest)
	#print trainlabel
	#print vallabel
	#print testlabel
	return testdata,testlabel,traindata,trainlabel,valdata,vallabel
#b,c,d=datasplit(a)




def pred(testdata,testlabel,traindata,trainlabel,valdata,vallabel):

    clf = svm.SVC(kernel='precomputed')
    print train data

    print trainlabel
    
    clf.fit(traindata,trainlabel)
   
    outputpred=clf.predict(valdata)
    print outputpred
	#print (clf.score(traindata,trainlabel))
	#print (cross_val_score(estimator=clf, X=valdata, y=vallabel, cv=6))
	#score=cross_val_predict(estimator=clf, X=valdata, y=vallabel, cv=6)
	#print score
    a=roc_auc_score(vallabel,outputpred)
    print a
    print (confusion_matrix(vallabel,outputpred))
    return a
#pred(c,d)

def select():
	path = '/home/rahman/Documents/MRPred1/add/'
	dirs = os.listdir(path)
	score=[]
	for files in dirs:
		labels=readlabel(files)
		data=readfile(files)
		#print labels
		#print data
		testdata,testlabel,traindata,trainlabel,valdata,vallabel=labeldatasplit(labels,data)
		#print testdata
		#print traindata
		#print valdata
		#print testlabel
		#print trainlabel
		#print vallabel
		score.append(str(pred(testdata,testlabel,traindata,trainlabel,valdata,vallabel))+':'+files)
	print score
	maxval=max(score)
	print maxval
	fields=maxval.split(':')
	f=fields[1]
	print f
	
	
	
select()
	 
