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
from Tkinter import *

#Using the specified time step the total timeframe is divided into time steps
def getdate(time_step,refdate_str):
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

#The Developer Keys are monitored and exchanged if there is an error with one Developer Key
#If all Developer Keys have been used by the point, the code will reset to the first Key
#If the user would like to stop the program, they have the option at that point to exit
def DKtest(DKcount,DKcheck,DKnum,current_day,DK,rerun_val):
    if DKcheck == DKcount or DKcount >= 100:
        print 'Possible DKcount off, changed DKnum: CHECK:%s, COUNT:%s, NUM:%s' %(DKcheck,DKcount,DKnum)
        DKnum = DKnum + 1
        DKcount = 0
        DKcheck = 0
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
                    DKrun = 0
                    sys.exit()
                    print 'exiting'
                    sys.exit()
                else:
                    print 'Expected Error'
            current_day = datetime.now().day
        else:
            current_day = datetime.now().day
        DKcheck = DKcount
        print 'Switched DK'
        res = ['Must Rerun']
        print res[0]
        print 'rerun_val = %s' %(rerun_val)
        if rerun_val == 1:
            print 'Will rerun last query submission'
        else:
            print 'Did not rerun last query submission'
        return res,rerun_val,DKcount,DKcheck,DKnum,current_day
    else:
        res = ['must rerun']
        DKcheck = DKcount
        rerun_val = 1
        return res,rerun_val,DKcount,DKcheck,DKnum,current_day
    
#A query is submitted to the google cse api
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
    rerun_val,
    ):
    try:
        service = build("customsearch", "v1", developerKey=DK[DKnum])
        query = 'site:%s "%s"' %(media,search)
        res = service.cse().list(
            q = query,
            cx ='015907315053208763487:ihyujd_at7y',
            exactTerms = 'California',
            orTerms = orterms,
            excludeTerms = excludeterms,
            start = index,
            sort = 'date:a,date:r:%s:%s' %(date_start,date_end)
            ).execute()
        DKcount += 1
        rerun_val = 0
    except:
        res,rerun_val,DKcount,DKcheck,DKnum,current_day = DKtest(DKcount,DKcheck,DKnum,current_day,DK,rerun_val)
    return res,rerun_val,DKcount,DKcheck,DKnum,current_day

#media source specific code is used to extract and filter information from various sources
def getinfo(res,day_list,site,search,sites_key,n,index,commands,article_excluded,title_missed,article_tally,error):
    
    #Extract Type
    try:
        media_type = str(eval(commands['type'][n])) #adjust in excel for all three ways of extracting
    except:
        media_type = 'pass'
        error = error + 1

#_____________________________________________________________________________________    
    #Extract Title	
    try:
        title = eval(commands['title'][n]).encode('ascii','ignore')
    except KeyError:
        title = 'miss'
    
    #Extract Date
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
            if dataframe_index >= article_tally.index[0] and dataframe_index <= article_tally.index[-1]:
                current_val = article_tally.loc[dataframe_index][sites_key[n]]
                article_tally.set_value(dataframe_index,sites_key[n],current_val+1)
            else:
                day = 'Fell outside of range'
                year = 'NA'
                article_excluded.append(title)
        else:
            day = 'NA'
            year = 'NA'
            article_excluded.append(title)
        row = [site,search,title,day,year,media_type,res['items'][index]]
    else:
        title_missed.append(title)
        row = [site,search,title,'NA','NA',media_type,res['items'][index]]
    return row,article_excluded,title_missed,article_tally,error

#_____________________________________________________________________________________    


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
    b4 = Button(master, text='Next', width=20, command=master.destroy)
    
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
    #if len(varf1.get()) > 0 and len(varf2.get()) > 0 and len(varf3.get()) > 0:
    if len(varf1.get()) > 0 and len(varf3.get()) > 0:
        if varf1.get()[-4:] == '.csv':
            #if varf2.get()[-4:] == '.csv':
            if varf3.get()[-4:] == '.csv':
                while L4.winfo_ismapped() == True:
                    remove_label()
                b4.grid(row=3, column=1)
            else:
                remove_button
                L4.grid(row=3,column=1)
            #else:
                #remove_button
                #L4.grid
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
    Label(master, text='Site Specific Code File (format is in .csv ... ie codes.csv): ').grid(row=2, sticky=W)
    
    global e1
    #global e2
    global e3
    
    e1 = Entry(master)
    #e2 = Entry(master)
    e3 = Entry(master)

    e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    e1.insert(10,'mediasites2.csv')
    #e2.insert(10,'keywords.csv')
    e3.insert(10,'codes.csv')
    
    global varf1
    #global varf2
    global varf3
    
    varf1 = StringVar()
    #varf2 = StringVar()
    varf3 = StringVar()

    b1_text = 'Enter'
    #b2_text = 'Enter'
    b3_text = 'Enter'

    b1 = Button(master, text=b1_text, width=10, command=callback1f)
    b1.grid(row=0, column=2, padx=4, pady=2)
    #b2 = Button(master, text=b2_text, width=10, command=callback2f)
    #b2.grid(row=1, column=2, padx=4, pady=2)
    b3 = Button(master, text=b3_text, width=10, command=callback3f)
    b3.grid(row=2, column=2, padx=4, pady=2)
    
    global b4
    b4 = Button(master, text='Next', width=20, command=master.destroy)
    
    global L4
    L4 = Label(master, text='Cannot Run With Given Parameters')
    L4.grid(row=4,column=1)

    mainloop()

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
    b4 = Button(master, text='Run Articulate', width=20, command=master.destroy)
    b4.grid(row=2, column=1, padx=4, pady=2)

    mainloop()

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
