import json
import os
import shutil
from os import listdir
from os.path import isdir
import IPython
import nbformat
from flask_restful import abort, reqparse
from flask_restful_swagger_2 import swagger, Resource
from flask_restplus import inputs

class MlModelListResource(Resource):
    def __init__(self):
        super(MlModelListResource, self).__init__()

    @swagger.doc({
        "summary": "get all models",
        "tags": ["models"],
        "produces": [
            "application/json"
        ],
        "description": 'get all models',
        "responses": {
            "200": {
                "description": "json with info about all models "
            }
        }
    })
    def get(self):

        dirPath = '/mlenvironment/models/'
        models = []

        for dir in listdir(dirPath):
            if isdir(dirPath + dir) and dir.find('mlmodel_') != -1:
                models.append(dir)

        return models

    @swagger.doc({
        "summary": "create model",
        "tags": ["models"],
        "produces": [
            "application/json"
        ],
        "description": 'create a model',
        "parameters": [
            {
                "name": "createExampleModel",
                "in": "path",
                "type": "boolean",
                "description": "creates example model data in fileys",
                "required": False
            }
        ],
        "responses": {
            "200": {
                "description": "json with info about model and its files"
            }
        }
    })
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('createExampleModel', type=inputs.boolean, required=False, location='args')
        args = parser.parse_args()
        b_example_model = True

        if args['createExampleModel'] is None or not args['createExampleModel']:
            b_example_model = False

        dirPath = '/mlenvironment/models/'

        models = []

        for dir in listdir(dirPath):
            if isdir(dirPath + dir) and dir.find('mlmodel_') != -1:
                models.append(dir[8::])

        models = sorted(models, key=int, reverse=True)
        if len(models) == 0:
            new_model_n = 1
        else:
            new_model_n = int(models[0]) + 1

        new_model_dir = dirPath + 'mlmodel_' + str(new_model_n)
        create_model_dir(new_model_dir, b_example_model)

        modelFiles = []
        for file in listdir(new_model_dir + '/'):
            modelFiles.append(file)

        return {'modelName': 'mlmodel_' + str(new_model_n), 'modelFiles': modelFiles}, 201


class MlModelResource(Resource):
    def __init__(self):
        super(MlModelResource, self).__init__()

    def abort_if_ml_model_doesnt_exist(self, model_id):
        abort(404, message="model {} doesn't exist".format(model_id))

    @swagger.doc({
        "summary": "get info for model",
        "tags": ["model"],
        "produces": [
            "application/json"
        ],
        "description": 'Get information about a specific model.',
        "parameters": [
            {
                "name": "mode_id",
                "in": "path",
                "type": "string",
                "description": "The ID of the model to be retrieved.",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "Retrieved Model Information as json."
            }
        }
    })
    def get(self, model_id):
        model_dir_path = '/mlenvironment/models/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        modelFiles = []
        for file in listdir(model_dir_path + '/'):
            modelFiles.append(file)

        with open(model_dir_path + '/model.ipynb') as nbf:
            nb = nbformat.read(nbf, as_version=4)

        return {'model_name': 'mlmodel_' + str(model_id), 'model_files': modelFiles, 'model_notebook': nb}, 201

    @swagger.doc({
        "summary": "delete model",
        "tags": ["model"],
        "produces": [
            "application/json"
        ],
        "description": 'delete a specific model',
        "parameters": [
            {
                "name": "mode_id",
                "in": "path",
                "type": "string",
                "description": "The ID of the model to be deleted.",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "model id of model which was removed"
            }
        }
    })
    def delete(self, model_id):
        model_dir_path = '/mlenvironment/models/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        shutil.rmtree(model_dir_path)

        return 'model' + str(model_id) + ' was removed', 201


def create_model_dir(model_dir, b_example_model):

    os.mkdir(model_dir)
    shutil.chown(model_dir, 'jupyter')

    if not b_example_model:
        return

    if os.path.exists('/ketos_data/ketos_predict_example.csv'):
        model_path = model_dir + '/ketos_predict_example.csv'
        shutil.copyfile('/ketos_data/ketos_predict_example.csv', model_path)
        shutil.chown(model_path, 'jupyter')

    if os.path.exists('/ketos_data/model.ipynb'):
        model_path = model_dir + '/model.ipynb'
        shutil.copyfile('/ketos_data/model.ipynb', model_path)
        shutil.chown(model_path, 'jupyter')
    else:
        fd = open(model_path + '/model.ipynb', 'w')

        jsonform = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "R",
                    "language": "R",
                    "name": "ir"
                },
                "language_info": {
                    "codemirror_mode": "r",
                    "file_extension": ".r",
                    "mimetype": "text/x-r-source",
                    "name": "R",
                    "pygments_lexer": "r",
                    "version": "3.3.3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 2
        }

        fd.write(json.dumps(jsonform))
        fd.close()
