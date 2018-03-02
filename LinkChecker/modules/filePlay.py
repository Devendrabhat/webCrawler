import os


def readfile(object):							##	Basic function to read files 
	return object.readlines()


def writefile(object,data,code,linkName):                ##	Basic function to write into files (mainly for checker)
	object.write(data+" ==>> "+code+" ==>> "+linkName)


def combiner(line,newDir):
	printingStack=[]
	printingStack.append("\n\nnew page => "+line+"\n")
	for file in os.listdir(newDir):
#		print(newDir)
		with open("%s/%s"%(newDir,file),'r') as inputObject:      ####### change slash
			data = inputObject.read()
#			print(data)
			if data.split():
				printingStack.append(data)			
	return printingStack

def writter(printingStack,newFile):
	if len(printingStack)==1:
		return "No errors"
	with open(newFile,'a+') as output_file:
		data = ''
		while printingStack:
			data = printingStack.pop()+data
		print("Writing final output to %s"%newFile)
		output_file.write(data)

