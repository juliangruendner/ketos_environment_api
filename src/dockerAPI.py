from flask import Flask
from flask_restful_swagger_2 import Api
# from rdb.rdb import connect_to_db, create_all
from resources.mlModelResource import MlModelListResource, MlModelResource
from resources.jupyterResource import JupyterResource
from resources.mlModelExecutorResource import MlModelExecutorResource
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)  # this will allow cross-origin requests; needed for http://localhost:4999 in swaggerResource to access whole api output
api = Api(app, add_api_spec_resource=True, api_version='0.0', api_spec_url='/api/swagger')  # Wrap the Api and add /api/swagger endpoint

api.add_resource(MlModelListResource, '/models', endpoint='models')
api.add_resource(MlModelResource, '/models/<int:model_id>', endpoint='model')
api.add_resource(JupyterResource, '/jupyter', endpoint='jupyter')
api.add_resource(MlModelExecutorResource, '/models/<string:model_id>/execute', endpoint='executor')

if __name__ == '__main__':
    # connect_to_db(app, 'postgresql://mad:MAD@db:5432/mad')
    # create_all()
    # set debug false in production mode
    app.run(debug=True, host='0.0.0.0', port=5000)
