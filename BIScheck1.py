import mechanize
import datetime
import urllib2
from bs4 import BeautifulSoup
import urllib

lb = "*&"*50

# pseudo code

# start with list of bins
# for bin in list_of_bins:

	# open_jobs_filings_page(bin)
	# create_list_of_all_jobs(open_jobs_filings_page)
	# get_info_from_job_links(list_of_links)
	
"jimmyhat"

list_of_bins=["1040908"]

url_dict = {}

# testbin = "1040908" # 706 MADISON
					  # has 2 jobs/filings pages 45 total

testbin = "1041072" # 11 E. 64tth STREET
					  # has only one page of jobs/filings
					  # 5 total jobs/filings

# testbin = "1015862"  # EMPIRE STATE BLDG - MAD FILINGS
					   #  2222 filings as of 1.4.14
 


def url_maker(bin):
	seed_url = "http://a810-bisweb.nyc.gov/bisweb/JobsQueryByLocationServlet?allbin="
	url = seed_url+bin
	return url

def open_page(url):
	page = urllib2.Request(url)
	response = urllib2.urlopen(page)
	content = response.read()
	return content

def search_forms(url):
	try:
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.open(url)
		stoopid = br.select_form(name="frmnext")
		response = br.submit()
		return True
	except:
		return False

def get_jobsfilings_links(url, list):
	# jobslist = []
	#if you declare empty list, it will reset it all the time
	page = urllib2.Request(url)
	response = urllib2.urlopen(page)
	jobspage = response.read()
	soup = BeautifulSoup(jobspage)
	for link in soup.find_all('a'):
		if "JobsQueryBy" in link.get("href"):
			link = link.get("href")
			list.append(link)		
	return list

# print search_forms(url_maker(testbin))

def list_all_job_urls(bin):
	bin_jobs_dict = {}
	url = url_maker(bin)
	jobs_url = "http://a810-bisweb.nyc.gov/bisweb/"
	jobslist = []		
	# if search_forms(url) == True:
	while search_forms(url) == True:
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.open(url)
		bin_jobs_dict[bin] = get_jobsfilings_links(url, jobslist)
		br.select_form(name="frmnext")
		response = br.submit()
		# newpage = response.read()
		new_url = response.geturl()
		print 'deeznuts'
		url = new_url	

		# print 'deeznuts'

	if search_forms(url) == False:
		bin_jobs_dict[bin] = get_jobsfilings_links(url, jobslist)

		print 'bootywhop'
	
	# loop_test = main_dict[bin]
	# i = 0
	# for num in loop_test:
	# 	i += 1
	# return i	

	# the code below constructs a full url
	# for BeautifulSoup to follow

	urllist = []

	for link in bin_jobs_dict[bin]:
		link = jobs_url + link
		urllist.append(link)

	url_dict[bin]= urllist
		
	return url_dict

# print list_all_job_urls(testbin)

def get_job_info(bin):
	job_dict = {}
	links_dict = list_all_job_urls(bin)
	for link in links_dict[bin]:
		# print link
		to_parse = open_page(link)
		soup = BeautifulSoup(to_parse)
		elem = soup.find_all(class_="content")
		print elem
		# jobnum = soup.get_text()
		# print jobnum

		# print 'deeznuts'

print get_job_info(testbin)		

# we want the job_dict have a job# and estimated cost (content)


	# have list of urls
	# need to open page, scrape it
	# and modify a dictionary to include the 
	# right info and tag



	# want data structure to have job# as 

















# def open_page_from_url(link2):
# 	page = urllib2.Request(link2)
# 	response = urllib2.urlopen(page)
# 	jobspage = response.read()
# 	return jobspage


# def return_bis_bin_content(url, bin):

# 	#url = "http://a810-bisweb.nyc.gov/bisweb/bispi00.jsp"
# 	br = mechanize.Browser()
# 	br.set_handle_robots(False)
# 	br.open(url)
# 	br.select_form(nr=2)	
# 	br["bin"] = bin
# 	res = br.submit()
# 	content = res.read()
# 	return content

# # 	with open('mechanize_results.html', 'w') as f:
# # 		f.write(content)

# # with is a safe way to open a file (file.open works) but 
# # the with function closes the file when the block is closed
# # always use with open() in python

# def get_to_jobsfilings_link2(page_content):
# 	soup = BeautifulSoup(page_content)
# 	targetlink = []
# 	i = 0
# 	for link in soup.find_all('a'):
# 		if "JobsQueryBy" in link.get("href"):
# 	 	 	targetlink.append(link)
# 	actual_link_i_need = targetlink[2] 
# 	#this code will break like a motherfucker,
# 	# need to find a better way to select the right link 	
# 	return actual_link_i_need

# link_to_filings = get_to_jobsfilings_link2(return_bis_bin_content(url, bin))
# real_link = janky_gov_link_cleaner(link_to_filings)

# #print real_link

# def open_page_from_url(link2):
# 	page = urllib2.Request(link2)
# 	response = urllib2.urlopen(page)
# 	jobspage = response.read()
# 	return jobspage

# def click_next(page):
# 	br = mechanize.Browser()
# 	br.set_handle_robots(False)
# 	br.open(page)
# 	br.select_form(name="frmnext")
# 	response = br.submit()
# 	return response.read()

# #gotem

# print lb	

# #print open_jobs_filings_page(real_link)

# #jobspage is html content

# def print_all_jobs_links(jobspage):
# 	soup = BeautifulSoup(jobspage)
# 	targetlinks = []
# 	i = 0
# 	for link in soup.find_all('a'):
# 		if "JobsQueryByNumber" in link.get("href"):
# 			i += 1
# 			targetlinks.append(janky_gov_link_cleaner(link))
# 	print lb
# 	print i
# 	return targetlinks

# def collect_all_links_from_all_pages(seed_job_page):
# 	try:
# 		click_next(seed_job_page)
# 	except:
# 		print "deeznuts"	

	
# #print print_all_jobs_links(open_page_from_url(real_link))		


			
# 	# for control in br.form.controls:
# 	# 	#print "Control Name:", control.name
# 	# 	print control
# 	#   this obvously lists the controls out

# 	# print content

# print collect_all_links_from_all_pages("http://a810-bisweb.nyc.gov/bisweb/JobsQueryByLocationServlet?previous.x=34&previous.y=16&allbin=1040908&allcount=0001&allboroughname=&allstrt=&allnumbhous=&jobsubmdate_month=&jobsubmdate_date=&jobsubmdate_year=&allinquirytype=BXS1PRA3&alljobtype=&passdocnumber=&stcodekey=&ckbunique=&glreccountn=0000000045&requestid=3")
# # print collect_all_links_from_all_pages("http://a810-bisweb.nyc.gov/bisweb/JobsQueryByLocationServlet?requestid=1&allbin=1041072&allstrt=EAST%20%20%2064%20STREET&allnumbhous=11")
