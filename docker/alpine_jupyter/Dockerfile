FROM alpine:latest

MAINTAINER eip
# docker run -d --name alpine-jupyter-01 -p 8888:8888 -v [host-src]:/opt/notebook eipdev/alpine-jupyter-notebook

ENV LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add --no-cache tini python3 libstdc++ openblas freetype wget ca-certificates
RUN python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip
RUN pip3 install --upgrade pip setuptools
RUN apk add --no-cache --virtual .build-deps@testing python3-dev make cmake clang clang-dev g++ linux-headers openblas-dev freetype-dev
RUN export CC=/usr/bin/clang CXX=/usr/bin/clang++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN mkdir -p /opt/tmp && cd /opt/tmp \
	&& pip3 download -d /opt/tmp numpy \
	&& unzip -q numpy*.zip \
	&& cd numpy* && echo "Building numpy..." \
	&& echo -e "[ALL]\nlibrary_dirs = /usr/lib\ninclude_dirs = /usr/include\n[atlas]\natlas_libs = openblas\nlibraries = openblas\n[openblas]\nlibraries = openblas\nlibrary_dirs = /usr/lib\ninclude_dirs = /usr/include\n" > site.cfg \
	&& python3 setup.py build -j 4 install &> /dev/null && echo "Successfully installed numpy" \
	&& cd /opt/tmp \
	&& echo "Downloading opencv" && wget --quiet https://github.com/opencv/opencv/archive/3.3.1.zip \
	&& unzip -q 3.3.1.zip \
	&& cd opencv* \
	&& mkdir build && cd build && echo "Building opencv..." \
	&& cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr \
		-D INSTALL_C_EXAMPLES=OFF \
		-D INSTALL_PYTHON_EXAMPLES=OFF \
		-D WITH_FFMPEG=NO \
		-D WITH_IPP=NO \
		-D WITH_OPENEXR=NO \
		-D WITH_WEBP=NO \
		-D WITH_TIFF=NO \
		-D WITH_JASPER=NO \
		-D BUILD_EXAMPLES=OFF \
		-D BUILD_PERF_TESTS=NO \
		-D BUILD_TESTS=NO .. &> /dev/null \
	&& make &> /dev/null && make install &> /dev/null && echo "Successfully installed opencv" \
	&& pip3 install --upgrade matplotlib jupyter ipywidgets \
	&& jupyter nbextension enable --py widgetsnbextension \
	&& echo "c.NotebookApp.token = ''" > /root/.jupyter/jupyter_notebook_config.py \
	&& cd /opt && rm -r /opt/tmp && mkdir -p /opt/notebook \
	&& unset CC CXX \
	&& apk del .build-deps \
	&& rm -r /root/.cache \
	&& find /usr/lib/python3.6/ -type d -name tests -depth -exec rm -rf {} \; \
	&& find /usr/lib/python3.6/ -type d -name test -depth -exec rm -rf {} \; \
	&& find /usr/lib/python3.6/ -name __pycache__ -depth -exec rm -rf {} \;

#install bash
RUN apk update && apk upgrade && apk add bash && apk add postgresql-dev && apk add py3-psycopg2

# add new user with home directory in /mlenvironment
RUN mkdir /mlenvironment && \
mkdir /mlenvironment/models && \
adduser -h /mlenvironment -D jupyter && \
su - jupyter && \
touch train.R predict.R save.R load.R data.json

#EXPOSE 8888
#WORKDIR /opt/notebook
#ENTRYPOINT ["/sbin/tini", "--"]
#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
