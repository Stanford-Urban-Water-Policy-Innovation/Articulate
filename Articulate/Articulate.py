#Import necessary modules
import csv
import time
from datetime import datetime
from googleapiclient.discovery import build
import ast
import numpy as np
import pandas as pd
import sys
import dateutil
import Articulations as art

def articulate():
    
    # User inputs
    
    #Creates GUI to initiate program with the proper files and specifications
    #Returns var1, var2, and var3
    art.initiate()
    
    #Finished File Name
    output_filename = art.var1.get()
    
    #Rference Date
    refdate_str = art.var2.get()
    refdate = datetime.strptime(refdate_str, '%m-%d-%Y')
    
    #Date Step Size
    time_step = art.var3.get()
    
    
    
    #Input Developer Keys
    art.get_keys()
    
    #DK is an array with all developer keys
    DK = []
    for DK_key in art.var_dict.keys():
        DK.append(art.var_dict[DK_key].get())
    DKnum = 0
    DKcount = 0
    DKcheck = 0
    
    
    
    #Collect Query Information
    art.input_files()
    
    #Media Sites
    media_sites_file = art.varf1.get()
    media_sites = [] #list of the web address ie www.nytimes.com
    global sites_key
    sites_key = [] #list of media source names ie New York Times
    #First extract the websites to a list without other information
    with open(media_sites_file, 'rb') as s:
        rdr = csv.reader(s)
        next(rdr)
        for x in rdr:
            media_sites.append(x[1])
            sites_key.append(x[0])
    
    '''
    This seacrhword extraction method has been disabled, to begin this again, remove triple quotes
    from here and place triple quotes around the search word extraction below (called "#Search Words").
    Then go into Articulation.py and from the "inpit_files() command on line 438. Take out the commented
    sections. This will allow you to import a csv file with your seacrh terms.
    
    
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
    
    #Site Specific Commands
    code_file = art.varf3.get()
    commands = {} #set of site specific commands to be executed to extract information from articles in each site
    #load in api specific code
    with open(code_file,'rb') as s:
        rdr = csv.reader(s)
        for x in rdr:
            keys = x
            break
        for x in rdr:
            try:
                commands[keys[1]].append(x[1]) #'type'
                commands[keys[2]].append(x[2]) #'date'
                commands[keys[3]].append(x[3]) #'keyword'
                commands[keys[4]].append(x[4]) #'title'
                commands[keys[5]].append(x[5]) #'website'
                commands[keys[6]].append(x[6]) #'type2'
            except KeyError:
                commands[keys[1]] = ([x[1]]) #'type'
                commands[keys[2]] = ([x[2]]) #'date'
                commands[keys[3]] = ([x[3]]) #'keyword'
                commands[keys[4]] = ([x[4]]) #'title'
                commands[keys[5]] = ([x[5]]) #'website'
                commands[keys[6]] = ([x[6]]) #'type2'
    
    
    
    #Search Words
    art.search_terms()
    searchwords = [] #list of search words to find in articles
    #This establishes the words being searched for in an article, search for direct quote
    for term_key in art.var_wordstore.keys():
        if art.var_wordstore[term_key] != 0:
            searchwords.append(art.var_wordstore[term_key])
    
    
    
    #Collect "or" Terms for each search
    or_count = 0
    orterms = {}
    for search in searchwords:
        art.or_terms(search)
        ors_list = []
        for or_keys in art.var_orstore.keys():
            ors_list.append(art.var_orstore[or_keys])
        orterms[or_count] = tuple(ors_list)
        or_count += 1

    #Collect "incl" Terms for each search
    incl_count = 0
    inclterms = {}
    for search in searchwords:
        art.incl_terms(search)
        incl_list = []
        for incl_keys in art.var_inclstore.keys():
            incl_list.append(art.var_inclstore[incl_keys])
        inclterms[incl_count] = tuple(incl_list)
        incl_count += 1

    
    #set up variable dateres, used to restrict search results to after 1/1/2005
    today = datetime.now()
    current_day = datetime.now().day
    daydelta = today - refdate
    past = int(daydelta.days)
    dateres = 'd%s' %(past)
    
    #Set up variables
    global day_list
    day_list = []
    dates_range = pd.date_range(
        start=pd.Timestamp(refdate_str),
        end=pd.Timestamp(today)+pd.tseries.offsets.MonthEnd(),
        freq=u'M')#must enter a day from next month or last day of current month or else concatinates.
    article_tally = {}
    title_missed = []
    article_excluded = [] 
    error = 0
    
    excludeterms = {}
    excludeterms[0] = ''
    for term in searchwords:
        try:
            excludeterms[searchwords.index(term)+1] = ('%s','"%s"') % (excludeterms[searchwords.index(term)],term)
        except:
            excludeterms[searchwords.index(term)+1] = '"%s"' % (term)
    
    #____________________________________________________________________________________________________________________________
    # Get dump of all media results for the time period
    #____________________________________________________________________________________________________________________________
    
    
    to_write = {}
    for k in range(len(searchwords)): #for each searchword there is a new dictionary
        search = searchwords[k]
        article_tally[search] = pd.DataFrame(np.zeros((len(dates_range),len(sites_key))),index=dates_range, columns=sites_key)
        to_write[search] = {}
        for n in range(len(media_sites)): #for each site, creating a new dictionary
            row_num = 1
            site = media_sites[n]
            to_write[search][site] = {}
            total_time = 0
            dates = art.getdate(time_step,refdate_str)
            for event_num in range(len(dates)-1):
                start_time = time.time()
                start = str(dates[event_num])
                date_store = pd.to_datetime(start)
                end = str(dates[event_num + 1]-dateutil.relativedelta.relativedelta(days=1))
                date_start = start[:4]+start[5:7]+start[8:10]
                date_end = end[:4]+end[5:7]+end[8:10]
                index = 1
                while True:
                    rerun_val = 1
                    while rerun_val == 1:
                        global res
                        res,rerun_val,DKcount,DKcheck,DKnum,current_day = art.runquery(
                            DK,
                            media_sites[n],
                            searchwords[k],
                            index,
                            date_start,
                            date_end,
                            DKcount,
                            DKcheck,
                            DKnum,
                            current_day,
                            orterms[k],
                            excludeterms[k],
                            rerun_val,
                            inclterms[k])
                    n_res1 = res['queries']['request'][0]['count']
                    n_res2 = int(res['queries']['request'][0]['totalResults'])
                    if n_res1 > 0 and n_res2 > 0:
                        for num in range(n_res1):
                            row,article_excluded,title_missed,article_tally[search],error = art.getinfo(res,day_list,site,search,sites_key,n,num,commands,article_excluded,title_missed,article_tally[search],error)
                            to_write[search][site][row_num] = row 
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
                    if 'nextPage' not in res['queries'].keys():
                        break
                    else:
                        index = res['queries']['nextPage'][0]['startIndex']
                        if index > 91:
                            timing = time.time() - start_time
                            total_time += timing
                            print '%s (%s) results retrieved for keyword: "%s" and media source: "%s" and time: %s' % (index+n_res1-1, n_res2, search, site, timing)
                            print 'Total time code has been running: %s seconds' % (total_time)
                            print 'missing results, last day found: %s' %(row[3])
                            date_start = date_store_str
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
        article_tally[search].to_csv(''.join(search.split())+'_Dataframe.csv')
    
    with open(output_filename, 'wb') as fto:
        wtr = csv.writer(fto)
        wtr.writerow(['site','search','title','day','year','media_type','further_info'])
        for srkey in to_write.keys():
            for sikey in to_write[srkey].keys():
                for inkey in to_write[srkey][sikey].keys():
                    wtr.writerow(to_write[srkey][sikey][inkey])

if __name__ == '__main__':
    articulate()
