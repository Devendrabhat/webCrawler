import re


def findDomainOfMainSite(mainSite):
	domains = ('com','ca','au','nz','net','org','co','gm','info','biz','vegas','us','mx')
	d1 = mainSite.split('.')
	d2 = d1[-1].split('/')
	domain = d2[0]
	name = d1[1]
	return name,domain

def findDomainInLink(domains,link):
	for domain in domains:
		if domain in link:
			return True

def getFileName(soup):
	link = soup.find(string = re.compile('webId'))
	l = str(link)
	l = set(l.split(','))
	#pattern = re.compile(r'^\"webId\".')
	pattern = (r'^\"webId\".')
	for i in l:
		if re.search(pattern,i):
			name = (i.split(':'))[1]
			if name != 'null':
				name = (name.split('\"'))[1]
				return name


def findAllLinks(soup,mainSite,UrlStatus):
	urls = []
	iterator = 1
	site_name,domain=findDomainOfMainSite(mainSite)             					 	##### from scrappy.py 
	allDomains = ('.com','.ca','.au','.nz','.net','.org','.co','.gm','.info','.biz','.vegas','.us','.mx')
	links = soup.find_all('a')
	for lin in links:											####### Checking all sorts of links (link validator)
		lTemp = lin.get('href')
		link = lTemp
		link_name = lin.string
		if type(link) is str and re.match(r'^http',link):       ####### Pure http link
			urls.append(link)
			UrlStatus.putLinkName(link,link_name)
			# print(link_name)
			# print(link)
			
		elif type(link) is str and re.match(r'^/',link):		####### links starting with /
			link = (mainSite.split(domain))[0]+domain+link
		#	print(site_domain)
			# print(link)
			urls.append(link)
			UrlStatus.putLinkName(link,link_name)
			# print(link_name)
		elif type(link) is str and re.match(r'^//',link):       ####### links starting with //
			link = 'https:'+link
		#	print(site_domain)
			# print(link)
			urls.append(link)
			UrlStatus.putLinkName(link,link_name)
			# print(link_name)
		elif type(link) is str and re.match(r'^[A-Z]',link):        ###### links starting with only capitol letters
			link = (mainSite.split(domain))[0]+domain+'/'+link
			urls.append(link)
			UrlStatus.putLinkName(link,link_name)
			# print(link_name)
			# print(link)
		elif type(link) is str and re.match(r'^[a-z]',link):        ###### links starting with only small letters
			if re.match(r'^tel',link):								###### it have to be different because there is tel no as well.	
				pass
			elif re.match(r'^mailto',link):								###### it have to be different because there is tel no as well.	
				pass
			elif findDomainInLink(allDomains,link):
				link = 'https://'+link 								###### Just append https:// to external links of some domain is found in it
				urls.append(link)
				UrlStatus.putLinkName(link,link_name)
				# print(link_name)
				# print(link)
			else:
				link = (mainSite.split(domain))[0]+domain+'/'+link      ###### So consider all other char other then tel.
				urls.append(link)                                     
				UrlStatus.putLinkName(link,link_name)
				# print(link_name)
				# print(link)
	
		else:
			pass
		#	print(link)
	return urls





# import urllib
# from bs4 import BeautifulSoup as bs 
# site = urllib.request.urlopen('https://google.com')
# soup = bs(site,'html.parser')
# taga = soup.a
# taga.string