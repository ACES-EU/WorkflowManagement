FROM python:3.12-slim

WORKDIR /opt/setup

COPY config/scripts .

RUN pip install -r requirements.txt && rm requirements.txt

CMD bash run.sh