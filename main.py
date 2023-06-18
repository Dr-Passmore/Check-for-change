import requests
import os
import csv
import time
from datetime import datetime, timedelta
class CheckForChange():
    def __init__(self, website, targetPhrase):
        request = requests.get(website)
        fileName = f"websiteContent/{website.replace('/', '_')}.txt"
        storageDirectory = "websiteContent"
        if not os.path.exists(storageDirectory):
            os.makedirs(storageDirectory)
        if os.path.isfile(fileName):
            CheckForChange.compareWebsite(self, fileName, request, targetPhrase)
        else:
            with open(fileName, 'w') as file:
                file.write(request.content.decode()) 
                time.sleep(20)

    def compareWebsite(self, fileName, request, targetPhrase):
        with open(fileName, "r") as file:
            savedVersion = file.read()
        if request.content.decode() == savedVersion:
            print("Website is the same")
            time.sleep(20)
        else:
            #update saved content 
            print("New content")
            with open(fileName, 'w') as file:
                file.write(request.content.decode()) 
            if targetPhrase in request.content.decode(): 
                CheckForChange.alert(self)
            else:
                time.sleep(20)

    def alert(self):
        print("test")
        time.sleep(20)
'''
with open("targets.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        website = row[0].strip('[]"')
        targetPhrase = row[1].strip('[]"')
        if len(row) < 3:
            # Get the current timestamp
            current_time = datetime.now()

            # Subtract 24 hours from the current timestamp
            time_24_hours_ago = current_time - timedelta(hours=24)

            # Convert the timestamps to string format
            time_24_hours_ago_str = time_24_hours_ago.strftime("%Y-%m-%d %H:%M:%S")
            row.insert(2, time_24_hours_ago_str)
            
        else:
            timestamp = row[2].strip('[]"')

        
        CheckForChange(website, targetPhrase)

    with open("targets.csv", "w", newline='') as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerows(rows)
'''

rows = []  # Initialize an empty list to store rows

with open("targets.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    rows = list(reader)  # Read all rows into a list

for row in rows:
    website = row[0].strip('[]"')
    targetPhrase = row[1].strip('[]"')
    if len(row) < 3:
        # Get the current timestamp
        current_time = datetime.now()

        # Subtract 24 hours from the current timestamp
        time_24_hours_ago = current_time - timedelta(hours=24)

        # Convert the timestamp to string format
        time_24_hours_ago_str = time_24_hours_ago.strftime("%Y-%m-%d %H:%M:%S")

        # Insert the timestamp after the "In stock" column
        row.insert(2, time_24_hours_ago_str)

with open("targets.csv", "w", newline='') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerows(rows)

for row in rows:
    website = row[0].strip('[]"')
    targetPhrase = row[1].strip('[]"')
    timestamp = row[2].strip('[]"')
    CheckForChange(website, targetPhrase)