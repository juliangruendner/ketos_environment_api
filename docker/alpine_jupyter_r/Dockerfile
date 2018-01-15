FROM alpine_jupyter:latest

RUN apk update
RUN apk add --no-cache R R-dev R-doc curl libressl-dev curl-dev libxml2-dev gcc g++ git coreutils bash ncurses
RUN apk add zeromq-dev

RUN git clone https://github.com/ropensci/git2r.git &&\
R CMD INSTALL --configure-args="--with-libssl-include=/usr/lib/" git2r &&\
rm -rf git2r /tmp/*


RUN R -q -e "install.packages(c('backports', 'mime', 'curl', 'openssl', 'magrittr', 'lazyeval', 'assertthat', 'rprojroot', 'BH', 'httr', 'memoise', 'whisker', 'digest', 'rstudioapi', 'jsonlite', 'withr', 'rex', 'crayon', 'stringr', 'stringi', 'brew', 'Rcpp', 'R6', 'desc', 'commonmark', 'xml2'), repos='https://cran.uni-muenster.de/')"

RUN R -q -e "install.packages(c('devtools', 'covr', 'roxygen2'), repos ='https://cloud.r-project.org/')" &&\
rm -rf /tmp/*

RUN R -e 'install.packages(c("git2r","httr"), repos="https://cran.uni-muenster.de/")' && \
R -e 'install.packages(c("crayon","pbdZMQ"), repos="https://cran.uni-muenster.de/")'

RUN R -e 'install.packages(c("evaluate", "uuid"), repos="https://cran.uni-muenster.de/")'

RUN R -e 'devtools::install_github(paste0("IRkernel/", c("repr", "IRdisplay", "IRkernel")))' && \
R -e 'IRkernel::installspec(user = FALSE)'

#add R example notebook
RUN chown -R jupyter:jupyter /usr/lib/R
RUN mkdir /ketos_data
ADD ./model.ipynb /ketos_data
ADD ./ketos_predict_example.csv /ketos_data