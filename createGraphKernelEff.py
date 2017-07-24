import networkx as nx
import SootUtilities as sUtil
import numpy as np 
import glob
import os
import pickle
import math
import sys

def create_direct_product_graph(g1,g2):
	g1_nodes=g1.nodes()
	g2_nodes=g2.nodes()
	#print len(g1_nodes)
	#print len(g2_nodes)
	g1_labels=sUtil.get_node_labels(g1)
	g2_labels=sUtil.get_node_labels(g2) 
	#g1_labels=nx.get_node_attributes(g1,'l')
	#g2_labels=nx.get_node_attributes(g2,'l')	
	dpg=nx.DiGraph()
	node_cnt=0;	
	for n in g1_nodes:
		for m in g2_nodes:
			if(g1_labels[n]==g2_labels[m]):
				dpg.add_node(node_cnt,v_i=n,w_i=m)
				node_cnt+=1

	#print dpg.nodes()
	dpg_nodes=dpg.nodes()
	for i in dpg_nodes:
		for j in dpg_nodes:
			if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'])) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i']))):
				dpg.add_edge(i,j)	
			
	#print dpg.nodes()
	#print dpg.edges()
	a=nx.adjacency_matrix(dpg)
	return a	

def get_similarity(l1,l2):

	if(l1==l2):
		return 1
	elif(sUtil.get_group(l1)==sUtil.get_group(l2)):
		return 0.5
	else:
		return 0
def get_similarity_exactEqual(l1,l2):
	if(l1==l2):
                return 1
        else:
                return 0
		

def createNodeKernelValsDict():
	nodeKernelFile=open('/s/bach/h/proj/saxs/upuleegk/Soot/graphletKernelData/nodeKernelVals')
	lines=nodeKernelFile.readlines()
	nodeKernelVals={}
	for i in lines:
		fields=i.strip('\n').split(',')
		nodeKernelVals[fields[0],fields[1]]=float(fields[2])
	return nodeKernelVals
		
def get_similarity_with_paramk(l1,l2,paramk):

        if(l1==l2):
                return 1
        elif(sUtil.get_group(l1)==sUtil.get_group(l2)):
                return paramk
        else:
                return 0

def create_modified_DPG(g1,g2):
        g1_nodes=g1.nodes()
        g2_nodes=g2.nodes()
        #print len(g1_nodes)
        #print len(g2_nodes)
        g1_labels=sUtil.get_node_labels(g1)
        g2_labels=sUtil.get_node_labels(g2)
        #g1_labels=nx.get_node_attributes(g1,'l')
        #g2_labels=nx.get_node_attributes(g2,'l')
        dpg=nx.DiGraph()
        node_cnt=0;
        for n in g1_nodes:
                for m in g2_nodes:
                        dpg.add_node(node_cnt,v_i=n,w_i=m)
                        node_cnt+=1

        #print dpg.nodes()
        dpg_nodes=dpg.nodes()
        for i in dpg_nodes:
                for j in dpg_nodes:
                        if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'])) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i']))):
                                i_v_label=g1_labels[dpg.node[i]['v_i']]
				i_w_label=g2_labels[dpg.node[i]['w_i']]
				j_v_label=g1_labels[dpg.node[j]['v_i']]
				j_w_label=g2_labels[dpg.node[j]['w_i']]
				dpg.add_edge(i,j,weight=get_similarity(i_v_label,i_w_label)*get_similarity(j_v_label,j_w_label))

        #print dpg.nodes()
        #print dpg.edges()
        a=nx.attr_matrix(dpg,edge_attr='weight',rc_order=dpg.nodes())
        return a

#a=create_modified_DPG(nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/test1.dot'),nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/test2.dot'))
#print a

