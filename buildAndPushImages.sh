cd docker/alpine_jupyter_r
docker build -t gruendner.de:5043/mlservicecontainer_r .
cd ..
docker build -f Dockerfile.API.prod -t gruendner.de:5043/mlservicecontainer_prod_r .
docker push gruendner.de:5043/mlservicecontainer_r
docker push gruendner.de:5043/mlservicecontainer_prod_r
