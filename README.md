# Articulate
A search tool for quantifying news media coverage

## Introduction

News media plays an important role shaping public opinion and attitudes. However, current proprietary databases used for media investigation can be expensive, rigid, and limited in scope. To address these challenges, we developed Articulate, an open-source, flexible tool for discovering, compiling, and quantifying newspaper coverage on a user-specified topic. Articulate is written in Python and interfaces with Google Custom Search Engine (CSE) API to allow the user to extract, classify, represent, and store information from various media sources in a functional database. Articulate offers equal and sometimes greater data coverage than produced by comparable proprietary databases. 


## Table of Contents    
1.	Installation
2.	Usage  
    (i) Background  
    (ii) Software Inputs  
    (iii) Software Outputs  
    (iv) Set up  
    (v) GitHub Repository and Executing Articulate     
     * via the GUI  
     * via the script  
3.  Limitaions    
4.	Contributing
6.	Credits
7.	License
8.  Contact


## 1. Installation    

The software environment used by this program is Python version 2.7 with the following modules:  csv.py, time.py, datetime.py, googleapiclient.discovery.py, ast.py, numpy.py, pandas.py, sys.py, dateutil.py, CookieJar.py, urllib.py, urllib2.py, and Tkinter.py. The program uses Google CSE API client, which requires internet access for use. The user must also create an account with Google CSE API client to obtain an API key and must also set up their custom search engine (see https://developers.google.com/custom-search/docs/overview for more information). Information about installing this API is found here: https://developers.google.com/api-client-library/python/start/installation.


## 2. Usage

### (i) Background

The backbone of this software is the Google CSE API client, a tool that allows the user to submit any Google search. The flexible and dynamic nature of Articulate is that it allows the user to input an array of parameters to be queried, providing the user with the capability to search various websites by date, quoted content, query, and other specifications. Articulate returns information about each of the up to ten results that occur per query, mimicking what would be returned as one page of results if the query was searched on Google’s search bar. The information within each result contains items including the title of the article, media type (i.e. video, article, etc.), author, short excerpt, content keywords, date of publication, and various other attributes. This output can be modified by changing the source code. The information for each article is extracted and stored within the user-specified database. 

The functionality of this tool allows the user to step through ten “pages” of the same search, up to the 100th result, the user is thus limited to only retrieve 100 results per search. Each query submission can retrieve up to 10 results, and each developer key gets 100 queries a day for free. After that, each 1000 queries used in a day is $5 and the user can submit up to 10,000 queries a day. This constraint limits the users number of searches (100 free). These (number of search results and number of searches) necessitate the development of the of the time-step method within the algorithm, which must be calibrated for each individual run, and is discussed later.


## (ii) Software Inputs

Articulate requires one comma-separated values (csv) input and multiple string inputs: 

**1) Csv input:**  

1. Media Sites- a csv file containing the specific news websites to be searched and the code used access each website-specific dictionary. The dictionary for each news source must be manually determined by examining how newspapers store their online information. This file also includes an "ALL" row which is required to run the script and is always the last row of the input file. The "ALL" row is a default for the most common dictionaries used by news sources. 

    The headers in the csv file are:    
    site, url, type, date, keyword, title, type2, keyword2

    The *codes.sites.csv* file in this repository includes the dictionaries for nine widely circulated national and         California newspapers. 

**2) String inputs:**  

1. Output File Name- name of the database (.csv) in which the information should be stored    
2. Reference Date- the start point in the time period of the search inquiry, until present     
3. Time Step Size- the time interval to be used in the representation of results    
4. Number of Developer Keys- multiple developer keys may be required depending on the size (number of Search Terms, time period length and number of websites to search) of the query
5. Developer Key(s)- from Google CSE 
6. Search term(s)- The main search term for the query    
7. Or term(s)- defined by google as "[Provide] additional search terms to check for in a document, where each document in the search results must contain at least one of the additional search terms." Each Search term can have multiple Or terms.     
8. Include term(s)- must be found in each result in addition to the initial search term. Google defines these as "exactTerms." It is suggested that each search only have one associated Include term.    

The search will be performed for the Search term AND one or more of the OR terms AND all Include terms. It should be noted that Search, Or, and Include terms in the query are case sensitive.    

### (iii) Software Outputs

Articulate produces two types of spreadsheet outputs: 

**1) The Database File**
   
The database file contains identifying information for each article with the following headers: site, search, title, day, year, media_type, and further_info. The database file contains both hits and misses: 
* Hits are articles meeting all query criteria. These articles are counted in the tally database. 
* Misses should be manually removed from the database and are identified by incomplete information in the spreadsheet. The following errors define misses:  

Column | Error Code  
--- | ---  
title | miss
day | NA2, fell outside of range  
year | NA_out, NA2, not yet found2  
media_type | false_reporting2, pass1, pass2  


**2) The Dataframe File(s) (the Tally File(s))**
   
The dataframe files will return a tally count for each source in each Time Step Size period. One file will be returned for each Search Term. These dataframes report tallied results, counting the number of desired articles occurring at specified time intervals (e.g number of articles each month).
    

### (iv) Set up

1. Download the Articulate or Articulate_script folder which contains the Articulate.py Module, Articulations.py, and an example Media Sites file (codes.sites.csv).
2. Download all necessary Python modules described above.
3. Obtain developer key(s) from Google CSE. 
4. Create or modify Media Sites input file    
    * File should maintain the same format as the example file
    * Adding new news sources, which requires understanding how websites store article information, may take time and practice. It is important to understand how to navigate a python dictionary when doing this to find how each news source stores article metadata. If you are unsure of the dictionary structure for your wesite of interest, a good place to start is by copying the information in the "ALL" line and replacing "site" and "url" with your webiste of interest. 
5. Determine your search requirements and then ***test your search on a short time-frame to better approximate your appropriate time-step size and the number of developer keys required***. 

### (v). GitHub Repository and Executing Articulate

Articulate can be executed using a GUI (Articulate.py) or directly in the script (Articulate_script.py):

**(a) via the GUI**

1. Run Articulate.py 
2. Input parameters in pop-up boxes tk through tk#7 
3. When inputting searches:

    >Once you specify a search you would like articulate to query, you must enter it AND select it's check box. You can specify multiply searches to query, however, call of them must be selected. The code will treat each search individually, however, the final database will exclude dublicates that may come about within multiple searches. As also stated below, each search gets it's own specified "or" terms.   
   
5. When resetting developer keys:
    
    >If the program runs and submits 100 query submissions per developer key, reaching the maximum number of query submissions for a developer key, the program will ask you to reset your developer keys, to any developer key you desire (Each developer key has a number associated with it, whichever number you input, it will rese at this number developer key, and will exclude all developer keys input before that). Once doing this the program will wait until midnight, which is when the query counts reset, and then the program will continue to run. You can also type 'Exit', and the program will stop.

**(b) via the script**

The code in the Example_Script folder does not use a GUI and is run as a Python script. If you do not want to use the GUI, you can fork and modify this code to fit your needs. 

## 4. Limitations



## 5. Contributing

We are looking to refine the method for finding the site specific code, making the program more user friendly, and expanding the option to search within different time periods (instead of only from the present looking backwards). For more information about contributions, please contact the noted contact below.

## 6. Credits
This code was developed by Nick Roby at Stanford University. 

## 7. License 
See copyright.txt and LICENSE for more information.

## 8. Contact
For more information about Stanford's Urban Water Policy and Innovation Team please contact Newsha Ajami, Director of Urban Water Policy at newsha at stanford.edu. 

