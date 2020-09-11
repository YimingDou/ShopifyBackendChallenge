from flask import jsonify


def error_response(msg, code=400):
    return jsonify({"msg": msg}), code


def success_response(msg, code=200):
    return jsonify({"msg": msg}), code


def token_response(access_token):
    return jsonify(access_token=access_token), 200
