from datetime import datetime
import time
from instapy_cli import client
import credentials as creds
import os
import praw 
from urllib.error import URLError, HTTPError
import urllib.request as web
import shutil 
import colorama
from colorama import Fore, Style

def uploadTree(image, text):
    username = creds.uname
    password = creds.pw 
    with client(username, password) as cli:
        cli.upload(image, text)

def dlreddit():
    reddit = praw.Reddit(client_id=creds.rpkey, \
                     client_secret=creds.rkey, \
                     user_agent=creds.rname, \
                     username=creds.runame, \
                     password=creds.rpw)
    current_dir = os.getcwd()
    dir_path = os.path.join(current_dir,'plants')
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    colorama.init(autoreset = True)
    post = reddit.subreddit('plants').hot(limit=3)

    for submissions in post:
        if not submissions.stickied and submissions.score > 50:
            fullfilename = os.path.join(dir_path, "{}.jpg".format(submissions))
            request = web.Request(submissions.url, headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'})
            with web.urlopen(request) as response, open(fullfilename, 'wb') as out_file:                
                try:
                    shutil.copyfileobj(response, out_file)
                except HTTPError as e:
                    print("{}{}{}".format(Fore.RED, e.code, Style.RESET_ALL))
                except URLError as e:
                    print("{}{}{}".format(Fore.RED, e.reason, Style.RESET_ALL))                 

                # delete corrupted files smaller than 55 KB
                filesize = os.path.getsize(fullfilename)
                if filesize < 55000:
                    os.remove(fullfilename)
                
    file = "/plants/" + fullfilename
    return file

if __name__ == "__main__":
    text =  'Save Trees!' + '\r\n.\n.\n' + '#trees #savetrees #enviornment #beatplasticpollution #globalclimatestrike #climatechange #climatecrisis #weekforfuture #fridaysforfuture #extinctionrebellion #plastics #ocean #recycling #climate #savetrees #nature #protectnature #savebees #saveplants #environment #onebhoomi #SaveEarth #CleanEnergy #Climatechange #zerocarbon #environment #cleanenergy #climatechangeisreal #sustainableliving #sustainability #getwoketotheplanet #environment'
    
    while True:
        now = datetime.now()
        currentTime = now.strftime("%H")
        print(currentTime)
        if currentTime == "08":
            uploadTree("daily.jpg", text)

        elif currentTime == "16":
            uploadTree("daily.jpg", text)

        elif currentTime == "00":
            img = dlreddit()
            uploadTree(img,"")
            os.chdir("../plants")

        time.sleep(3500)

