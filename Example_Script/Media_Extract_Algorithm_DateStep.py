'''
Try a time bracketed approach (or a time sorting approach)
Also, fix your problems! (Source API specific)
'''

#California Drought and Water Consumption (California)

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


#_______________________________________________ _____________________________________________________________________________
# Establish Functions
#____________________________________________________________________________________________________________________________

def exitquery(exit_val):
    if exit_val == 1:
        print 'exiting'
        sys.exit()

#Change! (refday,endday,steptime)
def getdate(time_step):
    ref = pd.Timestamp(refdate_str)
    today = pd.Timestamp(datetime.now())
    date_step = pd.date_range(
        start=ref,
        end=today,
        freq=time_step[-1])
    dateseries = pd.Series(range(len(date_step)),
        date_step).resample(time_step).mean()
    dates2adj = dateseries.index
    dates2use = dates2adj.shift(
        int((ref-dates2adj[0]).days),
        freq=pd.datetools.day)
    return dates2use

def DKtest(DKcount,DKcheck,DKnum,current_day):
    if DKcheck == DKcount or DKcount > 99:
        print 'Possible DKcount off, changed DKnum: CHECK:%s, COUNT:%s, NUM:%s' %(DKcheck,DKcount,DKnum)
        DKnum = DKnum + 1
        DKcount = 0
        DKcheck = 0
        exit_val = 0
        if DKnum >= len(DK):
            DKrun = 1
            DKnum_holder = len(DK)
            while DKrun == 1:
                DKnum_holder = input('Set DK back to 0:')
                print DKnum_holder
                if DKnum_holder < len(DK) and DKnum_holder >= 0:
                    DKrun = 0
                    print 'DKnum has been reset to %s' %(DKnum_holder)
                    DKnum = int(DKnum_holder)
                    while datetime.now().day == current_day:
                        print 'still waiting'
                        time.sleep(300) #sleep for 300 seconds
                elif DKnum_holder == 'Exit':
                    print '... Correctly Input'
                    print 'Exiting'
                    DKrun = 0
                    exit_val = 1
                    sys.exit()
                else:
                    print 'Error: Retry'
            current_day = datetime.now().day
        else:
            current_day = datetime.now().day
        DKcheck = DKcount
        print 'Switched DK'
        res = ['Must Rerun']
        print res[0]
        if exit_val == 0:
            rerun_val = 1
        else:
            rerun_val = 0
        print 'exit_val = %s' %(exit_val)
        print 'rerun_val = %s' %(rerun_val)
        return exit_val,res,rerun_val,DKcount,DKcheck,DKnum,current_day
    else:
        exit_val = 0
        res = ['must rerun']
        DKcheck = DKcount
        rerun_val = 1
        return exit_val,res,rerun_val,DKcount,DKcheck,DKnum,current_day
    

def runquery(
    DK,
    media,
    search,
    index,
    date_start,
    date_end,
    DKcount,
    DKcheck,
    DKnum,
    current_day,
    orterms,
    excludeterms,
    ):
    try:
        service = build("customsearch", "v1", developerKey=DK)
        query = 'site:%s "%s"' %(media,search)
        res = service.cse().list(
            q = query,
            cx ='015907315053208763487:ihyujd_at7y',
            orTerms = orterms,
            excludeTerms = excludeterms,
            start = index,
            sort = 'date:a,date:r:%s:%s' %(date_start,date_end)
            ).execute()
        DKcount += 1
        rerun_val = 0
        exit_val = 0
    except:
        exit_val,res,rerun_val,DKcount,DKcheck,DKnum,current_day = DKtest(DKcount,DKcheck,DKnum,current_day)
    return exit_val,res,rerun_val,DKcount,DKcheck,DKnum,current_day

def getinfo(n,index,commands,article_excluded,title_missed,article_tally,error):
    try:
        media_type = str(eval(commands['type'][n])) #adjust in excel for all three ways of extracting
    except:
        media_type = 'pass'
        error = error + 1	
    try:
        title = eval(commands['title'][n]).encode('ascii','ignore')
    except KeyError:
        title = 'miss'
    if media_type != 'pass' and title != 'miss':
        date_commands = commands['date'][n].split(', ')
        try:
            date = eval(date_commands[0][1:])
        except:
            try:
                date_commands = commands['date'][10].split(', ')
                date = eval(date_commands[0][1:])
            except:
                date = 'NA'
        if date != 'NA':
            try:
                day = eval(date_commands[1][:-1])
            except:
                day = date
                year = 'Not Yet Found'
                article_excluded.append(title)
            if day != date and day < datetime.now():
                day_list.append(day)
                year = day.year
                dataframe_index = day+pd.tseries.offsets.MonthEnd()
                if dataframe_index > article_tally.index[0] and dataframe_index < article_tally.index[-1]:
                    current_val = article_tally.loc[dataframe_index][sites_key[n]]
                    article_tally.set_value(
                        dataframe_index,
                        sites_key[n],
                        current_val+1)
                else:
                    day = 'Fell outside of range'
                    year = 'NA'
                    article_excluded.append(title)
        else:
            day = 'NA'
            year = 'NA'
            article_excluded.append(title)
        row = [site,
            search,
            title,
            day,
            year,
            media_type,
            res['items'][index]['pagemap']['metatags'][0]]
    else:
        title_missed.append(title)
        row = [site,
            search,
            title,
            'NA',
            'NA',
            'NA',
            'NA']
    return row,article_excluded,title_missed,article_tally,error








