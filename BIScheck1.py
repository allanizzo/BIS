import mechanize
import datetime
import urllib2
from bs4 import BeautifulSoup
from bs4 import NavigableString
import urllib
import re
import xlwt	

lb = "*&"*50

# pseudo code

# start with list of bins
# for bin in list_of_bins:

	# open_jobs_filings_page(bin)
	# create_list_of_all_jobs(open_jobs_filings_page)
	# get_info_from_job_links(list_of_links)

"jimmyhat"

list_of_bins=["1041072", "1040908"]

url_dict = {}

testbin = "1040908" # 706 MADISON
					  # has 2 jobs/filings pages 45 total

# testbin = "1041072" # 11 E. 64tth STREET
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
	jobslist = []
	jobs_url = "http://a810-bisweb.nyc.gov/bisweb/"	
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
		# print 'deeznuts'
		url = new_url	

		print 'deeznuts'

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
	# i = 0
	for link in bin_jobs_dict[bin]:
		# print link
		# i+=1
		link = jobs_url + link
		urllist.append(link)
	# print i	

	url_dict[bin]= urllist
		
	return url_dict

# print list_all_job_urls(testbin)

# def surrounded_by_strings(tag):
#     return (isinstance(tag.next_element, NavigableString)
#             and isinstance(tag.previous_element, NavigableString))

def get_job_info(bin):
	links_dict = list_all_job_urls(bin)
	binlist = []
	for link in links_dict[bin]:
		# print link
		minilist = []
		to_parse = open_page(link)
		soup = BeautifulSoup(to_parse)
		for tag in soup.find_all('td'):
			# print tag
			if tag.find(text=re.compile("Job No:")):
				minilist.append(tag.string)
			if tag.find(text=re.compile("Document:")):
				minilist.append(tag.string)
			#	getting duplicates here	
			if tag.find(text=re.compile("Job Type:")):
				minilist.append(tag.string)	
			if tag.find(text=re.compile("Estimated Total")):	
				# minilist.append(tag.string)
				# build = tag.string
				# now need to get the estimated cost string from tag
				minilist.append(tag.find_next('td').string)
				# build = build + (tag.find_next('td').string)
				# print build
				# minilist.append(build)
				binlist.append(minilist)
			# print tag

	# binlist.append(jobnumlist)
	return binlist

# print get_job_info(testbin)	


def output_to_excel(bin):
	jobinfo = get_job_info(bin)
	# print jobinfo
	wb = xlwt.Workbook()
	ws = wb.add_sheet(str(bin))
	# col0_name = "Sheet num"
	bin_col = "Bin #"
	col1_name = 'Job #'
	col2_name = 'Document #'
	col3_name = 'Job Type'
	col4_name = 'Est Cost'

	rowcount = 0

	ws.write(rowcount,0, bin_col)
	ws.write(rowcount,1, str(bin))

	rowcount += 2

	ws.write(rowcount,0, col1_name)
	ws.write(rowcount,1, col2_name)
	ws.write(rowcount,2, col3_name)
	ws.write(rowcount,3, col4_name)
	# ws.write(0,3, col4_name)

	rowcount += 1

	for d in jobinfo:
		# print d
		colcount = 0
		rowcount += 1
		for e in d:
			# print e
			ws.write(rowcount, colcount, e)
			# print colcount
			colcount +=1
			# print e
	# ws.write(rowcount,0, 'steazmonkey')

	wb.save(str(bin)+".xls")

	# CAN EITHER GENERATE NEW .xls FILES OR 
	# NEW SHEETS WITHIN A FILE - WHATEVER WORKS

# print output_to_excel(testbin)	



def agg_data(list_of_bins):
	for j in list_of_bins:
		output_to_excel(j)

print agg_data(list_of_bins)		


