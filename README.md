# mlService Docker API

the mlService Docker Api provides a restfulApi which can be installed on a docker container to provice an interface, which allows you
to interact with your docker container an create mlService specific structures as well as call finished mlModels and load Data into the container.

The Docker Api is part of the larger mlService project for creation and deployment of ML Models accross hosptials.

## General Remarks
The implementation of the docker api is based on the flaskRestful library
[Flask-RESTful](http://flask-restful.readthedocs.io/en/latest/) as framework to build our REST-APIs.
The implementation is based on this [tutorial](https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful)
and the respective [python file](https://github.com/miguelgrinberg/REST-tutorial/blob/master/rest-server-v2.py).


## Structure
- docker/: All files that are needed to deploy the webservice as docker container
- src: Python file for starting the Flask-RESTful-Server
    - resources/: All resources that are offered by the REST-API
    - ...

## Deploying the Server
To deploy the server just clone [this repo](https://github.com/juliangruendner/mlService_webserviceBase/)
then execute the "startDev.sh" to start your devlopment environment

If you want to extend the functionality of the server just create a new resource in the [resources-directory](src/resources/).
Then import the new resource in the [API-file](src/api.py) and add the resource to the *api*-object by using the *add_resource*-function.

## Testing the server
After you have started the server you can test it by sending http requests.
If the server is running on your local machine you could for instance execute the following [curl](https://curl.haxx.se/)-requests:
- get:
```
curl http://localhost:5000/tests
```

- post:
```
curl -H "Content-Type: application/json" http://localhost:5000/tests -d '{"my_id":24, "test_field1":"Testerama"}' -X POST -v
```

## POSTMAN to work with the api
for a deeper understanding of the API we have also included a postman json ("mlService_dockerApi.postman_collection.json"),
which can be imported to your postman client (https://www.getpostman.com/) and works with your local development environment.

