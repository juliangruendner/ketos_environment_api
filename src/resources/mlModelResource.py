import json
import os
import shutil
import subprocess
from os import listdir
from os.path import isdir

import IPython
import nbformat
from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_restful import abort, fields, marshal_with, reqparse
from flask_restful_swagger_2 import swagger, Resource
from nbformat import v4
from rdb.models.user import User, get_user_by_username
from rdb.rdb import db


class MlModelListResource(Resource):
    def __init__(self):
        super(MlModelListResource, self).__init__()

    def get(self):

        dirPath = '/mlenvironment/'
        models = []

        for dir in listdir(dirPath):
            if isdir(dirPath + dir) and dir.find('mlmodel_') != -1:
                models.append(dir)

        return models


    def post(self):

        dirPath = '/mlenvironment/'

        models = []

        for dir in listdir(dirPath):
            if isdir(dirPath + dir) and dir.find('mlmodel_') != -1:
                models.append(dir[8::])

        models = sorted(models, key=int, reverse=True)
        if len(models)  == 0:
            new_model_n = 1
        else:
            new_model_n = int(models[0]) + 1

        new_model_dir = dirPath + '/mlmodel_' + str(new_model_n)
        create_model_dir(new_model_dir)

        modelFiles = []
        for file in listdir(new_model_dir + '/'):
            modelFiles.append(file)

        return {'modelName': 'mlmodel_' + str(new_model_n), 'modelFiles': modelFiles}, 201


class MlModelResource(Resource):
    def __init__(self):
        super(MlModelResource, self).__init__()

    def abort_if_ml_model_doesnt_exist(self, model_id):
        abort(404, message="model {} doesn't exist".format(model_id))


    def get(self, model_id):
        model_dir_path = '/mlenvironment/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        modelFiles = []
        for file in listdir(model_dir_path + '/'):
            modelFiles.append(file)

        with open(model_dir_path + '/model.ipynb') as nbf:
            nb = nbformat.read(nbf, as_version=4)

        return {'model_name': 'mlmodel_' + str(model_id), 'model_files': modelFiles, 'model_notebook': nb}, 201


    def delete(self, model_id):
        model_dir_path = '/mlenvironment/mlmodel_' + str(model_id)
        
        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        shutil.rmtree(model_dir_path)

        return 'model' + str(model_id) + ' was removed', 201
    

def create_model_dir(model_dir):

    os.mkdir(model_dir)
    shutil.chown(model_dir, 'jupyter')
    os.chmod(model_dir, 0o664)

    if os.path.exists('/ketos_data/ketos_predict_example.csv'):
        model_path = model_dir + '/ketos_predict_example.csv'
        shutil.copyfile('/ketos_data/ketos_predict_example.csv', model_path)
        shutil.chown(model_path, 'jupyter')
        os.chmod(model_path, 0o664)

    if os.path.exists('/ketos_data/model.ipynb'):
        model_path = model_dir + '/model.ipynb'
        shutil.copyfile('/ketos_data/model.ipynb', model_path)
        shutil.chown(model_path, 'jupyter')
        os.chmod(model_path, 0o664)
    else:
        fd = open(model_path + '/model.ipynb', 'w')
        os.chmod(model_path + '/model.ipynb', 0o664)

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
