from flask import g
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from flask_httpauth import HTTPBasicAuth
import subprocess
import time

auth = HTTPBasicAuth()

parser = reqparse.RequestParser()
parser.add_argument('my_id', type=str, location='json')
parser.add_argument('test_field1', type=str, location='json')

query_fields = {
    'my_id': fields.Integer,
    'test_field1': fields.String,
}

'''
@auth.verify_password
def verify_password(username, password):
    # is username the real username or the email
    # username: not @ contained
    # email: @ contained
    user = get_user_by_username(username)

    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
'''


class JupyterResource(Resource):
    def __init__(self):
        super(JupyterResource, self).__init__()

    # @auth.login_required
    # @marshal_with(user_fields)
    def get(self):
        return [{"test1": "test1Value", "test2": "test2Value"}]

    # @marshal_with(query_fields)
    def post(self):

        jupyter_token = "no_token_found"

        subprocess.run(["./startJupyter.sh"], shell=True)
        count = 0

        while jupyter_token == 'no_token_found' and count < 10:
            file_object = open("/mlenvironment/jupyterToken.txt", "r")

            for line in file_object:
                if "token=" in str(line):
                    beginning = line.find("token=")
                    jupyter_token = line[beginning + 6:-1]
                    break

            time.sleep(1)
            count = count + 1

        return {"jupyter_token": jupyter_token}, 201


'''
class UserResource(Resource):
    def __init__(self):
        super(UserResource, self).__init__()

    def abort_if_user_doesnt_exist(self, user_id):
        abort(404, message="user {} doesn't exist".format(user_id))

    def get_user(self, username):
        u = get_user_by_username(username)

        if not u:
            self.abort_if_user_doesnt_exist(username)

        return u

    @auth.login_required
    @marshal_with(user_fields)
    def get(self, username):
        return self.get_user(username), 200

    @auth.login_required
    @marshal_with(user_fields)
    def delete(self, username):
        u = self.get_user(username)

        db.session.delete(u)
        db.session.commit()
        return {'result': True}, 204

    @auth.login_required
    @marshal_with(user_fields)
    def put(self, username):
        u = self.get_user(username)

        args = parser.parse_args()
        u.username = args['username'].lower()
        u.email = args['email'].lower()
        u.hash_password(args['password'])
        u.first_name = args['first_name']
        u.last_name = args['last_name']

        db.session.commit()
        return u, 200

'''
