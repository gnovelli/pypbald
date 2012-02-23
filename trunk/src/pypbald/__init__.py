'''
    pypbald (Python Passive Broadcast Analyzer - Listening Daemon:)
    is organized in five packages:
    - backend
    - logging
    - parsing
    - records

    Such packages contain classes source code for the following features:
    - Filtered capture of broadcast packets (selective sniffing)
    - Parsing of such filtered packets (parsing) and extraction of 
      well formed records with information of interest
    - Logging of such records on rotating logfiles
    - Storing on one or more DBs of such records 

    Author:
        Giovanni Novelli, Ph.D.
	giovanni.novelli@gmail.com
'''

__author__ = "Giovanni Novelli"
__date__ = "02/05/2010"


