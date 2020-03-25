FROM python:3.6

ADD . / TWITTERWEBHOOK/

RUN pip install pipenv && \
    cd TWITTERWEBHOOK && \
    pipenv install -r requirements.txt


CMD cd TWITTERWEBHOOK && \
    pipenv run python tweethook.py