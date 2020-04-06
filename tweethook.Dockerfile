FROM python:3.6
##create directory tweethook. It will auto cd in this directory when container run
WORKDIR /tweethook/
##copy current directory to workdir
COPY . .
## install dependencies
RUN pip install pipenv && \
    pipenv install -r requirements.txt
## -u to get console prints. Sometimes do not log if -u not present 
CMD pipenv run python -u tweethook.py