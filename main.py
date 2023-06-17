import requests
import os
import csv
import time

class CheckForChange():
    def __init__(self, website, targetPhrase):
        request = requests.get(website)
        fileName = f"{website.replace('/', '_')}.txt"
        if os.path.isfile(fileName):
            CheckForChange.compareWebsite(self, fileName, request, targetPhrase)
        else:
            with open(fileName, 'w') as file:
                file.write(request.content.decode()) 

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

with open("targets.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        website = row[0].strip('[]"')
        targetPhrase = row[1].strip('[]"')
        print(website)
        print(targetPhrase)
        CheckForChange(website, targetPhrase)
