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
from datetime import date
import time

## non standard libraries
import config
import proxyscraper as scrape
import requests


##conn = sqlite3.connect("twitterDB.db")

url = "https://twitter.com/realDonaldTrump"
timer = 60
days = {

}

for i in range(1,32):
    if i < 10: 
        days[str(i)] = f"0{i}"
    else:
        days[str(i)] = f"{i}"

months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
]

month_key = {
    'Jan' : '01',
    'Feb' : '02',
    'Mar' : '03',
    'Apr' : '04',
    'May' : '05',
    'Jun' : '06',
    'Jul' : '07',
    'Aug' : '08',
    'Sep' : '09',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12'
}


def  twitter_scrape(url):
    res = requests.get('http://neetcode.com:1337/api/tweet/')
    data = json.loads(res.content)

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

        with open("proxydictlist.json", "w") as f:
            json.dump(proxies_list, f)
        print("\n\n\n\n\n\n\n\n")
        search = soup.findAll("div", {"data-tweet-id": re.compile(r".*")}) ## in div find attribute with data-tweet-id with any tag

        tweet_ids = [

        ]
    
        for item in search: ## iterate through search which is in a list
        
            strip = item.get_text(strip = True)
            print("tweet:")
            print(strip)

            tweet = strip.replace("'","`")
            tweet_id = item.get('data-tweet-id') ## get tags in the data-tweet-id attribute
            print(f"\ntag id = {tweet_id}")

            split_ = url.split("/")
            split_.remove("")
            handle = split_[2]
            print(f"handle = {handle}")

            url1 = f"https://twitter.com/{handle}/status/{tweet_id}"
            print(f"constructed new url : {url1}")
            print("******************* \n")

            for month in months:
                tweet_when = re.findall(f'{month} \d\d|{month} \d', tweet)
                if tweet_when:
                    break

            if tweet_when:
                when_split = tweet_when[0].split()
                day = days[when_split[1]]
                month = month_key[when_split[0]]
                year = date.today().year
                constructed_date = f"{year}-{month}-{day}"
                print(constructed_date)

            if not tweet_when:
                print(date.today())
            
            ## post request. Preventing repeated entries
            if not any(dat['tweet_id'] == tweet_id for dat in data):

                payload = {
                
                    }
                payload['handle'] = handle
                payload['tweet'] = tweet
                if tweet_when: 
                    payload['date'] = constructed_date
                else:
                    payload['date'] = str(date.today())
                payload['url'] = url1 
                payload['tweet_id'] = tweet_id
                data.append(payload)
                post = requests.post('http://neetcode.com:1337/api/tweet/', data=payload)
                print(f'posted : {post}')

            else:
                print(f'{tweet_id} exists skipping \n')
            
        print('sleeping for 60s')
        time.sleep(60)
        return twitter_scrape(url)
    else:
        scrape.proxyscrape()
        return twitter_scrape(url)
twitter_scrape(url)