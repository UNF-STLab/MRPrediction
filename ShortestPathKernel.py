import networkx as nx
import SootUtilities as su
import itertools
import sys
import os
import glob

def createShortestPathGraph(g):
	shortestPaths=nx.all_pairs_shortest_path(g)
	
	#for i in shortestPaths:
	#	print shortestPaths[i] 

	spg=nx.DiGraph()
	spg.nodes=g.nodes
	
	for n1 in shortestPaths:
		for n2 in shortestPaths[n1]:
			if n1!=n2:
				spg.add_edge(n1,n2,weight=shortestPaths[n1][n2])

	#print spg.edges()
	return spg
	"""
	sPaths=nx.get_edge_attributes(spg,'weight')
	for e in spg.edges():
		print e 
		if e in sPaths:
			print sPaths[e]	
	"""
#createShortestPathGraph(cfg) 

def computeKShortestPaths(spg1,spg2,spg1NodeLabels,spg2NodeLabels):
	
	spg1ShortestPaths=nx.get_edge_attributes(spg1,'weight')
	spg2ShortestPaths=nx.get_edge_attributes(spg2,'weight')
	kShortestPath=0
	for e1 in spg1.edges():
		for e2 in spg2.edges():
			if len(spg1ShortestPaths[e1])==len(spg2ShortestPaths[e2]):
				kShortestPath+=computeKWalk(spg1ShortestPaths[e1],spg2ShortestPaths[e2],spg1NodeLabels,spg2NodeLabels)
	return kShortestPath

def computeKWalk(sp1,sp2,spg1NodeLabels,spg2NodeLabels):
	kWalk=1
	for i in range(len(sp1)-1):
		kWalk=kWalk*computeKStep(sp1[i],sp1[i+1],sp2[i],sp2[i+1],spg1NodeLabels,spg2NodeLabels)
	return kWalk

def computeKStep(v1,v2,w1,w2,spg1NodeLabels,spg2NodeLabels):
	kStep=get_similarity(spg1NodeLabels[v1],spg2NodeLabels[w1])*get_similarity(spg1NodeLabels[v2],spg2NodeLabels[w2])
	return kStep
		
def get_similarity(l1,l2):

        if(l1==l2):
                return 1
        elif(su.get_group(l1)==su.get_group(l2)):
                return 0.5
        else:
                return 0

def createShortestPathKernelMatrix(class_file_name,km_file_name):
	class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()

	dotFileLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/idenAndgotoRemovedDotFiles'
	computedValsDict={}
        f=open(km_file_name,'w')
        for i in range(0,len(dot_file_names)):
                temp_str=str(dot_file_names[i])
                for j in range(0,len(dot_file_names)):
                        print dot_file_names[i]
                        sys.stdout.flush()
                        print dot_file_names[j]
                        sys.stdout.flush()
                        if computedValsDict.has_key(str(i)+'.'+str(j)):
                                print 'Found val'
                                sys.stdout.flush()
                                val=computedValsDict[str(i)+'.'+str(j)]
                        elif computedValsDict.has_key(str(j)+'.'+str(i)):
                                print 'Found val'
                                sys.stdout.flush()
                                val=computedValsDict[str(j)+'.'+str(i)]
                        else:
                                print 'Computing  val...'
                                sys.stdout.flush()
                                
                                dd1,cfg1=su.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[i]+'.dot')
				spg1=createShortestPathGraph(cfg1)
                                spg1NLabels=su.get_node_labels(cfg1)
                                dd2,cfg2=su.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[j]+'.dot')
                                spg2=createShortestPathGraph(cfg2)
				spg2NLabels=su.get_node_labels(cfg2)
                                val=computeKShortestPaths(spg1,spg2,spg1NLabels,spg2NLabels)
				computedValsDict[str(i)+'.'+str(j)]=val
                        temp_str+=','+str(val)
                temp_str+='\n'
                f.write(temp_str)
        f.close()
        os.system("mailx -s \"File writing finished\" < /dev/null \"upuleegk@gmail.com\"")

createShortestPathKernelMatrix(sys.argv[1],sys.argv[2])

"""
dd1,cfg1=su.get_dd_cd_subgraphs('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/winsorizedMean.dot')
spg1=createShortestPathGraph(cfg1)
spg1NLabels=su.get_node_labels(cfg1)
dd2,cfg2=su.get_dd_cd_subgraphs('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/weightedRMS.dot')
spg2=createShortestPathGraph(cfg2)
spg2NLabels=su.get_node_labels(cfg2)
print computeKShortestPaths(spg1,spg2,spg1NLabels,spg2NLabels)
"""
