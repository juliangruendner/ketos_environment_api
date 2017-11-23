from flask import Flask
from flask_restful import Api
# from rdb.rdb import connect_to_db, create_all
from resources.testResource import TestResource
from resources.modelResource import ModelListResource
from resources.jupyterResource import JupyterResource


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


api.add_resource(TestResource, '/tests', endpoint='tests')
api.add_resource(ModelListResource, '/models', endpoint='models')
api.add_resource(JupyterResource, '/jupyter', endpoint='jupyter')

if __name__ == '__main__':
    # connect_to_db(app, 'postgresql://mad:MAD@db:5432/mad')
    # create_all()
    # set debug false in production mode
    app.run(debug=True, host='0.0.0.0', port=5000)
