FROM python:3.6

WORKDIR /tweethook/

COPY . .

RUN pip install pipenv && \
    pipenv install -r requirements.txt


CMD pipenv run python -u tweethook.py