def create_modified_DPG_with_paramk(g1,g2,paramk):
        g1_nodes=g1.nodes()
        g2_nodes=g2.nodes()
        #print len(g1_nodes)
        #print len(g2_nodes)
        g1_labels=sUtil.get_node_labels(g1)
        g2_labels=sUtil.get_node_labels(g2)
        #g1_labels=nx.get_node_attributes(g1,'l')
        #g2_labels=nx.get_node_attributes(g2,'l')
        dpg=nx.DiGraph()
        node_cnt=0;
        for n in g1_nodes:
                for m in g2_nodes:
                        dpg.add_node(node_cnt,v_i=n,w_i=m)
                        node_cnt+=1

        #print dpg.nodes()
        dpg_nodes=dpg.nodes()
        for i in dpg_nodes:
                for j in dpg_nodes:
                        if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'])) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i']))):
                                i_v_label=g1_labels[dpg.node[i]['v_i']]
                                i_w_label=g2_labels[dpg.node[i]['w_i']]
                                j_v_label=g1_labels[dpg.node[j]['v_i']]
                                j_w_label=g2_labels[dpg.node[j]['w_i']]
                                dpg.add_edge(i,j,weight=get_similarity_with_paramk(i_v_label,i_w_label,paramk)*get_similarity_with_paramk(j_v_label,j_w_label,paramk))
                                

        #print dpg.nodes()
        #print dpg.edges()
        a=nx.attr_matrix(dpg,edge_attr='weight',rc_order=dpg.nodes())
        return a

def getCFGAndDDEdges(g):
	cfgEdges=[]
	ddEdges=[]
	for i in g.nodes():
		for j in g.nodes():
			#print i,j
			edata=g.get_edge_data(i,j,default=0)
			if edata!=0:
				#print i,j
				if len(edata)==1:
					if edata[0]['label']=='\"cfg\"':
						cfgEdges.append((i,j))
					if edata[0]['label']=='\"DD\"':
                                                ddEdges.append((i,j))
				else:
					#print edata[0]['label'],edata[1]['label']
					if edata[0]['label']=='\"cfg\"':
                                                cfgEdges.append((i,j))
                                        if edata[0]['label']=='\"DD\"':
                                                ddEdges.append((i,j))
					if edata[1]['label']=='\"cfg\"':
                                                cfgEdges.append((i,j))
                                        if edata[1]['label']=='\"DD\"':
                                                ddEdges.append((i,j))
	#print len(cfgEdges)
	#print len(ddEdges)
	return cfgEdges,ddEdges
					
