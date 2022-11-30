FROM python:3.8

ADD main.py .

ADD application_default_credentials.json .

RUN pip install google-cloud-storage

CMD [ "python", "./main.py" ]