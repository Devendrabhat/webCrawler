import os
import re
from bs4.element import Comment

from modules import filePlay


class wordsProcessor:

	def __init__(self):
		self.elements = ['style', 'script', 'head', 'title', 'meta', '[document]']
		self.pageText = ''

	def putPageText(self,pageText):
		self.pageText = pageText
	def tag_visible(self,element):
	    if element.parent.name in self.elements:
	        return False
	    if isinstance(element, Comment):
	        return False
	    return True

	def hasWord(self,word):
		if re.search(word,self.pageText):
		    return True
		else:
		    return False

	def getInvalidWords(self,homeDir):
		fileObject = open(os.path.join(homeDir,'invalidWords.txt'),'r+')
		self.invalidWords = filePlay.readfile(fileObject)
		fileObject.close()
		self.invalidWords = [word[:-1].lower() for word in self.invalidWords if word != '\n']

		return self.invalidWords



def wordFinder(soup,filePath,homeDir):
	finder = wordsProcessor()
	output_file = open(filePath,'w')
	
	rawTexts = soup.findAll(text = True)
	visibleTexts = filter(finder.tag_visible, rawTexts)
	pageTexts = u" ".join(t.strip() for t in visibleTexts)
	finder.putPageText(pageTexts.lower())

	invalidWords = finder.getInvalidWords(homeDir)

	for word in invalidWords:
		if finder.hasWord(word):
			print("found "+word)
			filePlay.writeWordToFile(output_file,word)


	output_file.close()