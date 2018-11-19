'''
Functions_For_Articulate
'''
import csv
import time
from datetime import datetime
from googleapiclient.discovery import build
import ast
import numpy as np
import pandas as pd
import sys
import dateutil
import urllib
import urllib2
from cookielib import CookieJar
from Tkinter import *

today_str = '03-01-2006'
current_day = datetime.strptime(today_str, '%m-%d-%Y').day
#Using the specified time step the total timeframe is divided into time steps
#The output is a formatted list of dates corresponding to each time window
def getdate(time_step,refdate_str):
    ref = pd.Timestamp(refdate_str)
    today_str = '03-01-2006'
    today = datetime.strptime(today_str, '%m-%d-%Y')
    date_step = pd.date_range(
        start=ref,
        end=today)
    #resampling to time window. 
    dateseries = pd.Series(range(len(date_step)),date_step).resample(time_step).mean()
    dates2adj = dateseries.index
    dates2usem = dates2adj.shift(
        int((ref-dates2adj[0]).days),
        freq=pd.datetools.day)
    if dates2usem[-1] != today:
        dates2use = dates2usem.append((pd.DatetimeIndex([today])))
    else:
        dates2use = dates2usem
    return dates2use

#The Developer Keys are monitored and exchanged if there is an error with one Developer Key
#If all Developer Keys have been used by the point, the code will reset to the first Key
#If the user would like to stop the program, they have the option at that point to exit
#DKcount is the number of queries that have been used for that DK for that run (not for that day)
#DKcheck is the count before the latest query submission
#DKnum is the total umber of DKs that the user has entered/has available
#rerun_val is binary- 1 means rerun the query, 0 means continue
def DKtest(DKcount,DKcheck,DKnum,current_day,DK,rerun_val):
    if DKcheck == DKcount or DKcount >= 10000:
        print 'Possible DKcount off, changed DKnum: CHECK:%s, COUNT:%s, NUM:%s' %(DKcheck,DKcount,DKnum)
        DKnum = DKnum + 1 #go to next DK
        DKcount = 0 #reset count
        DKcheck = 0 #reset check
        if DKnum >= len(DK): #if trying to go beyond number you actually have
            DKrun = 1
            DKnum_holder = len(DK)
            while DKrun == 1:
                DKnum_holder = input('Set DK back to 0 or "Exit":')
                print DKnum_holder
                if DKnum_holder < len(DK) and DKnum_holder >= 0:
                    DKrun = 0
                    print 'DKnum has been reset to %s' %(DKnum_holder)
                    DKnum = int(DKnum_holder)
                    while datetime.now().day == current_day: #while today is still today
                        print 'still waiting'
                        time.sleep(300) #sleep for 300 seconds and then try again
                elif DKnum_holder == 'Exit': #if you dont want to wait for developer keys to reset, type "Exit"
                    DKrun = 0
                    sys.exit()
                    print 'exiting'
                    sys.exit()
                else:
                    print 'Expected Error'
        today_str = '03-01-2006'
        current_day = datetime.strptime(today_str, '%m-%d-%Y').day
        DKcheck = DKcount
        print 'Switched DK to %s' %(DK[DKnum])
        res = ['Must Rerun']
        print res[0]
        print 'rerun_val = %s' %(rerun_val)
        if rerun_val == 1:
            print 'Will rerun last query submission' #if there was an error but it's not due to DK count = 10,000
        else:
            print 'Did not rerun last query submission' #if there was error due to DK count = 10,000
        return res,rerun_val,DKcount,DKcheck,DKnum,current_day
    else: # denotes that it has errored once and will check again
        res = ['must rerun']
        DKcheck = DKcount
        rerun_val = 1
        return res,rerun_val,DKcount,DKcheck,DKnum,current_day
    
#A query is submitted to the google cse api
def runquery(
    DK,
    media,
    search,
    index, #the search index. I.e. the first result of page 2 of the search is index 11. Cannot exceed 92
    date_start,
    date_end,
    DKcount,
    DKcheck,
    DKnum,
    current_day,
    orterms,
    rerun_val,
    inclterms,
    ):
    try:
        service = build("customsearch", "v1", developerKey=DK[DKnum])
        query = 'site:%s "%s"' %(media,search)
        res = service.cse().list(
            q = query,
            cx ='015907315053208763487:ihyujd_at7y',
            exactTerms = inclterms, # Identifies a phrase that all documents in the search results must contain.
            orTerms = orterms, # Provides additional search terms to check for in a document, where each document in the search results must contain at least one of the additional search terms.
            start = index,
            sort = 'date:a,date:r:%s:%s' %(date_start,date_end)
            ).execute()
        DKcount += 1
        rerun_val = 0 #If it works, it doesn't rerun
    except: #if it doesn't work, it runs DKtest
        res,rerun_val,DKcount,DKcheck,DKnum,current_day = DKtest(DKcount,DKcheck,DKnum,current_day,DK,rerun_val)
    return res,rerun_val,DKcount,DKcheck,DKnum,current_day


