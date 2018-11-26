#Import necessary modules
import csv
import time
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
import ast
import numpy as np
import pandas as pd
import sys
import dateutil
import Articulations as art


global commands
# User inputs
#_______________________________________________________________________________________________

#Creates GUI to initiate program with the proper files and specifications

#Finished File Name
output_filename = 'insert_name.csv'

#Rference Date
refdate_str = '01-01-2005'
refdate = datetime.strptime(refdate_str, '%m-%d-%Y')

#Date Step Size
time_step = '1A'

#DK is an array with all developer keys
global DK
DK = ['insert_key']
DKnum = 0
DKcount = 0
DKcheck = 0

#Collect Query Information
#Media Sites and Site Specific Commands
media_sites_file = 'insert_sites.csv'
global media_sites #dictionary which has keys that list media source names ie New York Times
media_sites = {} #dictionary of the web address (ie www.nytimes.com) per site key (ie New York Times)

#Each website has a unique way to store article information. To determine how to access that information, 
#run an independent Google CSE query and examine the underlying structure. An example of the desired codes.csv 
#file is in the Example_Script folder

commands = {} #set of site specific commands to be executed to extract information from articles in each site
#load in api specific code
with open(media_sites_file,'rb') as s:
    rdr = csv.reader(s)
    keys = next(rdr) #keys are column headers in the first row
    for row in rdr:
        if row[0] != 'ALL':
            media_sites[row[0]] = row[1] #First extract the websites to a dictionary
        commands[row[0]] = {}
        for key_num in range(2,len(row)):
            commands[row[0]][keys[key_num]] = row[key_num]

#Establish duplicate filter
title_store = {}
for sitek in media_sites:
    title_store[sitek] = []

'''
This searchword extraction method has been disabled and replaced by the GUI, to begin this again, remove triple 
quotes from here and place triple quotes around the search word extraction below (called "#Search Words").
Then go into Articulation.py and got to the input_files() command on line 503. Take out the commented sections 
(denoted by #). This will allow you to import a csv file with your search terms instead of typing them in.


#Search Words
siteswords_files = art.varf2.get()
searchwords = [] #list of search words to find in articles
#This establishes the words being searched for in an article, search for direct quote
with open(siteswords_files, 'rb') as s:
    rdr = csv.reader(s)
    next(rdr)
    for x in rdr:
        searchwords.append(x[1])

print searchwords
'''

#Search Words
searchwords = [''] #list of search words to find in articles
#This establishes the words being searched for in an article, search for direct quote

#Collect "or" Terms for each search
global orterms
or_count = 2 #number of or terms
orterms = {0:[''],1:'orterm'}

#Collect "incl" Terms for each search
incl_count = 0 #number of inclterms
inclterms = {0:'include_term'}

#_______________________________________________________________________________________________

#set up variable dateres, used to restrict search results to after a user-specified refernce date
today_str = '03-01-2006'
today = datetime.strptime(today_str, '%m-%d-%Y')
current_day = datetime.strptime(today_str, '%m-%d-%Y').day
daydelta = today - refdate
past = int(daydelta.days)
dateres = 'd%s' %(past)

#Set up date bins
global day_list
day_list = []
dates_range = pd.date_range(
    start=pd.Timestamp(refdate_str),
    end=pd.Timestamp(today)+pd.tseries.offsets.MonthEnd(),
    freq=u'M')#must enter a day from next month or last day of current month or else concatenates.

article_tally = {} # Dictionary of date bins that tallies the results by source
title_missed = [] # tracking articles that have associated dates which cannot be found
article_excluded = [] # tracking articles that have a date beyond the timeline 
global error
error = 0

#____________________________________________________________________________________________________________________________
# Get output of all media results for the time period
#____________________________________________________________________________________________________________________________

