# Articulate
A search tool for quantifying news media coverage

## Introduction

News media plays an important role shaping public opinion and attitudes. However, current proprietary databases used for media investigation can be expensive, rigid, and limited in scope. To address these challenges, we developed Articulate, an open-source, flexible tool for discovering, compiling, and quantifying newspaper coverage on a user-specified topic. Articulate is written in Python and interfaces with Google Custom Search Engine (CSE) API to allow the user to extract, classify, represent, and store information from various media sources in a functional database. Articulate offers equal and sometimes greater data coverage than produced by comparable proprietary databases. 

## Table of Contents    
1.	Installation
2.	Usage  
    (i) Background  
    (ii) Inputs  
    (iii) Outputs  
    (iv) Set up  
    (v) GitHub Repository and Executing Articulate     
3.  Limitaions    
4.	Contributing
5.	Credits
6.	License
7.  Contact

## 1. Installation    

The software environment used by this program is Python version 2.7 with the following modules:  csv.py, time.py, datetime.py, googleapiclient.discovery.py, ast.py, numpy.py, pandas.py, sys.py, dateutil.py, CookieJar.py, urllib.py, urllib2.py, and Tkinter.py. The program uses Google CSE API client, which requires internet access for use. The user must also create an account with Google CSE API client to obtain an API key and must also set up their custom search engine (see https://developers.google.com/custom-search/docs/overview for more information). Information about installing this API is found here: https://developers.google.com/api-client-library/python/start/installation.

## 2. Usage

### (i) Background

The backbone of this software is the Google CSE API client, a tool that allows the user to submit any Google search. The flexible and dynamic nature of Articulate is that it allows the user to input an array of parameters to be queried, providing the user with the capability to search various websites by date, quoted content, query, and other specifications. Articulate returns information about each of the up to ten results that occur per query, mimicking what would be returned as one page of results if the query was searched on Google’s search bar. The information within each result contains items including the title of the article, media type (i.e. video, article, etc.), author, short excerpt, content keywords, date of publication, and various other attributes. This output can be modified by changing the source code. The information for each article is extracted and stored within the user-specified database. 

The functionality of this tool allows the user to step through ten “pages” of the same search, up to the 100th result, the user is thus limited to only retrieve 100 results per search. Each query submission can retrieve up to 10 results, and each developer key gets 100 queries a day for free. After that, each 1000 queries used in a day is $5 and the user can submit up to 10,000 queries a day. This constraint limits the users number of searches (100 free). These (number of search results and number of searches) necessitate the development of the of the time-step method within the algorithm, which must be calibrated for each individual run, and is discussed later. Once you have refined your search, it may be helpful to get a free trial of the upgraded version of Google CSE to increase your developer key limit (see https://cloud.google.com/free/docs/frequently-asked-questions#upgrading-billing for more infomration). 

### (ii) Software Inputs

Articulate requires one comma-separated values (csv) input and multiple string inputs: 

**1) Csv input:**  

1. Media Sites- a csv file containing the specific news websites to be searched and the code used access each website-specific dictionary. The dictionary for each news source must be manually determined by examining how newspapers store their online information. This file also includes an "ALL" row which is required to run the script and is always the last row of the input file. The "ALL" row is a default for the most common dictionaries used by news sources. 

    The headers in the csv file are:    
    site, url, type, date, keyword, title, type2, keyword2

    The *codes.sites.csv* file in this repository includes the dictionaries for nine widely circulated national and         California newspapers. 

**2) String inputs:**  

1. Output File Name- name of the database (.csv) in which the output Database file should be stored    
2. Reference Date- the start point in the time period of the search inquiry, until present     
3. Time Step Size- the time interval to be used in the representation of results    
4. Number of Developer Keys- multiple developer keys may be required depending on the size (number of Search Terms, time period length and number of websites to search) of the query
5. Developer Key(s)- from Google CSE 
6. Search term(s)- the main search term for the query    
7. Or term(s)- defined by Google as "additional search terms to check for in a document, where each document in the search results must contain at least one of the additional search terms." Each Search term can have multiple Or terms, and Or terms are defined seperately for each Search term.  
8. Include term(s)- must be found in each result in addition to the initial search term. Google defines these as "exactTerms." It is suggested that each search only have one associated Include term.    

The search will be performed for the Search term AND one or more of the OR terms AND all Include terms. It should be noted that Search, Or, and Include terms in the query are case sensitive.    

### (iii) Software Outputs

Articulate produces two types of spreadsheet outputs: 

**1) The Database File**
   
The database file contains identifying information for each article with the following headers: site, search, title, day, year, media_type, and further_info. The database file contains both hits and misses: 
* Hits are articles meeting all query criteria. These articles are counted in the tally database. 
* Misses should be manually removed from the database and are identified by incomplete information in the spreadsheet. The following errors define misses:  

