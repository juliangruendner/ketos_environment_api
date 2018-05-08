FROM ubuntu:latest

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get -y install python3.3 python3-pip python-dev && pip3 install jupyter \
	&& apt-get install -y libzmq3-dev

RUN apt-get update \
    && apt-get install -y python-psycopg2

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib \
	&& apt-get install postgresql-client 

#RUN apt-get install -y python-opencv

RUN pip3 install tensorflow \
	&& pip3 install numpy scipy pandas sklearn matplotlib psycopg2 psycopg2-binary

RUN jupyter nbextension enable --py widgetsnbextension \
	&& echo "c.NotebookApp.token = ''" > /root/.jupyter/jupyter_notebook_config.py

RUN adduser --home /mlenvironment --disabled-password --gecos "" jupyter \
	&& mkdir /mlenvironment/models \
	&& su - jupyter

