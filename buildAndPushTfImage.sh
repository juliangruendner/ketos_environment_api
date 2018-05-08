cd docker/ubuntu_jupyter_tf
docker build -t gruendner.de:5043/mlservicecontainer_tf .

cd ..
docker build -f Dockerfile.API.prodTf -t gruendner.de:5043/mlservicecontainer_prod_tf .
docker push gruendner.de:5043/mlservicecontainer_tf
docker push gruendner.de:5043/mlservicecontainer_prod_tf
