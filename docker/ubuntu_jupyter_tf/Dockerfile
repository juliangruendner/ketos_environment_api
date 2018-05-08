FROM ubuntu:latest

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

#RUN apt-get update
#RUN apt-get install -y software-properties-common curl
#RUN add-apt-repository ppa:jonathonf/python-3.6
#RUN apt-get remove -y software-properties-common
#RUN apt autoremove -y
#RUN apt-get update
#RUN apt-get install -y python3.6
#RUN curl -o /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py"
#RUN python3 /tmp/get-pip.py
#RUN apt-get remove -y curl
#RUN apt autoremove -y
#RUN rm -rf /var/lib/apt/lists/*

RUN apt-get -y install python3.3 python3-pip python-dev && pip3 install jupyter && \
apt-get install -y libzmq3-dev

RUN apt-get update \
    && apt-get install -y python-psycopg2

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib

#ARG TENSORFLOW_VERSION=1.7.0
#ARG TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-${TENSORFLOW_VERSION}-cp33-cp33m-linux_x86_64.whl

#RUN pip3 --no-cache-dir install --upgrade ${TF_BINARY_URL}

RUN pip3 install tensorflow

#RUN pip3 install --upgrade pip3 \
 #   && pip3 install pip3 -U \
  #  && pip3 install jupyter numpy scipy pandas sklearn matplotlib tensorflow psycopg2 psycopg2-binary \ 
   # && rm -r /root/.cache/pip

# add new user with home directory in /mlenvironment
RUN mkdir /mlenvironment  \
    && adduser -h /mlenvironment -D jupyter
