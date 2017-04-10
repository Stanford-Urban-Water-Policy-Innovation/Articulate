# Articulate
A search tool for quantifying news media coverage

Introduction
Written media has two mechanisms by which it is useful in social behavior analysis: it can be both a reflection of society and a mechanism by which society is influenced. This dual nature to news media (makes it an attractive source of data to understand deeper). There are currently limited resources for finding news articles. The Articulate python package allows for the analysis of written news media data. The user can extract, classify, represent, and store information from various media sources, generating a dataset of information in a manner that gives the user flexibility. Compared to proprietary tools, this package opens the door for analysis of more sources while maintaining equal and sometimes greater data coverage compared to the existing tools.

Table of Contents
I.	Installation
II.	Usage
A)	Background
B)	Software Inputs
C)	Software Outputs
D)	Set up
E)	Executing Articulate
III.	Contributing
IV.	Credits
V.	License

I. Installation
The software environment used by this program is Python version 2.7 with the following modules:  tkinter.py, serverscsv.py, time.py, datetime.py, googleapiclient.discovery.py, ast.py, numpy.py, pandas.py, sys.py, and dateutil.py. The program uses Google CSE API client, which requires internet access for use. As well the user must create an account with Google CSE API client to obtain an API key and must also set up their custom search engine. Information on how this is done can be found through https://developers.google.com/custom-search/docs/overview.

II. Usage
A) Background
The most important module used in this software is the Google CSE API client, a tool that allows the user to submit any Google search. The flexible and dynamic nature of this tool allows the user to input an array of parameters to be queried. This provides the user with the capability to search various websites by date, by quoted content, by an exclusive query, and other functions. The tool then returns information about each of the up to ten results that occur per query. The information returned is what would be returned as one page of results if the query was searched on Google’s search bar. The information within each result contains items which can include title of the result, media type (i.e. video, article, etc.), author, short excerpt, content keywords, date of publication, and various other attributes. All of these can be added or taken away, if desired, by slight changes to the articulate source code. The information is extracted and stored within the database specified by the user. The functionality of this tool allows the user to step through ten “pages” of the same search, up to the 100th result. This is the first of two important constraints in the development of this code: the user is limited to only retrieve 100 results per search. It is important to note that each query submission can retrieve up to 10 results, and each developer key gets 100 queries a day for free. After that, each 1000 queries used in a day is $5 and the user can submit up to 10,000 queries a day with this method. These limitations create the two formative constraints within this program. The first, as stated above, is the limit on the number of results returned per search (100). The second is a limit on the number of searches (100 free). These constraints are the reason for the development of the of the time-step method within the algorithm, which must be calibrated for each individual run, and is discussed later.

B) Software Inputs
The software takes both string and csv inputs. There are two distinct csv inputs: (1) a csv file that contains the code necessary to extract items of information from the search results and (2) a csv file containing the websites to be searched. The rest of the inputs are input as a string. This includes the search words, Developer Keys, terms to exclude, terms search as “or terms” (“or terms” are terms that could also be included in a search, but do not necessarily need to be present i.e. water or snow), the date range, the date step size (the date step size is the time interval to be use in the representation of results), and the name of the database in which the information should be created. All of these are input and using a GUI.

C) Software Outputs
As there were two kinds of inputs, there are also two kinds of outputs. The first output created by the program is a data frame that contains the number of articles published by each source for a certain search. The data frame reports tallied results, tallying the number of desired articles occurring at specified time intervals (i.e. number of articles each month). The second output is a database file containing various information about each article, such as date published, title, and more.

D) Set up
1) Download all necessary modules.
2) Obtain a developer key
3) Create Input Files
i) The creation of the file containing the site specific code may take time and practice. It is important to understand how to navigate a python dictionary when doing this. If this is too complicated, there is a suggested line of code that is available in the example.
4) Determine your search requirements
5) Test your search on a smaller time-frame to better approximate your appropriate time-step size

E) Executing Articulate
Step-by-step?

Contributing
I am looking to refine the method for finding the site specific code, to make it more user friendly. All other contributions can be emailed to ____

Credits