def create_modified_DPG_with_paramk_both_cfg_dd_edges(g1_multi,g2_multi,paramk):
	#print nx.info(g1)
	g1=sUtil.removeMultiGraphEdgesFromDD(g1_multi)
	g2=sUtil.removeMultiGraphEdgesFromDD(g2_multi)
        g1_nodes=g1.nodes()
        g2_nodes=g2.nodes()
        #print len(g1_nodes)
        #print len(g2_nodes)
        g1_labels=sUtil.get_node_labels(g1)
        g2_labels=sUtil.get_node_labels(g2)
	#g1EdgeLabels=nx.get_edge_attributes(g1,'label')
	#print g1EdgeLabels
        #g2EdgeLabels=nx.get_edge_attributes(g2,'label')
	#print len(g2.get_edge_data('12','13'))
	g1CfgEdges,g1DDEdges=getCFGAndDDEdges(g1)
        g2CfgEdges,g2DDEdges=getCFGAndDDEdges(g2)
	print g1DDEdges
	print g2DDEdges 
	#print g2EdgeLabels['12','13']
	#g1_labels=nx.get_node_attributes(g1,'l')
        #g2_labels=nx.get_node_attributes(g2,'l')
        dpg=nx.DiGraph()
        node_cnt=0;
        for n in g1_nodes:
                for m in g2_nodes:
                        dpg.add_node(node_cnt,v_i=n,w_i=m)
                        node_cnt+=1

        #print dpg.nodes()
        dpg_nodes=dpg.nodes()
	
        for i in dpg_nodes:
                for j in dpg_nodes:
                        #if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'])) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i'])) and ((dpg.node[i]['v_i'],dpg.node[j]['v_i']) in g1CfgEdges) and ((dpg.node[i]['w_i'],dpg.node[j]['w_i']) in g2CfgEdges)):
			if (((dpg.node[i]['v_i'],dpg.node[j]['v_i']) in g1CfgEdges) and ((dpg.node[i]['w_i'],dpg.node[j]['w_i']) in g2CfgEdges)):

				print 'cfg: ' +str(dpg.node[i]['v_i'])+","+str(dpg.node[j]['v_i'])+","+str(dpg.node[i]['w_i'])+","+str(dpg.node[j]['w_i'])
                                i_v_label=g1_labels[dpg.node[i]['v_i']]
                                i_w_label=g2_labels[dpg.node[i]['w_i']]
                                j_v_label=g1_labels[dpg.node[j]['v_i']]
                                j_w_label=g2_labels[dpg.node[j]['w_i']]
				dpg.add_edge(i,j,weight=get_similarity_with_paramk(i_v_label,i_w_label,paramk)*get_similarity_with_paramk(j_v_label,j_w_label,paramk))
			#if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'],key='DD')) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i']))  and ((dpg.node[i]['v_i'],dpg.node[j]['v_i']) in g1DDEdges) and ((dpg.node[i]['w_i'],dpg.node[j]['w_i']) in g2DDEdges)):
			if (((dpg.node[i]['v_i'],dpg.node[j]['v_i']) in g1DDEdges) and ((dpg.node[i]['w_i'],dpg.node[j]['w_i']) in g2DDEdges)):
				print 'DD: ' +str(dpg.node[i]['v_i'])+str(dpg.node[j]['v_i'])+str(dpg.node[i]['w_i'])+str(dpg.node[j]['w_i'])
                                i_v_label=g1_labels[dpg.node[i]['v_i']]
                                i_w_label=g2_labels[dpg.node[i]['w_i']]
                                j_v_label=g1_labels[dpg.node[j]['v_i']]
                                j_w_label=g2_labels[dpg.node[j]['w_i']]
				dpg.add_edge(i,j,weight=get_similarity_with_paramk(i_v_label,i_w_label,paramk)*get_similarity_with_paramk(j_v_label,j_w_label,paramk))

        #print dpg.nodes()
        #print dpg.edges()
        a=nx.attr_matrix(dpg,edge_attr='weight',rc_order=dpg.nodes())
	print a
        return a
#create_modified_DPG_with_paramk_both_cfg_dd_edges(nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/add_values.dot'),nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles/winsorizedMean.dot'),0.5)	

def create_modified_DPG_with_nodeKernelValsFromFile(g1,g2):
        g1_nodes=g1.nodes()
        g2_nodes=g2.nodes()
        #print len(g1_nodes)
        #print len(g2_nodes)
        g1_labels=sUtil.get_node_labels(g1)
        g2_labels=sUtil.get_node_labels(g2)
        #g1_labels=nx.get_node_attributes(g1,'l')
        #g2_labels=nx.get_node_attributes(g2,'l')
        nodeKernelVals=createNodeKernelValsDict()
        dpg=nx.DiGraph()
        node_cnt=0;
        for n in g1_nodes:
                for m in g2_nodes:
                        dpg.add_node(node_cnt,v_i=n,w_i=m)
                        node_cnt+=1

        #print dpg.nodes()
        dpg_nodes=dpg.nodes()
        for i in dpg_nodes:
                for j in dpg_nodes:
                        if((g1.has_edge(dpg.node[i]['v_i'],dpg.node[j]['v_i'])) and (g2.has_edge(dpg.node[i]['w_i'],dpg.node[j]['w_i']))):
                                i_v_label=g1_labels[dpg.node[i]['v_i']]
                                i_w_label=g2_labels[dpg.node[i]['w_i']]
                                j_v_label=g1_labels[dpg.node[j]['v_i']]
                                j_w_label=g2_labels[dpg.node[j]['w_i']]
                                dpg.add_edge(i,j,weight=nodeKernelVals[i_v_label,i_w_label]*nodeKernelVals[j_v_label,j_w_label])
                                

        #print dpg.nodes()
        #print dpg.edges()
        a=nx.attr_matrix(dpg,edge_attr='weight',rc_order=dpg.nodes())
        return a