# User inputs
#____________________________________________________________________________________________________________________________
output_filename = input('What file name is your output? (format is string ending in .csv ... ie "media_results.csv"): ') #answer: 'media_results.csv'
refdate_str = input('From what day is your reference? (format is string in mm-dd-yyyy ... ie "01-01-2005"): ') #answer: '01-01-2005'
time_step = input('What time step? (format is string of integer and A(year), M(month), or D(day) ie "30D"): ') #answer 'M6'
refdate = datetime.strptime(refdate_str, '%m-%d-%Y')

#____________________________________________________________________________________________________________________________

media_sites = [] #list of the web address ie www.nytimes.com
sites_key = [] #list of media source names ie New York Times
searchwords = []
commands = {}
error = 0

xmonth = []
media_byphrase_month_in = {}
media_byphrase_month_ex = {}
miss = 0
itval = 1

#DK is an array with all developer keys
DK = ['Input your own']
DKnum = 0
DKcount = 0
DKcheck = 0

#First extract the websites to a list without other information
with open('mediasites2.csv', 'rb') as s:
    rdr = csv.reader(s)
    next(rdr)
    for x in rdr:
        media_sites.append(x[1])
        sites_key.append(x[0])

#media_sites = ['http://www.nytimes.com/']
#sites_key = ['nytimes']

#This establishes the words being searched for in an article
with open('keywords4.csv', 'rb') as s:
    rdr = csv.reader(s)
    next(rdr)
    for x in rdr:
        searchwords.append(x[1])

#searchwords = ['California Drought']

#load in api specific code
with open('codes.csv','rb') as s:
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

excludeterms = {}
excludeterms[0] = ''
for term in searchwords:
    try:
        excludeterms[searchwords.index(term)+1] = ('%s','"%s"') % (excludeterms[searchwords.index(term)],term)
    except:
        excludeterms[searchwords.index(term)+1] = '"%s"' % (term)
	
ors = '"water conservation"','rainfall','snowpack','climate','weather','aqueducts','reservoirs','aqueduct','reservoir','"rain and snow"','"snow and rain"','conservation','"Jerry Brown"'
orterms = {0:'',1:'',2:'',3:'',4:ors,5:ors}

#set up variable dateres, used to restrict search results to after 1/1/2005
today = datetime.now()
current_day = datetime.now().day
daydelta = today - refdate
past = int(daydelta.days)
dateres = 'd%s' %(past)

#for testing purposes
day_list = []
dates_range = pd.date_range(
    start=pd.Timestamp(refdate_str),
    end=pd.Timestamp(today)+pd.tseries.offsets.MonthEnd(),
    freq=u'M')#must enter a day from next month or last day of current month or else concatinates.
article_tally = {}
title_missed = []
article_excluded = []    

#____________________________________________________________________________________________________________________________
# Get dump of all media results for the time period
#____________________________________________________________________________________________________________________________

exit_val = 0

if __name__ == "__main__":
    exitquery(exit_val)
    to_write = {}
    for k in range(len(searchwords)): #for each searchword there is a new dictionary
        exitquery(exit_val)
        search = searchwords[k]
        article_tally[search] = pd.DataFrame(np.zeros((len(dates_range),len(sites_key))),index=dates_range, columns=sites_key)
        to_write[search] = {}
        for n in range(len(media_sites)): #for each site, creating a new dictionary
            row_num = 1
            exitquery(exit_val)
            site = media_sites[n]
            to_write[search][site] = {}
            total_time = 0
            dates = getdate(time_step)
            for event_num in range(len(dates)-1):
                exitquery(exit_val)
                start_time = time.time()
                start = str(dates[event_num])
                date_store = pd.to_datetime(start)
                end = str(dates[event_num + 1]-dateutil.relativedelta.relativedelta(days=1))
                date_start = start[:4]+start[5:7]+start[8:10]
                date_end = end[:4]+end[5:7]+end[8:10]
                index = 1
                while True:
                    exitquery(exit_val)
                    rerun_val = 1
                    while rerun_val == 1:
                        exit_val,res,rerun_val,DKcount,DKcheck,DKnum,current_day = runquery(
                            DK[DKnum],
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
                            excludeterms[k])
                    exitquery(exit_val)
                    n_res1 = res['queries']['request'][0]['count']
                    n_res2 = int(res['queries']['request'][0]['totalResults'])
                    if n_res1 > 0 and n_res2 > 0:
                        for num in range(n_res1):
                            row,article_excluded,title_missed,article_tally[search],error = getinfo(n,num,commands,article_excluded,title_missed,article_tally[search],error)
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
