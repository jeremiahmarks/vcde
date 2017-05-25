#Welcome to my Vixxo code repo

This repo contains the code to automatically find the most recent surveys report,
assign the surveys to agents, close the surveys which are too old to survey, upload
the assigned surveys to google docs, and, finally, to send an email with the 
survey assignments to the floor. 

In order to get this code up and running you will need to 

* [Download and install Anaconda3
for Windows 64bit](https://www.continuum.io/downloads). Basically ensure that you are using
the installer for Python 3.6+ and 64-bit Windows.
* Clone and extract this repo into a folder that you know where it is. 
* Create a folder in your home directory named "surveyMagic"
* Find a copy of the "clientid.json" file and put it in the surveyMagic folder
* Open a command prompt (Win+r -> cmd -> run )
* Run the command `pip install google-api-python-client`
* Run the command 


*TODO*

* Make modular.  Basically make it to where it uses a popopen to run the process to send emails so that I can update the code on the fly.
* Include stats.  Service provider stats. SRs closed. All the stats.  Include them. 
* Make reusable - basically the fact that I copy/pasted that module in Email/start.py was an indication that I should have made it reusable. 
* Make a module to compare backstop reports over time, so that one can see what happened.
* Maybe add visuals/Animations for pretty things. 
* format the table html
* limit the table to the top items
* get a list of unfriendly statuses
* use unfriendly statuses to generate reporting
* add other teams
* add points. 
