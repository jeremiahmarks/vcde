#surveyData will exist to accept a URL and then get the data for 
#surveys assigned to me. It will output a single search string
#with all assigned SRs ORd together.

#Eventually this will break the SRs up by the store number and, perhaps add
#controls which control IE to page through the options. 

import requests

import urllib.request

temporaryTestingURL="https://docs.google.com/spreadsheets/d/1ELFMvDBhuROF9nMKpvMHQT8jLwOuvDIOUy1_hxYsda8/edit?usp=sharing"
csvTailer = "&output=csv"
with urllib.request.urlopen(temporaryTestingURL + csvTailer) as response:
	html = response.read()

n1 = "https://docs.google.com/spreadsheets/d/1ELFMvDBhuROF9nMKpvMHQT8jLwOuvDIOUy1_hxYsda8/export?format=csv"
r=requests.get(n1)
r
r.text
