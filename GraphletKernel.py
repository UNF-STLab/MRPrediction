import networkx as nx
import itertools
import SootUtilities as sutil
import sys
import os

def getSubgraphs(g,size):
	nodes=g.nodes()
	labels=sutil.get_node_labels(g) 
	combs=itertools.combinations(nodes,size)
	connectedSubgs=[]
	subgs={}
	for i in combs:
		subg=g.subgraph(i)
		if nx.is_weakly_connected(subg):
			connectedSubgs.append(subg)   
	print len(connectedSubgs)
	for i in connectedSubgs:
		#print i
		cnt=1	
		for j in connectedSubgs:
			#print j
			if i!=j:
				DiGM = nx.isomorphism.DiGraphMatcher(i,j)
                		if DiGM.is_isomorphic():
                        		nodeMap=DiGM.mapping
					if nodeLabelExactMatch(nodeMap,labels)==True:
						"""
						print 'iso found'
						print i.nodes()
						print j.nodes()
						print nodeMap
						"""
						cnt+=1
						connectedSubgs.remove(j)
                subgs[i]=float(cnt)/float(len(connectedSubgs))
			#if i in connectedSubgs:
			#	connectedSubgs.remove(i)	 
	return subgs

def nodeLabelExactMatch(nodeMap,labels):
	check=True
	for i in nodeMap:
		if labels[i]!=labels[nodeMap[i]]:
			check=False
	return check

#calculates the k_graph(G,G') for two graphs 
def calcGraphletKernelVal(g1Graphlets,g1NodeLabels,g2Graphlets,g2NodeLabels):
	k_graph=0
	for i in g1Graphlets:
		for j in g2Graphlets:
			#print i.nodes()
			#print j.nodes()
			k_graph+=calcSubgraphKernelVal(i,g1NodeLabels,j,g2NodeLabels)*g1Graphlets[i]*g2Graphlets[j]
	return k_graph			 

#calculate the kernel value k_subgraph(subg1,subg2) for two subgraphs 
def calcSubgraphKernelVal(subg1,subg1NodeLabels,subg2,subg2NodeLabels):
	DiGM = nx.isomorphism.DiGraphMatcher(subg1,subg2)
	if DiGM.is_isomorphic():
		#print 'isomorphic'
		nodeMap=DiGM.mapping
		k_subgraph=1
		for n in nodeMap:
			#k_subgraph=k_subgraph*getNodeKernelVal(subg1NodeLabels[n],subg2NodeLabels[nodeMap[n]])
			 k_subgraph=k_subgraph*getNodeKernelValExactEqual(subg1NodeLabels[n],subg2NodeLabels[nodeMap[n]])
	else:
		k_subgraph=0
	return k_subgraph

def getNodeKernelValExactEqual(l1,l2):
	if(l1==l2):
                return 1
	else:
                return 0

def getNodeKernelVal(l1,l2):

        if(l1==l2):
                return 1
        elif(sutil.get_group(l1)==sutil.get_group(l2)):
                return 0.5
        else:
                return 0.001


def create_graphlet_kernel_matrix(class_file_name,km_file_name,graphletSize):
        class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()

        dotFileLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles'
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
                                #g1=nx.read_dot(dotFileLoc+'/'+dot_file_names[i]+'.dot')
                                dd1,g1=sutil.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[i]+'.dot')
				#g1=sutil.removeMultiGraphEdgesFromDD(dd1)
				dd2,g2=sutil.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[j]+'.dot')
				#g2=sutil.removeMultiGraphEdgesFromDD(dd2)
                                g1NodeLabels=sutil.get_node_labels(g1)
				g1Graphlets=getSubgraphs(g1,graphletSize)
				g2NodeLabels=sutil.get_node_labels(g2)
                                g2Graphlets=getSubgraphs(g2,graphletSize)
				#a=create_modified_DPG(g1,g2)
                                val=calcGraphletKernelVal(g1Graphlets,g1NodeLabels,g2Graphlets,g2NodeLabels)
                                computedValsDict[str(i)+'.'+str(j)]=val
                        temp_str+=','+str(val)
                temp_str+='\n'
                f.write(temp_str)
        f.close()
        os.system("mailx -s \"File writing finished\" < /dev/null \"upuleegk@gmail.com\"")
create_graphlet_kernel_matrix(sys.argv[1],sys.argv[2],int(sys.argv[3]))
