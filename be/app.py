# save this as app.py
from flask import *
from datetime import datetime
import boto3
from flask_cors import CORS
import time
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    create_access_token,
)
from datetime import timedelta

app = Flask(__name__)
CORS(app)
app.secret_key = "super secret key"


@app.route("/", methods=["GET"])
def healthcheck():
    return Response(status=200)

@app.route("/hello", methods=["GET"])
def helloWorld():
    return jsonify({"msg": "HelloWorld"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
