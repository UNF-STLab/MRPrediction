import networkx as nx
import nx_pydot as pydot
import sys
import os
import glob
import itertools

def getOp(myName):

        if(myName.find('=')==-1):
                print myName
		return 'ERROR'
        else:
                #parts=myName.split('=')
                if(myName.find('&')!=-1):
                        return 'AND'
                elif(myName.find('cmpg')!=-1):
                        return 'CMPG'
                elif(myName.find('cmpl')!=-1):
                        return 'CMPL'
                elif(myName.find('cmp')!=-1):
                        return 'CMP'
		if(myName.find('+')!=-1):
                        return 'ADD'
                elif(myName.find('-')!=-1):
                        return 'SUB'
		elif(myName.find('/')!=-1):
                        return 'DIV'
                elif(myName.find('==')!=-1):
                        return 'EQL'
                elif(myName.find('>=')!=-1):
                        return 'GEQL'
                elif(myName.find('>')!=-1):
                        return 'GT'
                elif(myName.find('<=')!=-1):
                        return 'LEQL'
                elif(myName.find('<')!=-1):
                        return 'LT'
                elif(myName.find('*')!=-1):
                        return 'MUL'
                elif(myName.find('!=')!=-1):
                        return 'NEQL'
                elif(myName.find('|')!=-1):
                        return 'OR'
                elif(myName.find('%')!=-1):
                        return 'REM'
                elif(myName.find('<<')!=-1):
                        return 'SHL'
                elif(myName.find('>>')!=-1):
                        return 'SHR'
		elif(myName.find('xor')!=-1):
                        return 'XOR'
                else:
                        #return 'ASSI'
			return getAssiType(myName)
def getAssiType(assiLabel):
		#print assiLabel
		if '=' in assiLabel:
			rhs=assiLabel.split('=')[1]	
			#print rhs
			newLabel=''
			if 'lengthof' in rhs:
				newLabel='ASSI_ARRLEN'
			elif '[' in rhs and ']' in rhs:
				newLabel='ASSI_ARRELE'
			else:
				newLabel='ASSI'

		else:
			newLabel= 'ASSI'
		#print newLabel
		return newLabel	

def getIfType(ifLabel):
	#print ifLabel
	newLabel=''
	if '<=' in ifLabel:
		newLabel='IF_LEQ'
	elif '>=' in ifLabel:
		newLabel='IF_GEQ' 	
	elif '==' in ifLabel:
                newLabel='IF_EQ' 
	elif '!=' in ifLabel:
                newLabel='IF_NEQ'
	elif '<' in ifLabel:
                newLabel='IF_L'
	elif '>' in ifLabel:
                newLabel='IF_G'
	#print newLabel
	return newLabel
		



def get_node_labels(G):
        nodes=G.nodes()
        node_names=nx.get_node_attributes(G,'label')
	uses=nx.get_node_attributes(G,'use')
        defs=nx.get_node_attributes(G,'def')
        #print node_names
        node_labels={}
	useTypes={}
	defTypes={}
        for n in nodes:
                myName=node_names[n]
                if(myName.find('if')!=-1):
			#nodeLabel='IF'
			nodeLabel=getIfType(myName)
		elif(myName.find(':=')!=-1):
                        nodeLabel='IDEN_STMT'
		elif(myName.find('goto')==0 or myName.find('goto')==1 ):
                        nodeLabel='GOTO'
		elif(myName.find('exit')!=-1):
                        nodeLabel='EXIT'
		elif(myName.find('return')!=-1):
                        nodeLabel='RETURN'
		#elif(myName.find('(')!=-1 and myName.find(')')!=-1 and (myName.find('double')!=-1 or myName.find('float')!=-1 or myName.find('int')!=-1)):
                 #       nodeLabel='ASSI'
                elif((myName.find('(')!=-1 and myName.find(')')!=-1) and  (myName.find('staticinvoke')!=-1 or myName.find('virtualinvoke')!=-1)):
                        nodeLabel='FCALL'
                else:
                        nodeLabel=getOp(myName)
		#useTypes[n]=uses[n].strip('\"').strip(',').split(',')
		#defTypes[n]=defs[n].strip('\"').strip(',').split(',')
                node_labels[n]=nodeLabel
        #return node_labels,useTypes,defTypes
	return node_labels
#print get_node_labels(nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/allFileswithOPDatatypes/sumOfLogarithms.dot'))
"""
path='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/'
for infile in glob.glob(os.path.join(path,'*.dot')):
        print infile 
        print get_node_labels(nx.read_dot(infile))	
"""
 
