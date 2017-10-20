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
    (v) Executing Articulate 
        (a) via the GUI
        (b) via the script
3.	Contributing
4.  GitHub Repository
5.	Credits
6.	License
7.  Contact


## 1. Installation
The software environment used by this program is Python version 2.7 with the following modules:  csv.py, time.py, datetime.py, googleapiclient.discovery.py, ast.py, numpy.py, pandas.py, sys.py, dateutil.py, CookieJar.py, urllib.py, urllib2.py, and Tkinter.py. The program uses Google CSE API client, which requires internet access for use. The user must also create an account with Google CSE API client to obtain an API key and must also set up their custom search engine (see https://developers.google.com/custom-search/docs/overview for more information). Information about installing this API is found here: https://developers.google.com/api-client-library/python/start/installation.


## 2. Usage

**(i) Background**

The backbone of this software is the Google CSE API client, a tool that allows the user to submit any Google search. The flexible and dynamic nature of Articulate is that it allows the user to input an array of parameters to be queried, providing the user with the capability to search various websites by date, quoted content, query, and other specifications. Articulate returns information about each of the up to ten results that occur per query, mimicking what would be returned as one page of results if the query was searched on Google’s search bar. The information within each result contains items including the title of the article, media type (i.e. video, article, etc.), author, short excerpt, content keywords, date of publication, and various other attributes. This output can be modified by changing the source code. The information for each article is extracted and stored within the user-specified database. 

The functionality of this tool allows the user to step through ten “pages” of the same search, up to the 100th result, the user is thus limited to only retrieve 100 results per search. Each query submission can retrieve up to 10 results, and each developer key gets 100 queries a day for free. After that, each 1000 queries used in a day is $5 and the user can submit up to 10,000 queries a day. This constraint limits the users number of searches (100 free). These (number of search results and number of searches) necessitate the development of the of the time-step method within the algorithm, which must be calibrated for each individual run, and is discussed later.


**(ii) Software Inputs**

Articulate requires a set of comma-separated values (csv) and string inputs. 

1) Csv input: 

The csv file contains the specific news websites to be searched and the code to access each website-specific dictionary. The dictionary for each news source is based on examining how newspapers store their online information. necessary to extract items of information from the search results. This file also includes an "ALL" row which is required to run the script and is always the last row of the input file. 

2) String inputs: 

1. Developer Key(s) 
2. Search term(s) 
3. Include term(s)
4. Or term(s)- terms that could also be included in a search, but do not necessarily need to be present i.e. if you were searching for articles on drought, these terms could be water or snow)
5. Date range of interest- from a certain date to the present
6. Date step size- the time interval to be used in the representation of results
7. Name of the database in which the information should be stored. 

It should be noted that all terms in the query are case sensitive (search, include, and or terms). All of these are input either using a GUI (Articulate.py) or directly in the script (Articulate_script.py). 


**(iii) Software Outputs**

Articulate produces two types of spreadsheet outputs: 

1) The Database File
   
The database file contains important identifying information about each article with the following headers: site,	search, title, day, year, media_type, and further_info. If the type of media (ie. article, image, video, etc) of a result cannot be determined, the title is returned as "miss" and no other information is obtained (the date information will return as NA). If an article's date cannot be found, it will simply return as NA. If an article's date appears to be outside the spcified time window, the date will return as "Fell outside of range".
        
2) The Dataframe File (Tally File)
   
The dataframe files will return a tally count for each source in each month. One file returned will be for each main search term.The first kind of outputs contain the number of articles published by each source for a certain search. These data frames report tallied results, counting the number of desired articles occurring at specified time intervals (e.g number of articles each month). One spreadsheet is produced for each keyword query. 
    

**(iv) Set up**

1. Download Articulate folder which contains the Articulate.py Module as well as Articulations.py and a couple example input files.
2. Download all necessary modules.
3. Obtain a developer key
4. Create Input File (file should maintain the same format exemplified in the example given)
  > Note that the creation of the file containing the site specific code may take time and practice. It is important to understand how to navigate a python dictionary when doing this to find how each news source stores article metadata. If this is too complicated, there is a suggested line of code that is available in the example.
5. Determine your search requirements
6. Test your search on a smaller time-frame to better approximate your appropriate time-step size


**(v) Executing Articulate**

*** (a) via the GUI

1. Run Articulate.py
2. Input initial parameters
3. When inputting searches:

    >Once you specify a search you would like articulate to query, you must enter it AND select it's check box. You can specify multiply searches to query, however, call of them must be selected. The code will treat each search individually, however, the final database will exclude dublicates that may come about within multiple searches. As also stated below, each search gets it's own specified "or" terms.

4. When inputting "or" and "include" terms:

    >The search will be performed for the main search term AND one or more of the "or" terms AND all "include" terms.
    
    >"or" terms, as defined by google, "[Provide] additional search terms to check for in a document, where each document in the search results must contain at least one of the additional search terms." These are input for each search specified when running articulate. 
    
   >"include" terms must be found in each result in addition to the initial search term. Google defines these as "exactTerms." It is suggested that each search only have one associated include term.
   
5. When resetting developer keys:
    
    >If the program runs and submits 100 query submissions per developer key, reaching the maximum number of query submissions for a developer key, the program will ask you to reset your developer keys, to any developer key you desire (Each developer key has a number associated with it, whichever number you input, it will rese at this number developer key, and will exclude all developer keys input before that). Once doing this the program will wait until midnight, which is when the query counts reset, and then the program will continue to run. You can also type 'Exit', and the program will stop.

*** (b) via the script

## 3. GitHub Repository

There are two ways to run Articulate- through a GUI or manually:

1. The code in the Articulate folder uses a GUI.

2. The code in the Example_Script folder does not use a GUI and is run as a Python script. If you do not want to use the GUI, you can fork and modify this code to fit your needs. 

## 4. Contributing

I am looking to refine the method for finding the site specific code, to make it more user friendly. For more information about contributions, please contact the noted contact below.


## 5. Credits
This code was developed by Nick Roby at Stanford University. 

## 6. License 
See copyright.txt and LICENSE for more information.


## 7. Contact
For more information about Stanford's Urban Water Policy and Innovation Team please contact Newsha Ajami, Director of Urban Water Policy at newsha at stanford.edu. 