def get_num_similar_paths_of_length_n(a,n):
	
	#dpg=create_direct_product_graph(g1,g2)
        #a=nx.adjacency_matrix(dpg)
        a_pow=np.linalg.matrix_power(a,n)
        #num_paths=a_pow.sum()
        #return num_paths
	return a_pow


def create_comma_class_label_file(in_file_name,comma_file_name):
	class_file=open(in_file_name,'r')
	comma_class_file=open(comma_file_name,'w')
	for line in class_file:
        	fields=line.strip('\n').split(':')
        	comma_class_file.write(str(fields[0])+','+str(fields[1])+'\n')
        class_file.close()
	comma_class_file.close()
		
#create_comma_class_label_file('/s/bach/h/proj/saxs/upuleegk/Soot/inclusive_class_label','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/inclusive/inclusive_class_label_comma') 

#set paramk to 0.5 to get the default behaviour 
def create_kernel_matrix_add_path_length(class_file_name,km_file_name,path_len,lamda,paramk):
	class_file=open(class_file_name,'r')
	dot_file_names=[]

	for line in class_file:
		fields=line.strip('\n').split(',')
	        dot_file_names.append(fields[0])
	class_file.close()
	#dot file location of files that has idenstmts and goto
	#dotFileLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles'
	#dot file location of files that has removed idenstmts and goto
	dotFileLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/allTrainingAndSaxsMutatedFuns'
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
				dd1,g1=sUtil.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[i]+'.dot')
				#g1=sUtil.removeMultiGraphEdgesFromDD(dd1)
				#g2=nx.read_dot(dotFileLoc+'/'+dot_file_names[j]+'.dot')
				dd2,g2=sUtil.get_dd_cd_subgraphs(dotFileLoc+'/'+dot_file_names[j]+'.dot')
				#g2=sUtil.removeMultiGraphEdgesFromDD(dd2)
				#a=create_modified_DPG(g1,g2)
				a=create_modified_DPG_with_paramk(g1,g2,paramk)
				#a=create_modified_DPG_with_nodeKernelValsFromFile(g1,g2)
				mat=math.pow(lamda,0)*get_num_similar_paths_of_length_n(a,0)
				for l in range(1,path_len+1):
					temp_mat= math.pow(lamda,l)*get_num_similar_paths_of_length_n(a,l)
					mat=np.add(mat,temp_mat)
				val=mat.sum()
				computedValsDict[str(i)+'.'+str(j)]=val
			temp_str+=','+str(val)
		temp_str+='\n'
		f.write(temp_str)	
	f.close()
	os.system("mailx -s \"File writing finished\" < /dev/null \"upuleegk@gmail.com\"")
create_kernel_matrix_add_path_length(sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))

def create_kernel_matrix_add_path_length_both_cfg_and_dd(class_file_name,km_file_name,path_len,lamda,paramk):
        class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()
        #dot file location of files that has idenstmts and goto
        #dotFileLoc='/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/AllUsedDotFiles'
        #dot file location of files that has removed idenstmts and goto
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
                                g1=nx.read_dot(dotFileLoc+'/'+dot_file_names[i]+'.dot')
                                g2=nx.read_dot(dotFileLoc+'/'+dot_file_names[j]+'.dot')
				a=create_modified_DPG_with_paramk_both_cfg_dd_edges(g1,g2,paramk)
                                #a=create_modified_DPG_with_nodeKernelValsFromFile(g1,g2)
                                mat=math.pow(lamda,0)*get_num_similar_paths_of_length_n(a,0)
                                for l in range(1,path_len+1):
                                        temp_mat= math.pow(lamda,l)*get_num_similar_paths_of_length_n(a,l)
                                        mat=np.add(mat,temp_mat)
                                val=mat.sum()
                                computedValsDict[str(i)+'.'+str(j)]=val
                        temp_str+=','+str(val)
                temp_str+='\n'
                f.write(temp_str)
        f.close()
        os.system("mailx -s \"File writing finished\" < /dev/null \"upuleegk@gmail.com\"")