#media source specific code is used to extract and filter information from various sources. n is the site index
def getinfo(
    res,
    day_list,
    site,
    search,
    sites_key,
    n,
    index,
    commands,
    article_excluded,
    title_missed,
    article_tally,
    error,
    title_store,
    orterm):    
    
    #Extract Type
    try:
        media_type = str(eval(commands[sites_key[n]]['type'])) #adjust in excel for all three ways of extracting.
    except:
        media_type = 'pass'
        error = error + 1
    
    if media_type == 'article':
        try:
            media_type2 = str(eval(commands[sites_key[n]]['type2']))
        except:
            media_type2 = media_type
            
        if media_type != media_type2:
            media_type = 'pass2'
            error = error + 1
    else:
        try:
            media_type = str(eval(commands[sites_key[n]]['type2']))
        except:
            media_type = 'pass1'
    
    
    #this section formats search variable to remove the quotation marks around the search terms IF necessary (i.e. Press Democrat newspaper)
    temp_search = search
    global new_search
    new_search = ''
    while '"' in search:
        print new_search
        if temp_search[0] != '"': 
            new_search+temp_search[0]
            temp_search = temp_search[1:]
        else:
            temp_search = temp_search[1:]
        search = new_search
    
    
    #false reporting errors 1 and 2 indicate that the search terms were not found in the article despite being pulled by CSE
    if media_type == 'article':
        
        if orterm == ():
            orterm = search
        
        try:
            link = [str(eval(commands[sites_key[n]]['keyword']))]
        except:
            link = ['none']
        
        try:
            link.append(str(eval(commands[sites_key[n]]['keyword2'])))
        except:
            link.append('none')
        
        url_count = 0
        while url_count < len(link):
            url_str = link[url_count]

            if url_str != 'none':
                try:
                    wbsite_toread = urllib.urlopen(url_str)
                    wbsite = wbsite_toread.read()
                    if len(wbsite) < len(search):
                        sys.exit()
                except:
                    try:
                        cj = CookieJar()
                        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                        wbsite = opener.open(url_str).read()
                    except:
                        wbsite = search+' - '+url_str
                        media_type = 'article_unchecked'
                
                if (search in wbsite and orterm in wbsite) or (search.lower() in wbsite and orterm.lower() in wbsite):
                    media_type = 'article'
                    break
                else:
                    media_type = 'false_reporting'+str(url_count+1)
            url_count += 1

                    
    #Extract Title
    try:
        title = eval(commands[sites_key[n]]['title']).encode('ascii','ignore')
    except KeyError:
        print 'Title missed: %s' %(commands[sites_key[n]]['title'])
        title = 'miss'
    
    if title in title_store and title != 'miss':
        title = 'duplicate - ' + title

    #Extract Date
    date_commands = commands[sites_key[n]]['date'].split(', ')
    try:
        date = eval(date_commands[0][1:])
        
        try:
            day = eval(date_commands[1][:-1])
            year = day.year
        except:
            day = 'NA_try_again1'
            year = 'NA_try_again1'
            
    except:
        date = 'NA_try_again2'
        day = 'NA_try_again2'
        year = 'NA_try_again2'
    
    if type(day) != datetime:
        if 'NA_try_again' in day:
            date_commands = commands['ALL']['date'].split(', ') #the -1 denotes the last row of the site specific code csv which has a list of defaults
            try:
                date = eval(date_commands[0][1:])
                
                try:
                    day = eval(date_commands[1][:-1])
                    year = day.year
                except:
                    day = date
                    year = 'Not yet found2' #not yet found means that we can't convert the date to datetime
                                    
            except:
                if day == 'NA_try_again1':
                    day = date
                    year = 'Not yet found1'
                else: #if none of the date extraction techniques have worked
                    date = 'NA'
                    day = 'NA'
                    year = 'NA'
    
    if (date != 'NA') and (title != 'miss') and (title[:9] != 'duplicate') and ('article' in media_type):
        
        if day != date and day < datetime.now():
            day_list.append(day)
            year = day.year
            dataframe_index = day+pd.tseries.offsets.MonthEnd() #if you want daily, weekly, or yearly look up pandas date offset notation
            if dataframe_index >= article_tally.index[0] and dataframe_index <= article_tally.index[-1]: 
                current_val = article_tally.loc[dataframe_index][sites_key[n]] #
                print 'current tally is: %s for %s month' %(current_val+1,dataframe_index)
                article_tally.set_value(dataframe_index,sites_key[n],current_val+1) #tally articles
                title_store.append(title)
            else:
                day = 'Fell outside of range'
                year = 'NA_out'
                article_excluded.append(title)
        else:
            day = 'NA2'
            year = 'NA2'
            article_excluded.append(title)
        
        row = [site,search,title,day,year,media_type,res['items'][index]] #building the database output file
    
    else:
        title_missed.append(title)
        row = [site,search,title,day,year,media_type,res['items'][index]]
    return row,article_excluded,title_missed,article_tally,error,title_store  


