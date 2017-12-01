from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from rdb.models.user import User, get_user_by_username
from rdb.rdb import db
from flask_httpauth import HTTPBasicAuth
import os
from os import listdir
from os.path import isdir
import shutil
from nbformat import v4
import json
import IPython
from ketosJupyter.ketosNotebookProcessor import KetosNotebookProcessor

parser = reqparse.RequestParser()
parser.add_argument('dataUrl', type=str, required=True, location='args')

class MlModelExecutorResource(Resource):
    def __init__(self):
        super(MlModelExecutorResource, self).__init__()

    def abort_if_ml_model_doesnt_exist(self, model_id):
        abort(404, message="model {} doesn't exist".format(model_id))


    def get(self, model_id):
        args = parser.parse_args()
        data_url = args['dataUrl']
        model_dir_path = '/mlenvironment/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        nb_dir = model_dir_path + '/'
        nb_filepath = nb_dir + 'model.ipynb'

        nb_processor = KetosNotebookProcessor(timeout=600, kernel_name='ir')
        nb_processor.ketos_set_notebook(nb_filepath)
        nb_processor.ketos_insert_data_url('http://localhost:9000/mytest/url/awesome')
        nb_processor.ketos_executeNotebookCells(nb_dir)
        prediction = nb_processor.ketos_get_nb_output()

        return {'model_name': 'mlmodel_' + str(model_id), 'data_url': data_url, 'prediction': str(prediction)}, 201


    def delete(self, model_id):

        model_dir_path = '/mlenvironment/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        shutil.rmtree(model_dir_path)

        return 'model' + str(model_id) + ' was removed', 201
