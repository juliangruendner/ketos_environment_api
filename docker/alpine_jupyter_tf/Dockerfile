FROM alpine_jupyter:latest

# TODO Marcel Erpenbeck - install Tensorflow and add Tensorflow to jupyter notebook

RUN apk update && apk upgrade
RUN apk add python3-dev && apk add python-dev
RUN apk add --no-cache gcc musl-dev && rm -rf /var/lib/apt/lists/* && apk add g++ 
#&& apk add glib && apk add libstdc++
#RUN apk update && apk upgrade && apk add python3-dev && apk add python-dev && apk add --no-cache gcc musl-dev && rm -rf /var/lib/apt/lists/* && apk add g++ && apk add glib && apk add libstdc++

ENV LANG=C.UTF-8

# Install glibc and useful packages
RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && apk --update add \
    bash \
    curl \
    ca-certificates \
    libstdc++ \
    glib \
    libxext \
    libxrender \
    && curl "https://raw.githubusercontent.com/sgerrand/alpine-pkg-glibc/master/sgerrand.rsa.pub" -o /etc/apk/keys/sgerrand.rsa.pub \
    && curl -L "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-2.23-r3.apk" -o glibc.apk \
    && apk add glibc.apk \
    && curl -L "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.23-r3/glibc-bin-2.23-r3.apk" -o glibc-bin.apk \
    && apk add glibc-bin.apk \
    && /usr/glibc-compat/sbin/ldconfig /lib /usr/glibc/usr/lib \
    && rm -rf glibc*apk /var/cache/apk/*


# Latest Tensorflow and Keras version
ARG TENSORFLOW_VERSION=1.7.0
ARG TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-${TENSORFLOW_VERSION}-cp36-cp36m-linux_x86_64.whl
#ARG KERAS_VERSION=2.1.5


# Install Tensorflow
RUN pip3 --no-cache-dir install --upgrade ${TF_BINARY_URL}

#GPU
#pip3 --no-cache-dir install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.7.0-cp36-cp36m-linux_x86_64.whl

