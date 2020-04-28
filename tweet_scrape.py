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

## non pip install libraries
import config
from proxy.proxy_rotate import proxy_rotate
import requests


##conn = sqlite3.connect("twitterDB.db")

url = "https://twitter.com/search?f=tweets&vertical=default&q={(from%3ArealDonaldTrump)}&l=en"
timer = 60
days = {

}

url = "https://twitter.com/i/profiles/show/realDonaldTrump/timeline/tweets?include_available_features=1&include_entities=1&max_position=1254586604360011776&reset_error_state=false"
url = "https://twitter.com/i/profiles/show/realDonaldTrump/timeline/tweets?include_available_features=1&include_entities=1&max_position=1253422154256756738&reset_error_state=false"

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
    if os.path.exists('secrets.py'):
        import secrets

    res = requests.get(secrets.neetcode_api)
    data = json.loads(res.content)
    
    soup = proxy_rotate(url)
    print(soup.prettify())
    search = soup.findAll("div", {"data-tweet-id": re.compile(r".*")}) ## in div find attribute with data-tweet_raw-id with any tag

    tweet_ids = [

    ]
    
    for item in search: ## iterate through search which is in a list
        
        strip = item.get_text(strip = True)
        tweet_raw = strip.replace("'","`")

        ## remove TweetEmbed Tweet 
        tweet_re = re.findall('.+TweetEmbed Tweet(.+)', tweet_raw)
        tweet_re1 = re.findall('(.+)(?=[0-9]+,[0-9,]+ replies)', tweet_raw)
        tweet_id = item.get('data-tweet-id') ## get tags in the data-tweet-id attribute
       
        print(f"tweet_raw:\n{tweet_raw}")
        print("tweet:")
        print(f"{tweet_re}")
        print('tweet1:')
        print(f"{tweet_re1}")
        print(f"\ntag id = {tweet_id}")

        split_ = url.split("/")
        split_.remove("")
        handle = split_[2]
        print(f"handle = {handle}")

        url1 = f"https://twitter.com/{handle}/status/{tweet_id}"
        print(f"constructed new url : {url1}")
        print("******************* \n")

        for month in months:
            tweet_when = re.findall(f'{month} \d\d|{month} \d', tweet_raw)
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
            payload['tweet'] = tweet_raw
            if tweet_when: 
                payload['date'] = constructed_date
            else:
                payload['date'] = str(date.today())
            payload['url'] = url1 
            payload['tweet_id'] = tweet_id
            data.append(payload)
            #post = requests.post(secrets.neetcode_api, data=payload)
            #print(f'posted : {post}')
            with open("tweets.json", "w") as f:
                json.dump(payload, f)
        else:
            print(f'{tweet_id} exists skipping \n')
            
    print('sleeping for 60s')
    time.sleep(60)
    return twitter_scrape(url)

twitter_scrape(url)