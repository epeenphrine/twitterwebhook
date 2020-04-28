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
from proxy.proxy_scrape import scrape
import requests


##conn = sqlite3.connect("twitterDB.db")
max_position = ''
handle = 'realDonaldTrump'
url_base = f"https://twitter.com/{handle}"

days_to_search = 200
days_today = datetime.date.today()
days = datetime.timedelta(days_to_search)
days_delta = days_today - days
print(days_delta)
time.sleep(5)
def  twitter_scrape():
    global max_position
    tweet_datas = [

    ] 
    if os.path.exists('secrets.py'):
        import secrets
    ## initializing get first current tweet to add to max position
    if not max_position:
        res = requests.get(secrets.neetcode_api)
        data = json.loads(res.content)
      
        soup = proxy_rotate(url_base)
        initial_search = soup.find("div", 'tweet')['data-tweet-id'] ## in div find attribute with data-tweet_raw-id with any tag
   
    else:
        url_infinite_scroll = f"https://twitter.com/i/profiles/show/{handle}/timeline/tweets?include_available_features=1&include_entities=1&max_position={max_position}&reset_error_state=false"
        soup = proxy_rotate(url_infinite_scroll)

    search_tweet = soup.findAll('div', 'tweet')
    for item in search_tweet:
        tweet_data = {}
        tweet_data['tweet_content']= item.find('p', 'tweet-text').get_text(strip=True)
        tweet_data['tweet_id']= item['data-tweet-id']
        tweet_data['tweet_date'] = datetime.datetime.utcfromtimestamp(int(item.find('span', '_timestamp')['data-time'])).strftime("%Y-%m-%d")

        try:
            retweeter = item['data-retweeter']
        except:
            retweeter = None
        tweet_date = datetime.datetime.strptime(tweet_data['tweet_date'], "%Y-%m-%d").date()
        tweet_datas.append(tweet_data)
        print(tweet_date)
        if tweet_date < days_delta and (retweeter != handle): 
            print('scraping done!')
            break
        if item == search_tweet[-1]:
            max_position = tweet_data['tweet_id']
            print(max_position)
            return twitter_scrape()

twitter_scrape()
