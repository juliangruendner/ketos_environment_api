cd /mlenvironment
su jupyter bash -c 'jupyter notebook --ip=0.0.0.0 --port=8000 --NotebookApp.token=$1 &> jupyterToken.txt &'