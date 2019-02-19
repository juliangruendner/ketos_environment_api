#!/bin/bash
cd /mlenvironment
# su jupyter bash -c 'jupyter notebook --ip=0.0.0.0 --port=8000 --NotebookApp.token=$1 &'
chown -R jovyan:users /mlenvironment
mkdir /home/jovyan/auth
cp ./auth/* /home/jovyan/auth
chown -R jovyan:users /home/jovyan/auth

/usr/local/bin/start-notebook.sh --NotebookApp.token="$1" --port=8000 --certfile='~/auth/jupytercert.pem' --keyfile '~/auth/jupyterkey.pem' &
chown -R jovyan:users /home/jovyan/.local/share/jupyter