def get_group(l):
	
	if(l=='ADD' or l=='MUL'):
		return 'COMM'
	elif(l=='SUB' or l=='DIV' or l=='REM'):
		return 'N_COMM'
	elif(l=='AND' or l=='OR' or l=='XOR'):
		return 'LOGIC'
	else:
		return l

def createAllPairsOfOps():
	nodeKernelFileName='/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/nodeKernelVals'
	f=open(nodeKernelFileName,'w')
	ops=['IDEN_STMT','GOTO','EXIT','RETURN','FCALL','AND',
		'CMPG','CMPL','CMP','ADD','SUB','DIV','EQL',
                'GEQL','GT','LEQL','LT','MUL','NEQL','OR',
                'REM','SHL','SHR','XOR',
		'ASSI_ARRLEN','ASSI_ARRELE','ASSI',
		'IF_LEQ','IF_GEQ','IF_EQ','IF_NEQ','IF_L','IF_G']
	
	for pair in itertools.product(ops, repeat=2):
    		f.write(pair[0]+','+pair[1]+'\n')
	f.close()	
#createAllPairsOfOps()



def create_comma_class_label_file(in_file_name,comma_file_name):
        class_file=open(in_file_name,'r')
        comma_class_file=open(comma_file_name,'w')
        for line in class_file:
                fields=line.strip('\n').split(':')
                comma_class_file.write(str(fields[0])+','+str(fields[1])+'\n')
        class_file.close()
        comma_class_file.close()

#create_comma_class_label_file('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/excClassLabelFinal1','/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/excClassLabelFinal1_comma')

def createClassLabeFileFromFilesInFolder(folder,classLabelFileName):
	fClass=open(classLabelFileName,'w')
	files=glob.glob(folder+"/*.dot")
	for f in files:
		name=f.split('/')[-1].split('.')[0]
		fClass.write(name+",0\n")
	fClass.close()

#createClassLabeFileFromFilesInFolder("/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/saxsMutatedFunctionsDotFiles","/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/mutatedSAXSFunClassLabels")
def get_dd_cd_subgraphs(fileName):
        pdg=pydot.read_dot(fileName)
        #print pdg
        nodeLabels=nx.get_node_attributes(pdg,'label')
        #print nodeLabels
        #nodeShapes=nx.get_node_attributes(pdg,'shape')
        #nodeFontNames=nx.get_node_attributes(pdg,'fontname')
        #nodeIRLabels=nx.get_node_attributes(pdg,'weight')
        #edgeColor=nx.get_edge_attributes(pdg,'color')
        #print edgeColor
        edgeLabel=nx.get_edge_attributes(pdg,'label')
        #print edgeLabel
        edges=pdg.edges()
        #print edges
        dd_edge_set=set()
        #cd_edge_set=set()
        cfg_edge_set=set()
	"""
        for e in edges:
                if edgeLabel[e]=="\"DD\"":
                        dd_edge_set.add(e)
                elif edgeLabel[e]=="\"cfg\"":
                        cfg_edge_set.add(e)
	"""
	for item in edgeLabel:
		if edgeLabel[item]=="\"DD\"":
			dd_edge_set.add((item[0],item[1])) 
		elif edgeLabel[item]=="\"cfg\"":
			cfg_edge_set.add((item[0],item[1]))
        #print cfg_edge_set
        #print dd_edge_set
        dd_graph=nx.DiGraph()
        #cd_graph=nx.DiGraph()
        cfg_graph=nx.DiGraph()
        for n in pdg.nodes():
                dd_graph.add_node(n)
                #cd_graph.add_node(n)
                cfg_graph.add_node(n)
        nx.set_node_attributes(dd_graph,'label',nodeLabels)
	#nx.set_node_attributes(dd_graph,'shape',nodeShapes)
        #nx.set_node_attributes(dd_graph,'fontname',nodeFontNames)
        #nx.set_node_attributes(dd_graph,'weight',nodeIRLabels)
        #nx.set_node_attributes(cd_graph,'label',nodeLabels)
        #nx.set_node_attributes(cd_graph,'shape',nodeShapes)
        #nx.set_node_attributes(cd_graph,'fontname',nodeFontNames)
        #nx.set_node_attributes(cd_graph,'weight',nodeIRLabels)
        nx.set_node_attributes(cfg_graph,'label',nodeLabels)
        #nx.set_node_attributes(cfg_graph,'shape',nodeShapes)
        #nx.set_node_attributes(cfg_graph,'fontname',nodeFontNames)
        #nx.set_node_attributes(cfg_graph,'weight',nodeIRLabels)
        for e in dd_edge_set:
                dd_graph.add_edge(*e)
        #for e in cd_edge_set:
        #        cd_graph.add_edge(*e)
        for e in cfg_edge_set:
                cfg_graph.add_edge(*e)


        #nx.write_dot(dd_graph,"/s/bach/h/proj/saxs/upuleegk/Soot/originalProgs/CFGDDs/test_DD.dot")
        #nx.write_dot(cd_graph,"/s/bach/h/proj/saxs/upuleegk/CodeSurfer/myWork/add_values/test_CD.dot")
        #nx.write_dot(cfg_graph,"/s/bach/h/proj/saxs/upuleegk/Soot/originalProgs/CFGDDs/test_CFG.dot")
        return dd_graph,cfg_graph

