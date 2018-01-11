from flask_restful import abort
from flask_restful_swagger_2 import swagger, Resource
import subprocess
import uuid

class JupyterResource(Resource):
    def __init__(self):
        super(JupyterResource, self).__init__()

    def abort_if_jupyter_running(self):
        abort(400, message="jupyter notebook is already running - no new jupyter was started")

    def get(self):
        return get_running_jupyters()

    def post(self):

        notebook_list = get_running_jupyters()
        
        if len(notebook_list) > 0 :
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