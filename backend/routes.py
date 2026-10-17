from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = [datum for datum in data if datum["id"] == id]
    print(picture)
    if len(picture) > 0:
        return jsonify(picture[0]), 200
    else:
        return jsonify([]), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture, status_code = get_picture_by_id(request.json["id"])
    if status_code == 200:
        return jsonify({"Message": f"picture with id {request.json['id']} already present"}), 302
    else:
        data.append(request.json)
        return jsonify(data[-1]), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture, status_code = get_picture_by_id(request.json["id"])
    if status_code == 404:
        return jsonify({"message": "picture not found"}), 404
    else:
        picture = [datum for datum in data if datum["id"] == request.json["id"]]
        data.remove(picture[0])
        data.append(request.json)
        return jsonify(data[-1]), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture, status_code = get_picture_by_id(id)
    if status_code == 404:
        return jsonify({"message": "picture not found"}), 404
    else:
        picture = [datum for datum in data if datum["id"] == id]
        data.remove(picture[0])
        return jsonify(""), 204