Column | Error Code  | Description
--- | ---  | ---
title | miss, duplicate- | A "miss" error code indicates _Articulate_ was unable to retrieve a title from the article metadata. A "duplicate-" error indicates a title was retrieved but it is a duplicate of an article already tallied. 
day | NA, fell outside of range  | "NA" errors indicate that _Articulate_ was not able to extract the publication year, or that the date is in an unrecognized format. A "fell outside of range" error indicates the date was found to fall outside of the user-specified time range, and the article is not tallied.
year | NA_out, NA, not yet found  | "NA" and "not yet found" errors indicate that _Articulate_ was not able to extract the publication year, or that the date is in an unrecognized format. An "NA_out" error indicates the date was found to fall outside of the user-specified time range, and the article is not tallied.
media_type | false_reporting, pass1, pass2  | _Articulate_ uses two different methods to atetmpt to retrieve the media type label. A "pass1" or "pass2" error indicates _Articulate_ was unable to confirm the media type as an article. A "false_reporting" error indicates _Articulate_ could not confirm that the article is relevant despite being pulled by CSE (i.e. the "search", "or", and "include" terms could not be found in the article headline or body).

**2) The Dataframe File(s) (also known as the Tally File(s))**
   
The dataframe files will return a tally count for each source in each Time Step Size period. One file will be returned for each Search Term. These dataframes report tallied results, counting the number of desired articles occurring at specified time intervals (e.g number of articles each month). While the Database file is named by the user, the Dataframes are named automatically based on the Search terms and date of search.    

### (iv) Set up

1. Download the Articulate or Articulate_script folder which contains the Articulate.py Module, Articulations.py, and an example Media Sites file (codes.sites.csv).
2. Download all necessary Python modules described above.
3. Obtain developer key(s) from Google CSE. 
4. Create or modify Media Sites input file:    
    * File should maintain the same format as the example file
    * Adding new news sources, which requires understanding how websites store article information, may take time and practice. It is important to understand how to navigate a python dictionary when doing this to find how each news source stores article metadata. If you are unsure of the dictionary structure for your wesite of interest, a good place to start is by copying the information in the "ALL" line and replacing "site" and "url" with your webiste of interest. 
5. Determine your search requirements and then ***test your search on a short time-frame to better approximate your appropriate time-step size and the number of developer keys required***. 

### (v). GitHub Repository and Executing Articulate

Articulate can be executed using a GUI (Articulate.py) or directly in the script (Articulate_script.py).    

**(a) via the GUI**

1. Download the files from the Articluate folder. 

2. Run Articulate.py. The other python file in the folder, Articulations.py, is required to run the program and should be left untouched. 

2. Input parameters through a series of pop-up boxes labelled tk through tk#(n) where n depends on the number of Search terms and Developer keys entered. With one developer key and one search term, the pop-up boxes will be tk through tk#7    
   
***In the GUI, once you enter an input, you must also select it's check box.*** You can specify multiple searches to query. The code will treat each search individually, however, the final database will exclude dublicates that may come about within multiple searches. Also, as stated above, each search gets it's own specified "or" terms.  
    
3. Output files will be in the same folder as the code and input file. 

A note about developer keys: 

The program submits 100 query submissions per developer key. If Articulate reaches the maximum number of query submissions for a developer key and you have input multiple keys, it will automatically move to the next key. However, if the program reaches the maximum number of queries for all devleoper keys, the program will ask you to reset your developer keys. You can reset the developer key to any of the input keys and it will resstart at this number developer key, excluding all developer keys input before that. Then, the program will wait until midnight, which is when the query counts reset, and then continue to run. You can also type 'Exit', and the program will stop.

\****See the Articulate_ReadMe_Supplement.pdf file for screenshots showing the distinct steps for running Articulate through the GUI***\*

**(b) via the script**

1. Download the files in the Example_Script folder. 

2. Fork and modify the code to fit your needs, including manually hardcoding the input parameters.

3. Run Articulate_script.py.

## 3. Limitations

Users should consider some of the challenges and limitations that arise from the nature of this tool. In particular, this software relies on Google’s CSE API, a free online tool to retrieve information similar to the way a user would perform a Google Search. Because this method requires news media to be present in the internet, in a recognizable online format, Articulate is inherently limited to applications in recent decades, and may be insufficient when the purpose of the study is to assess multi-decadal trends expanding prior to the internet era. This is coupled with the limitation that Articulate searches from a certain date to the present, thus it is most practical to search for articles within a relatively recent time period. 

Similarly, because Articulate goes through a mechanistic process of looking for relevant information in the form of specific keywords and specific dates in news articles, there may be cases where results are falsely reported despite being irrelevant (e.g. a sports team in a winning drought, a flood of support for charity). ***Users should be careful to manually check Articulate output results for relevance as needed.*** This challenge is also faced by users querying from proprietary databases.

## 4. Contributing

We are looking to refine the method for finding the site specific code, making the program more user friendly, and expanding the option to search within different time periods (instead of only from the present looking backwards). For more information about contributions, please contact the noted contact below.

## 5. Credits
This code was developed by Nick Roby at Stanford University with contributions by Patricia Gonzales, Kim Quesnel, and Newsha Ajami.

Please cite the following manuscript when referencing Articulate:    
Roby, N. A., Gonzales, P., Quesnel, K. J., & Ajami, N. K. (2018). A novel search algorithm for quantifying news media coverage as a measure of environmental issue salience. Environmental Modelling & Software, 101, 249-255.

## 6. License 
See copyright.txt and LICENSE for more information.

## 7. Contact
For more information about Articulate or Stanford's Urban Water Policy and Innovation Team please contact Newsha Ajami, Director of Urban Water Policy, at newsha at stanford.edu. 

