FROM python:3.8.16-slim-bullseye
LABEL maintainer="zeenfts"

ENV KAFKA_HOME=/usr/producer

RUN apt-get -yqq update && apt-get -yqq install git
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir

WORKDIR $KAFKA_HOME
# VOLUME /usr

VOLUME ../app/producer.py :/usr/producer/producer.py

RUN pip install confluent_kafka
RUN pip install --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# RUN pip install --no-cache-dir -r requirements.txt
# RUN chmod 755 ./script/run_app.sh

# RUN chmod +x ./script/run_app.sh
ENTRYPOINT ["python", "./producer.py"]