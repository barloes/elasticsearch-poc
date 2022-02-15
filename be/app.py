# save this as app.py
from flask import *
import boto3
from flask_cors import CORS
import os
from tika import parser
from elasticsearch import Elasticsearch
from flask_apscheduler import APScheduler
import re

scheduler = APScheduler()
app = Flask(__name__)
scheduler.init_app(app)
scheduler.start()
CORS(app)

app.secret_key = "super secret key"

# GET ENV
S3_NAME = os.getenv("S3_NAME")
S3_LINK = os.getenv("S3_LINK")
ES_ENDPOINT = os.getenv("ES_ENDPOINT")
ES_INDEX = os.getenv("ES_INDEX")

es_client = Elasticsearch(ES_ENDPOINT)


@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({"msg": "aaHelloWorld"})


# return list containing file name
def list_objects_s3():
    s3_client = boto3.client("s3")
    response = s3_client.list_objects(Bucket=S3_NAME)["Contents"]

    obj_list = [obj["Key"] for obj in response]
    return obj_list


# get object content
def get_object_content_s3(object_name):
    def format_text(text):
        formatted_text = re.sub(
            r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt", " ", text
        )
        formatted_text = re.sub(" +", " ", formatted_text)
        return formatted_text

    s3_client = boto3.client("s3")
    response = s3_client.get_object(
        Bucket=S3_NAME,
        Key=object_name,
    )["Body"].read()

    content = format_text(parser.from_buffer(response)["content"])

    return content


# es status check
@app.route("/es", methods=["GET"])
def healthcheck_es():
    return jsonify({"msg": es_client.info()})


# search based on query and return list of objs consisting of name and link
@app.route("/search", methods=["GET"])
def get_search_es():
    q = request.args.get("q")

    query_body = q if q != "" else "*"
    query = {"query_string": {"query": query_body, "default_field": "text"}}

    res = es_client.search(index=ES_INDEX, query=query)
    obj_list = convert_es_res_to_obj_list(res)

    return jsonify({"result": obj_list})


def convert_es_res_to_obj_list(res):
    obj_list = []

    content = [obj["_source"] for obj in res["hits"]["hits"]]
    for obj in content:
        if "name" in obj:
            # app.logger.info(obj)
            obj = {"name": obj["name"], "link": f"{S3_LINK}{obj['name']}"}
            obj_list.append(obj)

    return obj_list


# get req to manually update index
@app.route("/es/add", methods=["GET"])
def get_update_es():
    # get file name
    try:
        upsert_index_es()

        return jsonify({"msg": str("insertion complete")})
    except Exception as e:
        return jsonify({"msg": str(e)})


# cron job to update index
@scheduler.task("cron", id="update_es", minute="*")
def upsert_index_es():
    # get file name
    name_list = list_objects_s3()
    for name in name_list:
        app.logger.info(f"processing {name}")
        obj_content = get_object_content_s3(name)
        doc = {
            "name": name,
            "text": obj_content,
        }
        res = es_client.update(
            index=ES_INDEX, id=name, body={"doc": doc, "doc_as_upsert": True}
        )

        app.logger.info(res)


# api to manually delete index
@app.route("/es/del", methods=["GET"])
def delete_index_es():
    res = es_client.indices.delete(index=ES_INDEX, ignore=[400, 404])
    return jsonify({"msg": str(res)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
