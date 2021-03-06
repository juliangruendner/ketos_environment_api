from flask_restful import reqparse, abort
from flask_restful_swagger_2 import swagger, Resource
import os
import shutil
import json
from ketosJupyter.ketosNotebookProcessor import KetosNotebookProcessor
from cerberus import Validator
from util.brainApiAccess import BrainApiAccess

parser = reqparse.RequestParser()
parser.add_argument('dataUrl', type=str, required=True, location='args')

def feature_set_validator(value):
    FEATURE_SET_SCHEMA = {
        'resource': {'required': True, 'type': 'string'},
        'key': {'required': True, 'type': 'string'},
        'value': {'required': True, 'type': 'string'}
    }
    v = Validator(FEATURE_SET_SCHEMA)
    if v.validate(value):
        return value
    else:
        raise ValueError(json.dumps(v.errors))


class MlModelExecutorResource(Resource):
    @BrainApiAccess()
    def __init__(self):
        super(MlModelExecutorResource, self).__init__()

    def abort_if_ml_model_doesnt_exist(self, model_id):
        abort(404, message="model {} doesn't exist".format(model_id))

    @swagger.doc({
        "summary": "execute a model with given input data url",
        "tags": ["model executor"],
        "produces": [
            "application/json"
        ],
        "description": 'Get information about a specific model.',
        "parameters": [
            {
                "name": "model_id",
                "in": "path",
                "type": "string",
                "description": "The ID of the model to be executed",
                "required": True
            },
            {
                "name": "dataUrl",
                "in": "query",
                "type": "string",
                "description": "the url from which the data can be downloaded as csv file",
                "required": True
            }
        ],
        "responses": {
            "200": {
                "description": "the model name, data url and a list of prediction as json"
            }
        }
    })
    def get(self, model_id):
        args = parser.parse_args()
        data_url = args['dataUrl']
        model_dir_path = '/mlenvironment/models/' + str(model_id)

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
