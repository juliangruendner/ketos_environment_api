from flask import Flask
from flask_restful_swagger_2 import Api
# from rdb.rdb import connect_to_db, create_all
from resources.mlModelResource import MlModelListResource, MlModelResource
from resources.jupyterResource import JupyterResource
from resources.mlModelExecutorResource import MlModelExecutorResource
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

api.add_resource(MlModelListResource, '/models', endpoint='models')
api.add_resource(MlModelResource, '/models/<int:model_id>', endpoint='model')
api.add_resource(JupyterResource, '/jupyter', endpoint='jupyter')
api.add_resource(MlModelExecutorResource, '/models/<string:model_id>/execute',endpoint='executor')

if __name__ == '__main__':
    # connect_to_db(app, 'postgresql://mad:MAD@db:5432/mad')
    # create_all()
    # set debug false in production mode
    for your_dir in '/mlenvironment':
        for root, dirs, files in os.walk(your_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)
    app.run(debug=True, host='0.0.0.0', port=5000)
