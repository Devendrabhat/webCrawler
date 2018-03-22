import os


def readfile(object):							##	Basic function to read files 
	return object.readlines()


def writefile(object,data,code,linkName):                ##	Basic function to write into files (mainly for checker)
	object.write(data+" ==>> "+code+" ==>> "+linkName)

def combiner(line,newDir,newFile):
	print("Writing final output to %s"%newFile)
	fileNames = os.listdir(newDir)          
	with open(newFile,'a+') as output_file:
		output_file.write("\n\nnew page => "+line+"\n")
		for file in fileNames:
		#	print(newDir)
			with open("%s/%s"%(newDir,file),'r') as inputObject:      ####### change slash
				data = inputObject.read()
#				print(data)
				output_file.write(data)
	