#get_dd_cd_subgraphs('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/allTrainingAndSaxsMutatedFuns/add_values.dot')

def addTwoKMs(cfgkmfile,ddkmfile,newkmfile):
	
	cfgkm=open(cfgkmfile,'r')
	cfgkmlines=cfgkm.readlines()
	ddkm=open(ddkmfile,'r')
        ddkmlines=ddkm.readlines() 
	newfile=open(newkmfile,'w')
	
	for i in range(0,len(cfgkmlines)):
		cfgfields=cfgkmlines[i].split(',')
		ddfields=ddkmlines[i].split(',')
		wstr=cfgfields[0]
		for j in range(1,len(cfgkmlines)):
			r=float(cfgfields[j])+float(ddfields[j])
			wstr+=','+str(r)
		wstr+='\n'
		newfile.write(wstr)
	newfile.close()
#addTwoKMs('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.4','/s/bach/h/proj/saxs/upuleegk/Soot/KMsCreatedFromNodeAndPathData/km_node_path','/s/bach/h/proj/saxs/upuleegk/Soot/KMsCreatedFromNodeAndPathData/km_mod_cfg_lamda_0.4_and_node_path')
"""
for i in range(1,10):
	addTwoKMs('/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/CFGKMs/mod_km_cfg_1_10_0.'+str(i),'/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/DDKMs/mod_km_dd_1_10_0.'+str(i),'/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/km_afterModifyingIfandAssLabels/combined//mod_km_cfg_dd_add_1_10_0.'+str(i))
"""		

def removeIdenStmtAndGotoNodes(oldDotFile,newDotFileName):
	g=nx.read_dot(oldDotFile)
	nLabels=get_node_labels(g)
	edgeLabel=nx.get_edge_attributes(g,'label')	
	idenNodes=[]
	gotoNodes=[]
	for n in g.nodes():
		if nLabels[n]=='IDEN_STMT':
			idenNodes.append(n)
		if nLabels[n]=='GOTO':
			gotoNodes.append(n)
	for i in gotoNodes:
		print i
		eout=g.out_edges(i)
		print eout
		ein=g.in_edges(i)
		print ein
		if len(eout)>1 or len(ein)>1:
			print "Error: multiple edges coming or going from goto node "+str(i) 
			return
		if edgeLabel[eout[0]]!="\"cfg\"" or edgeLabel[ein[0]]!="\"cfg\"":
			print "Error: either one edge coming or going from goto node "+str(i)+"is not a cfg edge"
                        return 
		
		#print ein
		newEdgeStart=ein[0][0]
		#print eout
		newEdgeEnd=eout[0][1]
		#print newEdgeStart,newEdgeEnd	
		print "Adding cfg edge between nodes: "+str(newEdgeStart)+"-"+str(newEdgeEnd)  
		g.add_edge(newEdgeStart,newEdgeEnd,label="\"cfg\"")
		print "removing GOTO node: "+str(i)
		g.remove_node(i)
	for i in idenNodes:
                print "removing IDEN_STMT node: "+str(i)
                g.remove_node(i)
	nx.write_dot(g,newDotFileName)
#removeIdenStmtAndGotoNodes('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/binarySearchFromTo.dot','/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/idenAndgotoRemovedDotFiles/test.dot') 

def removeIdenStmtAndGotoNodesFromAllDotGraphs():
        path='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/'
	newLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/idenAndgotoRemovedDotFiles/'
        
        for infile in glob.glob(os.path.join(path,'*.dot')):
              	print infile 
		newFileName=newLoc+infile.split('/')[-1]
		removeIdenStmtAndGotoNodes(infile,newFileName)
		print "==============="
#removeIdenStmtAndGotoNodesFromAllDotGraphs()                

def removeMultiGraphEdgesFromDD(dd):
	#print len(dd.edges())
	for i in dd.edges():
		if i[0]==i[1]:
			dd.remove_edge(*i)
	return dd  
	

#dd,cfg=get_dd_cd_subgraphs('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/winsorizedMean.dot')
#removeMultiGraphEdgesFromDD(dd)
