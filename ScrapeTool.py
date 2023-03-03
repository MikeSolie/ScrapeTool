##################################################
# Mike Solie                                     #
# 02/24/2023                                     #
# Version 2                                      #
# Website Scraping and writing to Database       #
#                                                #
# Description:                                   #
# Scrapes a website for anchor tags in the root  #
# directory. Then checks to see if the specified #
# database exists, if it doesn't it creates it,  #
# then writes tag and time.                      #
##################################################


#####
# import os to use the operating system for the filepath
# import sqlite3 to interact/write db file
# import datetime to write time to db
# import http.client to send get request/receive response
# import ssl incase of https errors
# import re to search for expressions
#####

import os
import sqlite3
import datetime
import http.client
import ssl
import re

#####
# function: time
# purpose: to get run time
# inputs: none
# returns: current_time
#####
def time():
    # current time variable
    current_time = datetime.datetime.now().time()
    # returns the current time
    return current_time

#####
# function: get_path
# purpose: to get the file path to the database file
# inputs: filename
# returns: full path to database file
#####
def get_path(filename):
    # path to current directory for this program
    DIR_NAME = os.path.dirname(__file__)

    # variable to the full path of the file (assuming it is in the same directory as the program
    db_path = os.path.join(DIR_NAME, filename)
    # print(db_path) debug print statement
    # returns the full path to the file
    return db_path

#####
# function: connect
# purpose: connects to website catches stores the response
# inputs: website to be scraped
# returns: url_list
#####
def connect(website):
    # connection count list to break out of while loop
    count = 0
    # empty list to write urls to
    url_list = []
    # connection/http client variable
    connection = http.client.HTTPSConnection(website)
    # defines the connection request - GET request at the root directory
    connection.request("GET", "/")
    # response to the get request
    response = connection.getresponse()

    # while loop at 500
    while count < 500:
        # try/except block for the connection
        try:
            # counter to break out of loop
            count = count + 1
            # reads the lines from the response
            line = response.readline()
            # if statement that uses re to search for anchor tags and decodes to utf-8
            if re.search("<a ", line.decode("utf-8")):
                # appends the url_list with the decoded outcome
                url_list.append(line.decode("utf-8"))
        # keyboard exception exit
        except KeyboardInterrupt as k:
            print(k)
    # for loop to clean up terminal output
    for url in url_list:
        print(url)
    # returns url_list to be iterated through
    return url_list

#####
# function: open_db
# purpose: to connect to and open the database
# inputs: SQL command
# returns: nothing, updates table
#####
def create_db(db_path, url_list, current_time):
    # connects to/writes the db
    connection = sqlite3.connect(db_path)
    # cursor uses the connection to execute SQL commands
    cursor = connection.cursor()
    # stores current time as a str... I did it here because turning it into
    # string didn't work in the time function
    current_time = str(current_time)
    # try/except block for creating the "scrape" table
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS scrape (
                    current_time TEXT,
                    url TEXT
                    )""")
    except sqlite3.Error as e:
        print(e)
    # for loop to pull the urls out from the list
    for url in url_list:
        # try/except block to insert the values into the scrape table
        try:
            cursor.execute("INSERT INTO scrape VALUES (?,?)", (current_time, url))
        except sqlite3.Error as e:
            print(e)
    # saves the changes made to the db/table
    connection.commit()
    # closes the connection
    connection.close()


#####
# function: main
# purpose: to run the program
# inputs: db file
# returns: nothing, runs the program
#####
def main():
    # variable where the 'scrape.db' is stored
    path = get_path('scrape.db')
    # gets the current time
    current_time = time()
    # the website to scrape
    url_list = connect("catalog.champlain.edu")
    # opens/writes/closes the db file
    create_db(path, url_list, current_time)

# call to start the program
##---->
main()
##<----
# program end
