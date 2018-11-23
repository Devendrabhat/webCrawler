########### Default Modules ##########
import urllib.request									########## Add .request in end
import urllib.error
import re
import threading
from random import randrange
from numpy import array

############ Self Modules ###########

from modules.filePlay import writeLinkToFile



def isInlink(mainSite,link):
	if re.match(r'^%s'%mainSite,link):                            #### check if inlink or not that is substring or not
		return True
	else:
		return False



def isLinkValid(mainSite,link,UrlStatus):
	
	temp = mainSite.split('/')
	no = len(temp)
	temp = link.split('/')
	
	if no != len(temp):
		flag = 'valid'						#### By default all the links are valid
		link = temp[no]
		for page in UrlStatus.getLinksToExclude():
			pattern = re.compile(re.escape(page))
			if pattern.match(link) and (UrlStatus.getExcluded(page))==0:
				UrlStatus.putExcluded(page,1)				#### Set 1 in dictionary if the link is found
				break
			elif pattern.match(link) and (UrlStatus.getExcluded(page))==1:
				flag = 'invalid'
				break
			
		if re.match(flag,'valid'):
			return True
		else:
			return False
	else:
		return False

class inlinkStatus:
	def __init__(self):
		self.linkStatusDictionary = {}
		self.linkType = {}
		self.linkName = {}
		self.linksToExclude = array(['tests',       #### Excluded links, include here if needed.
									'solitare',
									'models','Specials',
									'review','?','sticker',
									'collection',
									'HomePage',
									'PrivacyPolicy',
									'Connections'])
		
		self.excludedLinks = {key:0 for key in self.linksToExclude}			### Dictionary to maintain the no of times excluded links to allow

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	def getLinksToExclude(self):
		return self.linksToExclude

	def getExcluded(self,page):
		if page in self.excludedLinks:
			no = self.excludedLinks[page]
			return no

	def putExcluded(self,page,no):
		if page not in self.excludedLinks:
			self.excludedLinks[page] = no
		else:
			self.excludedLinks[page] = no


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



	def getLinkName(self,link):
		if link in self.linkName:
			name = self.linkName[link]
			return name

	def putLinkName(self,link,name):
		self.linkName[link] = name
	def hasLinkName(self,link):
		if link in self.linkName:
			return True
		else:
			return False



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



	def getLinkType(self,link):
		if link in self.linkType:
			lType = self.linkType[link]
			return lType

	def putLinkType(self,link,lType):
		if link not in self.linkType:
			self.linkType[link] = lType
	def hasLinkType(self,link):
		if link in self.linkType:
			return True
		else:
			return False



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


	def hasLink(self,link):
		if link in self.linkStatusDictionary:
			return True
		else:
			return False
	def getStatus(self,link):
		if link in self.linkStatusDictionary:
			code = self.linkStatusDictionary[link]
		#	print('Get > '+link+"&&&"+code)
			return code
	def putStatus(self,link,code):
	#	print(link + "&&&" + code)
		if link not in self.linkStatusDictionary:
			self.linkStatusDictionary[link] = code
	#	print('Put > '+link+"&&&"+code)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@



	def getAll(self):
		return self.linkStatusDictionary,self.linkType





def getUserAgent():
	useragents = ('Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0','Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 OPR/51.0.2830.34','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36')
	useragent = useragents[randrange(0,len(useragents))]
#	print(useragent)
	return useragent

def request(threadName,page):
	userAgent = getUserAgent()
#	print(page)
	req = urllib.request.Request(page,None,headers={ 'User-Agent': '{}'.format(userAgent)})
	site = urllib.request.urlopen(req)
	site = site.geturl()
#	print(threadName+" > To = %s"%site)
	req = urllib.request.Request(site,None,headers={ 'User-Agent': '{}'.format(userAgent)})
	site = urllib.request.urlopen(req)
	code = site.getcode()

	return site,code

def checker(mainSite,link,fileName,UrlStatus):
	output_file = open(fileName,'w')

	threadName = (" name of thread : {}".format(threading.current_thread().name))
	#print(threading.current_thread().name+" link =>"+link)
	if isInlink(mainSite,link):
	#	print(threading.current_thread().name+" inlink => "+link)
		status(threadName,"inlink",link,output_file,UrlStatus)
	else:
	#	print(threading.current_thread().name+" outlink => "+link)
		status(threadName,"outlink",link,output_file,UrlStatus)
	output_file.close()



def status(threadName,siteType,page,outputObject,UrlStatus):
	#print(threadName+" > {} => ".format(siteType)+link)
	try:
		if not UrlStatus.hasLinkType(page):				### page contains original link
			UrlStatus.putLinkType(page,siteType)
		if UrlStatus.hasLink(page):
			code = UrlStatus.getStatus(page)
		#	print(threadName+' > '+code)
		#	writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+link,code)			
		elif not UrlStatus.hasLink(page):
			site,code = request(threadName,page)		### site contains redirected link
			UrlStatus.putStatus(page,code)
			linkName = UrlStatus.getLinkName(page)
			# if linkName is None:
			# 	writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+link,code,'no name found')			
			# 	print('none')
			# else:
			# 	writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+link,code,linkName)			
			# 	print(linkName+' = {}'.format(type(linkName)))

	except urllib.error.HTTPError as e:
		e = str(e)
		code = (e.split())[2]
		code = (code.split(':'))[0]
	#	print(threadName+" > {} => ".format(siteType)+page+' > '+code)
	#	print(threadName+' > '+code)
		# if not UrlStatus.hasLink(page):
		# 	UrlStatus.putStatus(page,code)
		linkName = UrlStatus.getLinkName(page)
		if linkName is None:
			writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,code,"No Name found")
			# print('none')
		elif re.match(r'^\n',linkName):								####### for name only with space
			writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,code,"No Name found")
		else:
			writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,code,linkName)
			# print(linkName+' = {}'.format(type(linkName)))
		#writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,code)
	except urllib.error.URLError as e:
		e = str(e)
		#print(threadName+'> {} > '.format(page)+"URLError")
		# if not UrlStatus.hasLink(page):
		# 	UrlStatus.putStatus(page,code)
		writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,"URLError",'none')
	except UnicodeError as e:
		writeLinkToFile(outputObject,"\n"+"{} => ".format(siteType)+page,"UnicodeError",'none')


def test():
	return 4,5