def remove_button():
    try:
        b4.grid_forget()
    except:
        None

def remove_label():
    try:
        L4.grid_forget()
    except:
        None

def label_check():
    if len(var1.get()) > 0 and len(var2.get()) > 0 and len(var3.get()) > 0:
        if var1.get()[-4:] == '.csv':
            if len(var2.get()) >= 6:
                if var2.get()[2] == '-' and var2.get()[5] == '-' and len(var2.get()) == 10:
                    if var3.get()[-1] in ['D','A','M']:
                        while L4.winfo_ismapped() == True:
                            remove_label()
                        b4.grid(row=3, column=1)
                    else:
                        remove_button	
                        L4.grid(row=3,column=1)
                else:
                    remove_button
                    L4.grid(row=3,column=1)
        else:
            remove_button
            L4.grid(row=3,column=1)
    else:
        remove_button
        L4.grid(row=3,column=1)

def callback1():
    print 'Entered "%s"' %(e1.get())
    var1.set(e1.get())
    e1.grid_forget()
    L1 = Label(master, text=var1.get())
    L1.grid(row=0,column=1)
    label_check()

def callback2():
    print 'Entered "%s"' %(e2.get())
    var2.set(e2.get())
    e2.grid_forget()
    L2 = Label(master, text=var2.get())
    L2.grid(row=1,column=1)
    label_check()

def callback3():
    print 'Entered "%s"' %(e3.get())
    var3.set(e3.get())
    e3.grid_forget()
    L3 = Label(master, text=var3.get())
    L3.grid(row=2,column=1)
    label_check()

