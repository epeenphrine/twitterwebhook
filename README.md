# twitterwebhook

## about twitterwebhook
created due to the limited amount of requests you can make with twitter API. The webhook posts the newest tweets and posts it to discord.

Since you are making alot of requests to get the most recent tweets. There is a built in proxy rotation to prevent your ip from being blacklisted.

twitterwebhook for discord uses SQLite3, MySQL, bs4, requests and asyncio

make sure you have all the libraries that are imported in the python files. 

you only need to run the tweethook.py. Make sure you put your discord webhoook url, the twitter handles, and your MySQL connection info(if no MySQL connection or error to MySQL conenction, it will default to SQLite3)

## RUN 
```pip install -r requirements.txt```\
or\
```pip install pipenv```\
```pipenv install -r requirements.txt```

## RUN IN DOCKER

cd into directory and setup config.py\
run : ```docker-compose up -d```

you can try docker-compose up without -d to check logs. But it will stop the container once you exit.
