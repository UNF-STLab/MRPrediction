def createDataDict(featFileName):
	featFile=open(featFileName,'r')
	lines=featFile.readlines()
	data={}	
	for l in lines:
		field1=(l.split(',')[0]).split('/')
		vals=(l.strip().split(',')[1]).split(' ')[2:]
		prog=(field1[len(field1)-1].split('.'))[0]
		featureVals={}

		for i in vals:
	 		cell=i.split(':')
			featureVals[cell[0]]=cell[1]
		data[prog]=featureVals
	print len(data)
	return data

def createKM(data,class_file_name,km_file_name):
	class_file=open(class_file_name,'r')
        dot_file_names=[]

        for line in class_file:
                fields=line.strip('\n').split(':')
                dot_file_names.append(fields[0])
        class_file.close()
               
        f=open(km_file_name,'w')
        for i in range(0,len(dot_file_names)):
                temp_str=str(dot_file_names[i])
		iFeats=data[dot_file_names[i]]
                for j in range(0,len(dot_file_names)):
			jFeats=data[dot_file_names[j]]
			val=0
			for iKey in iFeats.keys():
				if jFeats.has_key(iKey):
					val+=float(iFeats[iKey])*float(jFeats[iKey])
			temp_str+=','+str(val)
		temp_str+='\n'
                f.write(temp_str)					
	f.close()
	

data=createDataDict('/s/bach/h/proj/saxs/upuleegk/Soot/openSourceMethods/AllUsedMethods/DataFiles/add_new_osmethods_cfg_only_with_startEndPaths')
createKM(data,'/s/bach/h/proj/saxs/upuleegk/Soot/classLabelFiles/addClassLabelFinal1','/s/bach/h/proj/saxs/upuleegk/Soot/KMsCreatedFromNodeAndPathData/km_node_path')


