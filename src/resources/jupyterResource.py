from flask_restful import abort
from flask_restful_swagger_2 import swagger, Resource
import subprocess
import uuid

class JupyterResource(Resource):
    def __init__(self):
        super(JupyterResource, self).__init__()

    def abort_if_jupyter_running(self):
        abort(400, message="jupyter notebook is already running - no new jupyter was started")

    @swagger.doc({
        "summary": "get the currently running jupyters",
        "tags": ["jupyter notebook"],
        "produces": [
            "application/json"
        ],
        "description": 'gets the jupyter notebooks currently running on the environment',
        "responses": {
            "200": {
                "description": "a list of the currently running jupyters as json"
            }
        }
    })
    def get(self):
        return get_running_jupyters(), 200

    @swagger.doc({
        "summary": "start jupyter notebook for environment",
        "tags": ["jupyter notebook"],
        "produces": [
            "application/json"
        ],
        "description": 'start a jupyter notebook if it does not yet exist',
        "responses": {
            "200": {
                "description": "the token of the newly running jupyter notebook as json"
            },
            "400": {
                "description": "jupyter was already running and could not be created"
            }
        }
    })
    def post(self):

        notebook_list = get_running_jupyters()

        if len(notebook_list) > 0:
            return self.abort_if_jupyter_running()

        jupyter_token = uuid.uuid4().hex
        subprocess.run(["./startJupyter.sh", str(jupyter_token)], shell=True)

        return {"jupyter_token": jupyter_token}, 201


def get_running_jupyters():
    notebook_list = []
    process = subprocess.Popen("./listJupyter.sh", stdout=subprocess.PIPE, shell=True)
    line = process.stdout.readline().decode("utf-8").strip()

    while line != '':
        if '::' in line:
            notebook_list.append(line)
        line = process.stdout.readline().decode("utf-8").strip()

    return notebook_list