to_write = {}
for k in range(len(searchwords)): #for each searchword there is a new dictionary
    search = searchwords[k]
    # One data frame for each search, where each data frame has columns corresponding to sources and rows corresponding to dates
    article_tally[search] = pd.DataFrame(np.zeros((len(dates_range),len(media_sites.keys()))),index=dates_range, columns=media_sites.keys()) 
    to_write[search] = {}
    for n in range(len(media_sites.keys())): #for each site, creating a new dictionary
        row_num = 1
        site = media_sites[media_sites.keys()[n]]
        to_write[search][site] = {}
        total_time = 0
        dates = art.getdate(time_step,refdate_str) #set up the time windows (bins)
        for event_num in range(len(dates)-1): #event_num is the index of the time window
            start_time = time.time() #timer to see how long it takes to run
            start = str(dates[event_num]) #convert time series to string
            date_store = pd.to_datetime(start) #convert string to datetime, this is the first date in the time window
            end = str(dates[event_num + 1]-dateutil.relativedelta.relativedelta(days=1)) #remove first day of next window from time series e.g 1-1-05 tp 1-1-06 minut 1 day
            date_start = start[:4]+start[5:7]+start[8:10] #formatting the date to match the api format
            date_end = end[:4]+end[5:7]+end[8:10]
            date_start_track = date_start
            index = 1
            for orterm_specific in orterms[k]: #to get around formatting issues, include a blank tuple rather than an empty "orterm"
                if orterm_specific == '':
                    orterm_specific = ()
                while True:
                    rerun_val = 1
                    while rerun_val == 1:
                        global res
                        res,rerun_val,DKcount,DKcheck,DKnum,current_day = art.runquery(
                            DK,
                            media_sites[media_sites.keys()[n]],
                            searchwords[k],
                            index,
                            date_start,
                            date_end,
                            DKcount,
                            DKcheck,
                            DKnum,
                            current_day,
                            orterm_specific,
                            rerun_val,
                            inclterms)
                    n_res1 = res['queries']['request'][0]['count'] #first way to count results- results per query submission
                    n_res2 = int(res['queries']['request'][0]['totalResults']) #second way to count results- total results for query
                    if n_res1 > 0 and n_res2 > 0:
                        for num in range(n_res1):
                            row,article_excluded,title_missed,article_tally[search],error,title_store[media_sites.keys()[n]] = art.getinfo(
                                res,
                                day_list,
                                site,
                                search,
                                media_sites.keys(),
                                n,
                                num,
                                commands,
                                article_excluded,
                                title_missed,
                                article_tally[search],
                                error,
                                title_store[media_sites.keys()[n]],
                                orterm_specific)

                            to_write[search][site][row_num] = row 

                            #date check is addressing the limitations of Google CSE to only return 100 results within a time period.
                            #it is continually updating the "newest" article found. This may be used later if there are more than 100 results
                            #in a period to define a new time window until there are less than 100 articles in a period
                            date_check = row[3]
                            if type(date_check) == datetime:
                                if date_check > date_store and date_check < pd.to_datetime(end):
                                    date_store = date_check
                                    year_str = str(date_store.year)
                                    month_str =  str(date_store.month)
                                    if len(month_str) < 2:
                                        month_str = '0'+month_str
                                    day_str = str(date_store.day)
                                    if len(day_str) < 2:
                                        day_str = '0'+day_str
                                    date_store_str = year_str+month_str+day_str

                            row_num = row_num + 1              	
                    else:
                        break
                    if 'nextPage' not in res['queries'].keys(): #if there is no next page, end search
                        break

                    #If there is a next page, but the index is such that the data connot be retreived, due to the API's limitations, (meaning the 
                    #index value is greater than 91), then date_start gets a new value (its new value comes from sate_store_str found above). This
                    #creates a time window that is shorter than the previous, and thus finds additional articles that were missed.
                    else:
                        index = res['queries']['nextPage'][0]['startIndex'] 
                        if index > 91:
                            timing = time.time() - start_time
                            total_time += timing
                            print '%s (%s) results retrieved for keyword: "%s" and media source: "%s" and time: %s' % (index+n_res1-1, n_res2, search, site, timing)
                            print 'Total time code has been running: %s seconds' % (total_time)
                            print 'missing results, last day found: %s' %(date_store)
                            try:
                                date_start = date_store_str
                            except:
                                year_str = str(date_store.year)
                                month_str =  str(date_store.month)
                                if len(month_str) < 2:
                                    month_str = '0'+month_str
                                day_str = str(date_store.day)
                                if len(day_str) < 2:
                                    day_str = '0'+day_str
                                date_start = year_str+month_str+day_str

                            if date_start == date_start_track:
                                #convert string to datetime
                                date_start_del = datetime(
                                    year=int(date_start[0:4]),
                                    month=int(date_start[4:6]),
                                    day=int(date_start[6:8]))
                                #add one day
                                date_start_del = date_start_del+timedelta(days=1)
                                #convert datetime to string
                                date_start = str(date_start_del)[:4]+str(date_start_del)[5:7]+str(date_start_del)[8:10]

                            date_start_track = date_start
                            index = 1

                    if time.time() - start_time > 300:
                        print 'Request for results for %s to %s for keyword: "%s" and media source: "%s" timed out' %(refdate, today, search, site)
                        break
                timing = time.time() - start_time
                total_time += timing
                print '%s (%s) results retrieved for keyword: "%s" and media source: "%s" and time: %s' % (index+n_res1-1, n_res2, search, site, timing)
                print 'Total time code has been running: %s seconds' % (total_time)

    #create way to have same search with diff exclusions or orterms...
    article_tally[search]['Sum'] = (
        article_tally[search][article_tally[search].keys()[0:]].sum(1))
    article_tally[search].to_csv(''.join(search.split())+'_Dataframe_%s_%s%s%s.csv' %(output_filename,datetime.today().month,datetime.today().day,datetime.today().year))

with open(output_filename, 'wb') as fto:
    wtr = csv.writer(fto)
    wtr.writerow(['site','search','title','day','year','media_type','further_info'])
    for srkey in to_write.keys():
        for sikey in to_write[srkey].keys():
            for inkey in to_write[srkey][sikey].keys():
                wtr.writerow(to_write[srkey][sikey][inkey])
