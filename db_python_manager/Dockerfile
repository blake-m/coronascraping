FROM python:3.8

WORKDIR /usr/src/app

RUN pip install --no-cache-dir psycopg2 flask requests pandas

COPY . .
#RUN cd ./receiver && mkdir received


EXPOSE 5000