#create_kernel_matrix_add_path_length_both_cfg_and_dd(sys.argv[1],sys.argv[2],int(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))

                
def create_kernel_matrix_converge_path_length(class_file_name,km_file_name,lamda):
        class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()

        f=open(km_file_name,'w')
        for i in range(0,len(dot_file_names)):
                temp_str=str(dot_file_names[i])
                for j in range(0,len(dot_file_names)):
                        g1=nx.read_dot(dot_file_names[i])
                        g2=nx.read_dot(dot_file_names[j])
                        print dot_file_names[i]
			print dot_file_names[j]
			a=create_direct_product_graph(g1,g2)
                        mat=math.pow(lamda,0)*get_num_similar_paths_of_length_n(a,0)
                        p_len=1
			pre_val=mat.sum()
			while True:
				print 'path len'+str(p_len)	
                                temp_mat= math.pow(lamda,p_len)*get_num_similar_paths_of_length_n(a,p_len)
                                mat=np.add(mat,temp_mat)
				val=mat.sum()
				#print val
				if(math.fabs(val-pre_val)<0.001 or p_len>20):
					print '========='
					break
				pre_val=val
				p_len+=1
                        temp_str+=','+str(val)
                temp_str+='\n'
                f.write(temp_str)
        f.close()


#old method used for computing matrices with multiple lamda values. When running in multiple machines not required 
def create_data_files_with_lamda_arr():
	#arr_lamda=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
	arr_lamda=[0.1,0.2]
	for i in range(len(arr_lamda)):
		print('lamda ='+str(arr_lamda[i]))
		create_kernel_matrix_add_path_length('/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/testClassLabel','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/OpenSourceMethodData/test/mod_km_test_1_10_'+str(arr_lamda[i]),10,arr_lamda[i])

#create_data_files_with_lamda_arr()

def create_data_files_with_lamda_arr_conv():
        arr_lamda=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        for i in range(len(arr_lamda)):
                print('lamda ='+str(arr_lamda[i]))
                create_kernel_matrix_converge_path_length('/s/bach/h/proj/saxs/upuleegk/Soot/per_class_label','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/per/km_per_conv_'+str(arr_lamda[i]),arr_lamda[i])
	#os.system('mail -s \'Done per\' upuleegk@gmail.com < ./per_out.txt')

#create_data_files_with_lamda_arr_conv()

def create_kernel_matrix_single_path_length(class_file_name,km_file_name,path_len):
        class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()

        f=open(km_file_name,'w')
        for i in range(0,len(dot_file_names)):
                temp_str=str(dot_file_names[i])
                for j in range(0,len(dot_file_names)):
                        g1=nx.read_dot(dot_file_names[i])
                        g2=nx.read_dot(dot_file_names[j])
                        val= get_num_similar_paths_of_length_n(g1,g2,path_len).sum()
                        temp_str+=','+str(val)
                temp_str+='\n'
                f.write(temp_str)
        f.close()

#create_kernel_matrix_single_path_length('/s/bach/h/proj/saxs/upuleegk/Soot/per_class_label','/s/bach/h/proj/saxs/upuleegk/Soot/graphKernelData/km_2',2)


"""
g1=nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/bubbleSort.dot')
g2=nx.read_dot('/s/bach/h/proj/saxs/upuleegk/Soot/binary_search.dot')

g1=nx.DiGraph()
g1.add_node(1,l='a')
g1.add_node(2,l='b')
g1.add_node(3,l='c')
g1.add_node(4,l='a')
g1.add_edges_from([(1,2),(1,3),(2,4),(3,4),(2,3)])
g2=nx.DiGraph()
g2.add_node(1,l='a')
g2.add_node(2,l='b')
g2.add_node(3,l='c')
g2.add_node(4,l='a')
g2.add_edges_from([(1,2),(1,3),(2,4),(3,4),(1,4)])

for i in range(1,10): 
	print get_num_similar_paths_of_length_n(g1,g2,i)
"""
