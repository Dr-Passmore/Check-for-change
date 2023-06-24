# Standard Library
import os
import csv
import time
from datetime import datetime, timedelta
from urllib.parse import quote
import logging
import configparser
# External Library
import requests
from bs4 import BeautifulSoup
# Local Imports
from alert import alertProccess


# TODO - Comment up code 

class CheckForChange():
    '''
    Class checks for change in the target website. 
    '''
    def __init__(self, website, targetPhrase, timestamp):
        '''
        Initialisation of the CheckForChange Class. 
        Confirms that the websiteContent folder exists (if not it creates the folder)
        Checks to see if the website has been stored as a .txt file.
        If the website has not been previously stored it creates a .txt file of the visible text content. 
        If the website has previously been processed __init__ calles the compareWebsite function
        '''

        logging.info(f"The target website: {website} is being checked")
        # Gets the webpage
        request = requests.get(website)
        
        # creates a storage directory varible
        storageDirectory = "websiteContent"

        # creates a filename varible
        fileName = f"{storageDirectory}/{quote(website, safe='')}.txt"
        
        # Checks whether the storageDirectory exists
        if not os.path.exists(storageDirectory):
            # Creates directory if it does not exist
            os.makedirs(storageDirectory)
        
        if not os.path.isfile("config.ini"):
            config_file = configparser.ConfigParser()
            logging.info('Process to create config file started')
            configcreation = alertProccess.create_config(self, config_file)
            

        # If the fileName exists compare current website content with previously recorded
        if os.path.isfile(fileName):
            CheckForChange.compareWebsite(self, fileName, request, targetPhrase, timestamp, website)

        # if the website is seen for the first time it will create a file and populate with the visible website text
        else:
            logging.info(f"First time {website} has been processed. txt file created")
            with open(fileName, 'w', encoding='utf-8') as file:
                soup = BeautifulSoup(request.content, 'html.parser')
                visible_text = soup.get_text()
                file.write(visible_text)
                time.sleep(20)

    def compareWebsite(self, fileName, request, targetPhrase, timestamp, website):
        with open(fileName, "r", encoding='utf-8') as file:
            savedVersion = file.read()
        soup = BeautifulSoup(request.content, 'html.parser')
        if soup.get_text() == savedVersion:
            logging.info("The website remains unchanged from the last check")
            time.sleep(20)
        else:
            #update saved content 
            logging.info("New content has been detected - txt file has been updated")
            with open(fileName, 'w', encoding='utf-8') as file:
                visible_text = soup.get_text()
                file.write(visible_text)
            
            if targetPhrase in soup.get_text():
                logging.info(f"The target phrase: {targetPhrase} has been detected")
                #check timestamp if within 24 hours do not alert
                timestamp_str = timestamp
                
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                current_time = datetime.now()

                if current_time - timestamp < timedelta(hours=24):
                    # The timestamp is within the last 24 hours
                    logging.info("Timestamp is within the last 24 hours.")
                    time.sleep(20)
                else:
                    logging.info("Timestamp is older than 24 hours.") 
                    # Create new timestamp
                    new_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Update the timestamp in the current row
                    row[2] = new_timestamp
                    logging.info(f"Timestamp updated: {new_timestamp}")

                    # Write the updated rows back to the CSV file
                    with open("targets.csv", "w", newline='') as file:
                        writer = csv.writer(file, delimiter=",")
                        writer.writerows(rows)
                    CheckForChange.alert(self, website)
            else:
                time.sleep(20)

    def alert(self, website):
        logging.info("Alert Process has been started")
        alertProcessInstance = alertProccess(website)
        time.sleep(20)

# Logging
logging.basicConfig(filename='checkforchange.log', 
                    filemode='a', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Initialise an empty list to store rows
rows = []  

# Read all rows into a list
with open("targets.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    rows = list(reader)  

# For each item in Rows
for row in rows:
    
    # Get the URL
    website = row[0].strip('[]"')
    
    # get target phrase for webpage
    targetPhrase = row[1].strip('[]"')
    
    # First time running with the a new URL, the script adds a time stamp 24 hours previously (This is to prevent the item going into stock within 24 hours)
    if len(row) < 3:
        # Get the current timestamp
        current_time = datetime.now()

        # Subtract 24 hours from the current timestamp
        time_24_hours_ago = current_time - timedelta(hours=24)

        # Convert the timestamp to string format
        time_24_hours_ago_str = time_24_hours_ago.strftime("%Y-%m-%d %H:%M:%S")

        # Insert the timestamp after the "In stock" column
        row.insert(2, time_24_hours_ago_str)
    
# Writes the rows back to the CSV
with open("targets.csv", "w", newline='') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerows(rows)
    
# Runs CheckForChange class passing website, targetPhrase, and timestamp variables for each row
for row in rows:
    website = row[0].strip('[]"')
    targetPhrase = row[1].strip('[]"')
    timestamp = row[2].strip('[]"')
    CheckForChange(website, targetPhrase, timestamp)