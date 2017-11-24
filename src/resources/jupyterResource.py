from flask_restful import Resource
import subprocess
import uuid

class JupyterResource(Resource):
    def __init__(self):
        super(JupyterResource, self).__init__()

    # @marshal_with(user_fields)
    def get(self):

        notebook_list = []

        process = subprocess.Popen("./listJupyter.sh", stdout=subprocess.PIPE, shell=True)
        line = process.stdout.readline().decode("utf-8").strip()

        while line != '':
            if '::' in line:
                notebook_list.append(line)
            line = process.stdout.readline().decode("utf-8").strip()

        return notebook_list

    # @marshal_with(query_fields)
    def post(self):

        jupyter_token = uuid.uuid4().hex
        subprocess.run(["./startJupyter.sh", str(jupyter_token)], shell=True)

        return {"jupyter_token": jupyter_token}, 201