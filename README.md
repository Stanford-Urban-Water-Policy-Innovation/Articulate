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
    
        1) Reading the Database File
        2) The Tally File
    
    (iv) Set up
    
    (v) Executing Articulate
3.	Contributing
4.	Credits
5.	License
6.  Contact

## 1. Installation
The software environment used by this program is Python version 2.7 with the following modules:  tkinter.py, serverscsv.py, time.py, datetime.py, googleapiclient.discovery.py, ast.py, numpy.py, pandas.py, sys.py, and dateutil.py. The program uses Google CSE API client, which requires internet access for use. The user must also create an account with Google CSE API client to obtain an API key and must also set up their custom search engine (see https://developers.google.com/custom-search/docs/overview for more information). Information about installing this API is found here: https://developers.google.com/api-client-library/python/start/installation.

## 2. Usage

**(i) Background**

The backbone of this software is the Google CSE API client, a tool that allows the user to submit any Google search. The flexible and dynamic nature of Articulate is that it allows the user to input an array of parameters to be queried, providing the user with the capability to search various websites by date, quoted content, query, and other specifications. Articulate returns information about each of the up to ten results that occur per query, mimicking what would be returned as one page of results if the query was searched on Google’s search bar. The information within each result contains items including the title of the article, media type (i.e. video, article, etc.), author, short excerpt, content keywords, date of publication, and various other attributes. This output can be modified by changing the source code. The information for each article is extracted and stored within the user-specified database. The functionality of this tool allows the user to step through ten “pages” of the same search, up to the 100th result, the user is thus limited to only retrieve 100 results per search. Each query submission can retrieve up to 10 results, and each developer key gets 100 queries a day for free. After that, each 1000 queries used in a day is $5 and the user can submit up to 10,000 queries a day. This constraint limits the users number of searches (100 free). These (number of search results and number of searches) necessitate the development of the of the time-step method within the algorithm, which must be calibrated for each individual run, and is discussed later.

**(ii) Software Inputs**

The software takes both string and csv inputs. There are two distinct csv inputs: (1) a csv file that contains the code necessary to extract items of information from the search results and (2) a csv file containing the websites to be searched. The rest of the inputs are string inputs. This includes the search words, Developer Keys, terms to exclude, terms search as “or terms” (“or terms” are terms that could also be included in a search, but do not necessarily need to be present i.e. water or snow), the date range, the date step size (the date step size is the time interval to be use in the representation of results), and the name of the database in which the information should be created. All of these are input using a GUI.

**(iii) Software Outputs**

Articulate produces two types of spreadsheet outputs. The first kind of outputs contain the number of articles published by each source for a certain search. These data frames report tallied results, counting the number of desired articles occurring at specified time intervals (e.g number of articles each month). One spreadsheet is produced for each keyword query. The second output is a database file containing important identifying information about each article such as date published, title, author, and more.

    

**(iv) Set up**

1. Download Articulate folder which contains the Articulate.py Module as well as Articulations.py and a couple example input files.
2. Download all necessary modules.
3. Obtain a developer key
4. Create Input Files
  > Note that the creation of the file containing the site specific code may take time and practice. It is important to understand how to navigate a python dictionary when doing this to find how each news source stores article metadata. If this is too complicated, there is a suggested line of code that is available in the example.
5. Determine your search requirements
6. Test your search on a smaller time-frame to better approximate your appropriate time-step size

**(v) Executing Articulate**

1. Run Articulate.py
2. Input initial parameters
3. When inputting searches:

4. When inputting "or" terms:

## 3. Contributing

I am looking to refine the method for finding the site specific code, to make it more user friendly. All other contributions can be emailed to ____

## 4. Credits

## 5. License 
See copyright.txt and LICENSE for more information.

## 6. Contact
For more information about Stanford's Urban Water Policy and Innovation Team please contact Newsha Ajami, Director of Urban Water Policy at newsha at stanford.edu. 

