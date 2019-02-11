#!/bin/bash
cd /mlenvironment
# su jupyter bash -c 'jupyter notebook --ip=0.0.0.0 --port=8000 --NotebookApp.token=$1 &'
chown -R jovyan:users /mlenvironment
/usr/local/bin/start-notebook.sh --NotebookApp.token="$1" --port=8000 &
chown -R jovyan:users /home/jovyan/.local/share/jupyter