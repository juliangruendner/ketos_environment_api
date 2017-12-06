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
from cerberus import Validator

parser = reqparse.RequestParser()
parser.add_argument('dataUrl', type=str, required=True, location='args')



def feature_set_validator(value):
   FEATURE_SET_SCHEMA = {
       'resource': {'required': True, 'type': 'string'},
        'key': {'required': True, 'type': 'string'},
        'value': {'required': True,'type': 'string'}
       }
   v = Validator(FEATURE_SET_SCHEMA)
   if v.validate(value):
       return value
   else:
       raise ValueError(json.dumps(v.errors))


class MlModelExecutorResource(Resource):
    
    def __init__(self):
        super(MlModelExecutorResource, self).__init__()

    def abort_if_ml_model_doesnt_exist(self, model_id):
        abort(404, message="model {} doesn't exist".format(model_id))

    def get(self, model_id):
        args = parser.parse_args()
        data_url = args['dataUrl']
        model_dir_path = '/mlenvironment/' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        nb_dir = model_dir_path + '/'
        nb_filepath = nb_dir + 'model.ipynb'

        nb_processor = KetosNotebookProcessor(timeout=600, kernel_name='ir')
        nb_processor.ketos_set_notebook(nb_filepath)
        nb_processor.ketos_insert_data_url(data_url)
        nb_processor.ketos_execute_notebook_cells(nb_dir)
        prediction = nb_processor.ketos_get_nb_output()

        return {'model_name': 'mlmodel_' + str(model_id), 'data_url': data_url, 'prediction': prediction}, 201


    def delete(self, model_id):

        model_dir_path = '/mlenvironment/mlmodel_' + str(model_id)

        if not os.path.isdir(model_dir_path):
            self.abort_if_ml_model_doesnt_exist(model_id)

        shutil.rmtree(model_dir_path)

        return 'model' + str(model_id) + ' was removed', 201


    def post(self,model_id):
        crawler_parser = reqparse.RequestParser()
        crawler_parser.add_argument('patient_ids', type = str, action = 'append', required = True, help = 'patient ids missing', location = 'json')
        crawler_parser.add_argument('feature_set', type = feature_set_validator, action='append', required = True, help = 'feature set missing', location = 'json')
        args = crawler_parser.parse_args()
        feature_set = args['feature_set']
        
        return feature_set, 201



        