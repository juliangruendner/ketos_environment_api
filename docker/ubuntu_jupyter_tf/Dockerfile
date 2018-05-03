FROM ubuntu:latest

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get update \
    && apt-get install -y software-properties-common curl \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get remove -y software-properties-common \
    && apt autoremove -y \
    && apt-get update \
    && apt-get install -y python3.6 \
    && curl -o /tmp/get-pip.py "https://bootstrap.pypa.io/get-pip.py" \
    && python3.6 /tmp/get-pip.py \
    && apt-get remove -y curl \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y cmake \
    && apt-get install -y unzip \
    && pip install --upgrade pip 

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
	#&& echo "c.NotebookApp.token = ''" > /root/.jupyter/jupyter_notebook_config.py \
    && echo "c.NotebookApp.token = ''\nc.FileContentsManager.delete_to_trash = False" > /root/.jupyter/jupyter_notebook_config.py \
	&& cd /opt && rm -r /opt/tmp && mkdir -p /opt/notebook \
	&& unset CC CXX \
	&& rm -r /root/.cache \
	&& find /usr/lib/python3.6/ -type d -name tests -depth -exec rm -rf {} \; \
	&& find /usr/lib/python3.6/ -type d -name test -depth -exec rm -rf {} \; \
	&& find /usr/lib/python3.6/ -name __pycache__ -depth -exec rm -rf {} \;

RUN apt-get update \
    && apt-get install -y python-pip build-essential \
    && apt-get -y autoremove \
    && apt-get -y clean  \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y python-psycopg2

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib

ARG TENSORFLOW_VERSION=1.7.0
ARG TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-${TENSORFLOW_VERSION}-cp36-cp36m-linux_x86_64.whl

RUN pip3 --no-cache-dir install --upgrade ${TF_BINARY_URL}

RUN pip install --upgrade pip \
    && pip install pip -U \
    && pip install jupyter numpy scipy pandas sklearn matplotlib tensorflow psycopg2 psycopg2-binary\ 
    && rm -r /root/.cache/pip

# add new user with home directory in /mlenvironment
RUN mkdir /mlenvironment  \
    && adduser -h /mlenvironment -D jupyter