def initiate():
    
    global master
    
    master = Tk()

    Label(master, text='Output File Name (format is in .csv ... ie media_results.csv): ').grid(row=0, sticky=W)
    Label(master, text='Reference Date (format is mm-dd-yyyy ... ie 01-01-2005): ').grid(row=1, sticky=W)
    Label(master, text='Time Step Size (format is integer AND A[year(s)], M[month(s)], or D[day(s)] ie 30D): ').grid(row=2, sticky=W)
    
    global pass_val
    pass_val = 0
    
    global e1
    global e2
    global e3
    
    e1 = Entry(master)
    e2 = Entry(master)
    e3 = Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    e1.insert(10,'media_results.csv')
    e2.insert(10,'01-01-2005')
    e3.insert(10,'30D')
    
    global var1
    global var2
    global var3
    
    var1 = StringVar()
    var2 = StringVar()
    var3 = StringVar()

    b1_text = 'Enter'
    b2_text = 'Enter'
    b3_text = 'Enter'

    b1 = Button(master, text=b1_text, width=10, command=callback1)
    b1.grid(row=0, column=2, padx=4, pady=2)
    b2 = Button(master, text=b2_text, width=10, command=callback2)
    b2.grid(row=1, column=2, padx=4, pady=2)
    b3 = Button(master, text=b3_text, width=10, command=callback3)
    b3.grid(row=2, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Enter All and Continue', width=20, command=master.destroy)
    
    global L4
    L4 = Label(master, text='Cannot Run With Given Parameters')
    L4.grid(row=3,column=1)

    mainloop()

def label_check_keys():
    if type(var1.get()) is int:
        while L4.winfo_ismapped() == True:
            remove_label()
        b4.grid(row=3, column=1)
        global yes
        yes = 1
    else:
        yes = 0
        remove_button
        L4.grid(row=3,column=1)

def callback1keys():
    print 'Entered "%s"' %(e1.get())
    var1.set(e1.get())
    e1.grid_forget()
    L1 = Label(master, text=var1.get())
    L1.grid(row=0,column=1)
    label_check_keys()
    
def devkey():
    global lab2
    if lab2.winfo_ismapped() == True:
        lab2.destroy()
    var_dict[rowx] = StringVar()
    var_dict[rowx].set(ent.get())
    print 'Entered "%s"' %(var_dict[rowx].get())
    lab2 = Label(master2, text='Developer Key Entered: %s' %(var_dict[rowx].get()))
    lab2.grid(row=rowx+1,column=1)
    b4.grid(row=rowx+2,column=1)

def get_keys():
    
    global master
    
    master = Tk()

    Label(master, text='Number of Developer Keys you wish to input: ').grid(row=0, sticky=W)
    
    global e1
    e1 = Entry(master)
    e1.grid(row=0, column=1)
    e1.insert(10,'1')
    
    global var1
    var1 = IntVar()

    b1_text = 'Enter'
    b1 = Button(master, text=b1_text, width=10, command=callback1keys)
    b1.grid(row=0, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Next', width=20, command=master.destroy)

    global L4
    L4 = Label(master, text='Cannot Run With Given Parameters')
    L4.grid(row=3,column=1)
    
    global yes
    yes = 0

    mainloop()
    
    if yes == 1:
        
        global but
        but = {}
        global var_dict
        var_dict = {}
        
        global rowx
        for rowx in range(var1.get()):
            
            global master2
            master2 = Tk()
            
            if rowx+1 != var1.get():
                b4 = Button(master2, text='Next', width=20, command=master2.destroy)
            else:
                b4 = Button(master2, text='Enter', width=20, command=master2.destroy)
            
            lab = Label(master2, text='Developer Key %s' %(rowx+1) )
            lab.grid(row=rowx,column=0)
            
            global lab2
            lab2 = Label(master2, text='Developer Key Entered:')
            lab2.grid(row=rowx+1,column=1)
            
            global ent
            ent = Entry(master2)
            ent.grid(row=rowx,column=1)
            
            but[rowx] = Button(master2, text='Enter Developer Key %s' %(rowx+1), command=lambda: devkey())
            but[rowx].grid(row=rowx,column=2)
        
            mainloop()
            
def label_checkf():
    if len(varf1.get()) > 0:
        if varf1.get()[-4:] == '.csv':
            while L4.winfo_ismapped() == True:
                remove_label()
            b4.grid(row=3, column=1)
        else:
            remove_button
            L4.grid(row=3,column=1)
    else:
        remove_button
        L4.grid(row=3,column=1)

def callback1f():
    print 'Entered "%s"' %(e1.get())
    varf1.set(e1.get())
    e1.grid_forget()
    L1 = Label(master, text=varf1.get())
    L1.grid(row=0,column=1)
    label_checkf()

def callback2f():
    print 'Entered "%s"' %(e2.get())
    varf2.set(e2.get())
    e2.grid_forget()
    L2 = Label(master, text=varf2.get())
    L2.grid(row=1,column=1)
    label_checkf()

def callback3f():
    print 'Entered "%s"' %(e3.get())
    varf3.set(e3.get())
    e3.grid_forget()
    L3 = Label(master, text=varf3.get())
    L3.grid(row=2,column=1)
    label_checkf()

def input_files():
    global master
    master = Tk()

    Label(master, text='Media Sites File (format is in .csv ... ie mediasites2.csv): ').grid(row=0, sticky=W)
    #Label(master, text='Keywords File (format is in .csv ... ie keywords.csv): ').grid(row=1, sticky=W)
    
    global e1
    #global e2
    
    e1 = Entry(master)
    #e2 = Entry(master)

    e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    
    global varf1
    #global varf2
    
    varf1 = StringVar()
    #varf2 = StringVar()

    b1_text = 'Enter'
    #b2_text = 'Enter'

    b1 = Button(master, text=b1_text, width=10, command=callback1f)
    b1.grid(row=0, column=2, padx=4, pady=2)
    #b2 = Button(master, text=b2_text, width=10, command=callback2f)
    #b2.grid(row=1, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Enter All and Continue', width=20, command=master.destroy)
    
    global L4
    L4 = Label(master, text='Cannot Run With Given Parameters')
    L4.grid(row=4,column=1)

    mainloop()

#________________________________________________________

def storevar():
    for num in c_dict.keys():
        if val[num].get() == 1:
            var_orstore[num] = var_ordict[num].get()
        else:
            var_orstore[num] = 0

def callback1or():
    counter = lcounter[-1]

    print 'Entered "%s"' %(e1.get())
    val[counter] = IntVar()
    var_ordict[counter] = StringVar()
    var_ordict[counter].set(e1.get())
    c_dict[counter] = Checkbutton(master, text=var_ordict[counter].get(), variable=val[counter], command=storevar)
    c_dict[counter].grid(row=counter+2,column=1)
    b4.grid_forget()
    b4.grid(row=counter+3, column=1, padx=4, pady=2)

    counter += 1
    lcounter.append(counter)

def or_terms(search):
    global master
    master = Tk()
    
    Label(master, text='For %s' %search).grid(row=0, sticky=W)
    Label(master, text='Input "Or" Terms (If you want it as a quote it must have quotation marks) ie "Articulate Software": ').grid(row=1, sticky=W)
    
    global e1
    e1 = Entry(master)
    e1.grid(row=1, column=1)
    
    global lcounter
    global var_ordict
    global var_orstore
    global c_dict
    global val
    
    lcounter = [0]
    var_ordict = {}
    var_orstore = {}
    c_dict = {}
    val = {}

    b1_text = 'Enter'
    b1 = Button(master, text=b1_text, width=10, command=callback1or)
    b1.grid(row=1, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Next', width=20, command=master.destroy)
    b4.grid(row=2, column=1, padx=4, pady=2)

    mainloop()

#________________________________________________________

def storewords():
    for num in c_dict.keys():
        if val[num].get() == 1:
            var_wordstore[num] = var_worddict[num].get()
        else:
            var_wordstore[num] = 0

def callback1words():
    counter = lcounter[-1]

    print 'Entered "%s"' %(e1.get())
    val[counter] = IntVar()
    var_worddict[counter] = StringVar()
    var_worddict[counter].set(e1.get())
    c_dict[counter] = Checkbutton(master, text=var_worddict[counter].get(), variable=val[counter], command=storewords)
    c_dict[counter].grid(row=counter+1,column=1)
    b4.grid_forget()
    b4.grid(row=counter+2, column=1, padx=4, pady=2)

    counter += 1
    lcounter.append(counter)

def search_terms():
    global master
    master = Tk()

    Label(master, text='Input Search Terms: ').grid(row=0, sticky=W)
    
    global e1
    e1 = Entry(master)
    e1.grid(row=0, column=1)
    
    global lcounter
    global var_worddict
    global var_wordstore
    global c_dict
    global val
    
    lcounter = [0]
    var_worddict = {}
    var_wordstore = {}
    c_dict = {}
    val = {}

    b1_text = 'Enter'
    b1 = Button(master, text=b1_text, width=10, command=callback1words)
    b1.grid(row=0, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Next', width=20, command=master.destroy)
    b4.grid(row=1, column=1, padx=4, pady=2)

    mainloop()

#___________________________________________________________________________

def storevarincl():
    for num in c_dict.keys():
        if val[num].get() == 1:
            var_inclstore[num] = var_incldict[num].get()
        else:
            var_inclstore[num] = 0

def callback1incl():
    counter = lcounter[-1]

    print 'Entered "%s"' %(e1.get())
    val[counter] = IntVar()
    var_incldict[counter] = StringVar()
    var_incldict[counter].set(e1.get())
    c_dict[counter] = Checkbutton(master, text=var_incldict[counter].get(), variable=val[counter], command=storevarincl)
    c_dict[counter].grid(row=counter+2,column=1)
    b4.grid_forget()
    b4.grid(row=counter+3, column=1, padx=4, pady=2)

    counter += 1
    lcounter.append(counter)

def incl_terms(search):
    global master
    master = Tk()
    
    Label(master, text='For %s' %search).grid(row=0, sticky=W)
    Label(master, text='Input "Include" Terms (If you want it as a quote it must have quotation marks) ie "Articulate Software": ').grid(row=1, sticky=W)
    
    global e1
    e1 = Entry(master)
    e1.grid(row=1, column=1)
    
    global lcounter
    global var_incldict
    global var_inclstore
    global c_dict
    global val
    
    lcounter = [0]
    var_incldict = {}
    var_inclstore = {}
    c_dict = {}
    val = {}

    b1_text = 'Enter'
    b1 = Button(master, text=b1_text, width=10, command=callback1incl)
    b1.grid(row=1, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Next', width=20, command=master.destroy)
    b4.grid(row=2, column=1, padx=4, pady=2)

    mainloop()
