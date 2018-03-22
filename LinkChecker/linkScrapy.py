########### Default Modules ##########
from bs4 import BeautifulSoup as bs
import re
import threading
import os
import time
import queue
import shutil
from numpy import array

############ Self Modules ###########
from modules import scrapper
from modules import filePlay
from modules import linkDetails

###################### Main Module (  Called from Below  )



def main(input_file):

	
	sites = filePlay.readfile(input_file)
	site_iterator = 1

	q = queue.Queue()

	if os.path.isdir('temp')==True:
		shutil.rmtree('temp')

	os.mkdir('temp')
	cwd = os.getcwd()                               ###### main directory             	$current dir = ./
	os.chdir('temp')								###### operate in temp directory  	$current dir = ./temp
	#linkToExclude = ['VehicleSearchResults','VehicleDetails','models','Specials','reviews','?', 'f_ ', 'ConnectedStore_D']
	
	sites = array(sites)
	for site in sites:
		initialTime = time.time()
		site = site[:-1]							###### cleaning base url
		if re.match(r'/',site[-1]):
			site = site[:-1]
#		print(site)
		q.put(site)
		os.mkdir('output{}'.format(site_iterator))
		os.chdir('output{}'.format(site_iterator)) 	######						$current dir = ./temp/output{link_no}

		
		link_iterator = 1
		uniqueLinkSet = set()
		DictionaryUrl = {}
		DictionaryUrl[site]=1						###### To maintain the unique links to work with	
		UrlStatus = linkDetails.inlinkStatus()		###### To maintain the unique links for status
		mainSite = site
		while not q.empty():
			page = q.get()
			uniqueLinkSet.add(page)
			DictionaryUrl[page] = 0 				###### as soon as removes the link from queue set 0 to dictionary
			os.mkdir('output{}'.format(link_iterator))
			print("current page "+page)

			site,code = linkDetails.request('mainThread',page)        ###$$$$****&&&&^^*))($#$%^&*&)  put this in if else for main site
			#print(site.read())
			if not UrlStatus.hasLink(page):
				UrlStatus.putStatus(page,code)
			#print(UrlStatus.getAll())
			soup = bs(site,'html.parser')

			if re.match(mainSite,page):
				name = scrapper.getFileName(soup)

			urls = scrapper.findAllLinks(soup,mainSite,UrlStatus)			###### Finds and returns the set of urls on the page
			
			urls = list(urls)
			
			
			tempList = list()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    Url filtering
			fileName = "output{}/fileNextGen".format(link_iterator)
			output_file = open(fileName,'a')
			for url in urls:
				#print(url)
				if re.search('nextGen=false',url) or re.search('disableAutofill=true',url):
					#print(url)
					output_file.write(("\n nextGen=false or disableAutofill=true ".upper())+url)
				elif re.search(r'FactoryPreOwnedCollection', url):
					pass
				elif linkDetails.isInlink(mainSite,url):
					if linkDetails.isLinkValid(mainSite,url,UrlStatus):
						tempList.append(url)
				else:
					tempList.append(url)
				#	print(url)
			output_file.close()
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

			urls = tempList
			print(len(urls))
			
			

			no = len(urls)				#--------------------------- Total no of unique links found
			iterator=1
			t=[]
			for url in urls:
		#		print(url)
				t.append(threading.Thread(target=linkDetails.checker,args=(mainSite,url,"output{}/file{}".format(link_iterator,iterator),UrlStatus),name='t{}'.format(iterator)))
				iterator+=1

			iterator=0
			while iterator<no:
				t[iterator].start()
				iterator+=1

			iterator=0
			while iterator<no:
				t[iterator].join()
				iterator+=1

			filePlay.combiner(page,"output{}".format(link_iterator),"{}/{}_{}.csv".format(cwd,name,time.strftime("%A%d%b%y")))     #### change slash
					#   | arg 1 !! slash above							| arg 2					!! timestamp (Day,HH,date)
			

			for url in urls:
				linkType = UrlStatus.getLinkType(url)
				#print(url)
				if UrlStatus.hasLinkType(url) and re.match(r'inlink',linkType):
					code = UrlStatus.getStatus(url)
					#print(type(code))
					if UrlStatus.hasLink(url) and code == 200:
						if url in DictionaryUrl:
							pass
						else:
							DictionaryUrl[url] = 1


			for url in DictionaryUrl:
				if DictionaryUrl[url] == 1 and url not in uniqueLinkSet:
					q.put(url)


			for url in DictionaryUrl:
				#print(url)
				uniqueLinkSet.add(url)




			link_iterator+=1
		
		#statusDict,typeDict = UrlStatus.getAll()
		#print(len(typeDict))
		#print(len(statusDict))

		os.chdir('../')									######				$current dir = ./temp
		print('Site {} is completed in {}'.format(site_iterator,time.time()-initialTime))
		site_iterator+=1
	os.chdir('../')										######				$current dir = ./
	if os.path.isdir('temp')==True:
		shutil.rmtree('temp')





################################   Main Function Call   #################################
if __name__ == "__main__":
	input_file = open('sites.txt','r')
	main(input_file)                     ######## calling of the main link
	input_file.close()