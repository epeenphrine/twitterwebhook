## standard library pip install
import bs4 as bs
import urllib.request
import json
import random
import asyncio
import re
import sqlite3
import os
import datetime
import time
import mysql.connector as mysql

## non standard libraries
import config
from dbsetup import db_check as dbcheck
import proxyscraper as scrape
import webhook

##conn = sqlite3.connect("twitterDB.db")
try:  ## try connecting to mysql first
    conn = mysql.connect(
        host=config.host,
        user=config.user,
        passwd=config.passwd,
        port=config.port
    )
except: ## if no successful MySQl connection use SQLite3
    conn = sqlite3.connect("twitterDB.db")

c = conn.cursor()
dbcheck() ## dbcheck will make sure tables and database is present / created by looking at the handles in config.twitter_url
urls = config.twitter_url
status = 0 ## status is here to check if we are in first run or not. Don't want to puke every tweet out there on initilization
"""starts at  0 to load the initial database. When status is 1 checks for new tweet after initial to send discord webhook"""

##url = "https://google.com"

def db_update(handle, url1, tweet):
    global status
    
    print (conn)
    db_type = str(type(conn)).lower()
    if "mysql" in db_type:
        c.execute("use twitterDB")
        entry_date = str(datetime.datetime.now())
        entry = (url1, tweet, entry_date)
        c.execute(f"SELECT * FROM {handle} where url = '{url1}'")
        query = c.fetchall()
        print(f"this is {query}")
        if not query and status == 0:
            print(f"mysql entry : {entry}")
            c.execute(f"INSERT INTO {handle} VALUES {entry}")
            conn.commit()
        elif not query and status == 1:
            print(f"mysql entry : {entry}")
            c.execute(f"INSERT INTO {handle} VALUES {entry}")
            conn.commit()
            webhook.message(url1)

        else:
            print("table and tweet exists skipping")
    elif "sqlite" in db_type:
        ## entry to database sqlite
        entry_date = str(datetime.datetime.now())
        entry = (url1, tweet, entry_date)
        query = c.execute(f"SELECT url FROM {handle} WHERE url = '{url1}'").fetchall()
        if not query and status == 0:
            print(f"sqlite entry : {entry}")
            c.execute(f"INSERT INTO {handle} VALUES {entry}")
            conn.commit()
        elif not query and status == 1:
            print(f"sqlite entry : {entry}")
            c.execute(f"INSERT INTO {handle} VALUES {entry}")
            conn.commit()
            webhook.message(url1)
        else:
            print("table and tweet exists skipping ....")

    else:
        print("can't connect to SQLite3 or MySQL")



async def twitter_scrape(url):
    global status
    if os.path.exists("proxydictlist.json"):
        with open("proxydictlist.json") as f:
            proxies_list = json.load(f)
            print(f"attempting to connect to: {url}")
            print(len(proxies_list))
    else:
        print("proxydictlist.json doesn't exist creating new proxylist")
        time.sleep(2)
        scrape.proxyscrape()
        with open("proxydictlist.json") as f:
            proxies_list = json.load(f)
            print(f"attempting to connect to: {url}")
            print(len(proxies_list))

    if len(proxies_list) >= 100:
        for i in range(0, len(proxies_list)):
            try:
                pick = random.choice(proxies_list)

                ## building opener
                proxy_support = urllib.request.ProxyHandler(pick)
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)

                ## requests
                req = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0"})
                sauce = urllib.request.urlopen(req, timeout=1).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')


                print(f"{pick} WORKED")
                ## break off the loop when we have a working proxy
                break
            except:
                print(f"{pick} did not work")
                proxies_list.remove(pick)
                print(f"{pick} removed")
                print(len(proxies_list))
                print(Exception)

        with open("proxydictlist.json", "w") as f:
            json.dump(proxies_list, f)
        print("\n\n\n\n\n\n\n\n")
        search = soup.findAll("div", {"data-tweet-id": re.compile(r".*")}) ## in div find attribute with data-tweet-id with any tag
        ##print(search) ## search in data type list
        for item in search: ## iterate through search which is in a list
            strip = item.get_text(strip = True)
            print("tweet:")
            print(strip)

            tweet = strip.replace("'","`")
            tag_get = item.get('data-tweet-id') ## get tags in the data-tweet-id attribute
            print(f"\ntag id = {tag_get}")

            split_ = url.split("/")
            split_.remove("")
            handle = split_[2]
            print(f"handle = {handle}")

            url1 = f"https://twitter.com/{handle}/status/{tag_get}"
            print(f"constructed new url : {url1}")
            print("*******************")
            db_update(handle, url1, tweet)
            print(f"status ........................................... {status}")
        print("\nscraping success !!")
        ##return db_update(url1)
    else:
        print("\n\n\n\n\n")
        print("getting new proxies")
        scrape.proxyscrape()
        print("\n")
        print("got new proxies ........................... ")

    print("sleeping for 30s")
    await asyncio.sleep(30)

def parallel_run():
    global status
    while True:
        tasks = []
        loop = asyncio.new_event_loop()
        for url in urls:
            tasks.append(loop.create_task(twitter_scrape(url)))
        loop.run_until_complete(asyncio.wait(tasks))
        status = 1


parallel_run()
