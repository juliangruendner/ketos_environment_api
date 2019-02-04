FROM jupyter/r-notebook:latest

USER root
RUN sudo apt-get update
RUN sudo apt-get install gnupg -y

# install r and datashield dev packages
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E084DAB9

RUN apt-get update && \
apt-get install -y r-base r-base-dev && \
apt-get install -y libcurl4-openssl-dev && \
apt-get install -y libxml2-utils && \
apt-get install -y libxml2-dev

# install opal packages
RUN R -e 'install.packages(c("rjson", "RCurl", "mime"), repos="https://cran.uni-muenster.de/")' && \
R -e 'install.packages("opal", repos="http://cran.obiba.org", type="source", dependencies=TRUE)' && \
R -e 'install.packages("opaladmin", repos="http://cran.obiba.org", type="source")'

# install datashield packages
RUN R -e "install.packages('datashieldclient', repos=c('https://cran.uni-muenster.de/', 'http://cran.obiba.org'), dependencies=TRUE)"

# install packages needed for development
RUN R -e "install.packages('devtools',repos=c('https://cran.uni-muenster.de/', 'http://cran.obiba.org'), dependencies = TRUE)" && \
R -e "install.packages('roxygen2', repos=c('https://cran.uni-muenster.de/', 'http://cran.obiba.org'),dependencies = TRUE)" && \
R -e "install.packages('Rtools',repos=c('https://cran.uni-muenster.de/', 'http://cran.obiba.org'), dependencies = TRUE)"

# update obiba packages
RUN R -e 'update.packages(repos="http://cran.obiba.org")'

RUN mkdir /mlenvironment && \
mkdir /mlenvironment/models

RUN mkdir -p /home/jovyan/.local/share/jupyter

RUN chown -R jovyan:users /mlenvironment
RUN chown -R jovyan:users /home/jovyan/.local

#add R example notebook
RUN mkdir /ketos_data
ADD ./model.ipynb /ketos_data
ADD ./ketos_predict_example.csv /ketos_data