# imports incessary libarries

import requests
from bs4 import BeautifulSoup
import os
import urllib2
import itertools
import random
import urlparse
from optparse import OptionParser
import os.path
import re
import datetime
import threading
import schedule
import time
import sched
import os, os.path


# uses link_list to get email addresses
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\s[at]\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

def put_emails_in_list (lists, url, main_count):
        #for each link we grab out all of the emails and put them in email_list
    print "Starting to pull all of the links and examine them for email addresses"

    for link in lists:
        # print " "
        # print link
        email_list = []

        try:

            source_code = requests.get(link, timeout=200)
            print "got request"
            if len(source_code.content) > 100000:
                raise ValueError('Too large a response')
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text,  "html.parser")
    #    for link in soup.findAll(span',{"class": "about_text"}):
            soup = str(soup)
            all_emails_on_page = get_emails(soup, email_list)
            z = 0
            for x in all_emails_on_page:
                email_list.append(x)
                global file_number
                f = open('text_files/main_file' + str(file_number) + '.txt', 'a')
                f.write( '\n' + str(main_count) + ',' + x + ',' + str(datetime.datetime.now())   +  ','+ url + ',' + link)
                f.close()
                print "-------------------------------------"
                print str(z) + " adding " + x + " to email_list"
                print "-------------------------------------"
                z = z + 1

        except:
            print "beautiful soup failure"









def get_emails(s, email_list):
    """Returns an iterator of matched emails found in string s."""
    # Removing lines that start with '//' because the regular expression
    # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
    # return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))

    return (email[0] for email in re.findall(regex, s) if not email[0].startswith('//'))
    # for x in re.findall(regex, s):
    for x in re.findall("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)", s):
            email_list.append(x)
            print x
    for y in email_list:
        print y
    return email_list




def get_links(url):
    soup = None                                        # Beautiful Soup object
    current_page   = url         # Current page's address
    links          = []                             # Queue with every links fetched
    visited_links  = []
    link_list = []
    #i = 1

    #Set this number for the number of pages you will go through
    # to get more pages

    print "link getting process initialized"
#    print "counter = " + str(counter)
    print "opening " + current_page
    res = urllib2.urlopen(current_page)
    html_code = res.read()
    visited_links.append(current_page)
    soup = BeautifulSoup(html_code, "lxml")


        # try :
    for link in [h.get('href') for h in soup.find_all('a', { "class" : "jobtitle" })]:
        try:
            # print "Found link: '" + link + "'"
            if link.startswith('http'):
                links.append(link)
                # print "Adding link" + link + "\n"
            elif link.startswith('/'):
                parts = urlparse.urlparse(current_page)
                links.append(parts.scheme + '://' + parts.netloc + link)
                # print "Adding link " + parts.scheme + '://' + parts.netloc + link + "\n"
            else:
                links.append(current_page+link)
        #        print "Adding link " + self.current_page+link + "\n"

            # except Exception, ex: # Magnificent exception handling
            #     print ex

            # Update links
            #links = links.union( set(page_links) )

            # Choose a random url from non-visited set
            #current_page = random.sample( links.difference(visited_links),1)[0
            # Crawl 3 webpages (or stop if all url has been fetched)
            #while (visited_links == links):

            sett = set(links)
            result = sorted(list(sett))
            for link in result:
                link_list.append(link)
        except:
            print " failed this time!"

    return link_list
            # print link
        #print "email getting process complete"



def spider2():
    global spider_function
    spider_function = True
    global main_count
    link_list = []
    url = ""
    # put all of links we will use to grad email addresses from in the link_list list

    # url = 'http://www.' + url_part + '.com'
    url = 'https://www.indeed.ca/software-jobs-in-london'
    print url
    url_part = ""
    link_list = get_links(url)
    new_link_list = []
    zz = 0
    set_list = set(link_list)
    reduced_list = list(set_list)

    for x in reduced_list:
        match = re.search(r'^(.*?)(java)(.*)$', x)
        if match:
            print x + " will not be copied to new list"
        else:
            print x
            new_link_list.append(x)
        zz = zz + 1

    try:
        put_emails_in_list(new_link_list, url, main_count)

    except:
        "couldnt put the more emails in a list - beautiful soup error of some kind - moving on now"
    #print "you failed on the last step"
    #reset_lists()


    print ""
    print ""






def create_link_list(page_list):
    link_list = []
    for link in page_list:
        source_code = get_source_code(link)
        print "here 1111"
        for item in source_code.findAll('a', { "class" : "turnstileLink" }):
            href = item.get('href')
            if href.startswith('http'):
                job_page = get_source_code(href)
                link_list.append(href)
                print "exit"
                return "exit"
                # print "starts with http **************"
            elif href.startswith('/'):
                new_item = "https://www.indeed.ca" + href
                job_page = get_source_code(new_item)
                if job_page.findAll('a', { "class" : "save-job-link" }):
                    print "***** THIS IS AN INDEED PAGE ***** "
                    #below put code to past a resume and fill out the survey
                else:
                    print "NOT INDEED PAGE"
                # print new_item + "*****************************"






# indeed-apply-iframe-holder

def create_page_list(number_of_pages):
    i = 0
    list_of_links = []

    while i < number_of_pages:
        link = create_url(title_and_city[0], title_and_city[1], str(i * 20))
        list_of_links.append(link)
        i = i + 1
    print len(list_of_links)
    return list_of_links

def calculate_pages(number_of_jobs):
    return number_of_jobs / 20



def get_number_of_jobs_in_source_code(source_code):
    #this searches the page for a div with an id of "searchCount"
    div = str(source_code.find_all('div', { "id" : "searchCount" }))
    print div
    #this regex grabs all numbers above 30
    regex = r"([3-9][0-9]+|\d{3,})"
    #this uses the regex and the string provided with the div to
    #find a match. If there is a match, we take the string from the
    #match object and save it to a variable

    match = re.search(regex, div)
    if match:
        number = str(("{}".format(match.group(0))))
        print number
        return int(number)
    else:
        print "FAILED TO FIND A MATCH ------ INDEED HAS CHANGED SOMETHING!"



def get_source_code(url):
    print "opening " + url
    res = urllib2.urlopen(url)
    html_code = res.read()
    soup = BeautifulSoup(html_code, "lxml")
    return soup

def create_url(title, city, job_number):
    url = "https://www.indeed.ca/jobs?q=" + title +"&l=" + city + "&start=" + job_number
    return url

def get_title_and_city():
    title = "engineer"
    city = "toronto"
    # title = raw_input('Enter the position you want ')
    # city = raw_input('Enter the city to search in ')
    title_and_city = []
    title_and_city.append(title)
    title_and_city.append(city)
    return title_and_city

# This gets the title and city name from a user
title_and_city = get_title_and_city()

#create a url with the title and city name
url = create_url(title_and_city[0], title_and_city[1], "0")

#gets source code.... accepts a url as input
source_code = get_source_code(url)

# Search source code for number of jobs on page ----> returns integer
number_of_jobs = get_number_of_jobs_in_source_code(source_code)

#calculate how many pages there are (accepts number of jobs from search)
number_of_pages = calculate_pages(number_of_jobs)

# create a list of links based upon the number of pages and number of jobs
page_list = create_page_list(number_of_pages)

# Visit each link in the page_list and create a master list of links
link_list = create_link_list(page_list)
