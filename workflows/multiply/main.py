import random, json
from flask import jsonify

def multiply(request):
    request_json = request.get_json()
    output = {"multiplied":2*request_json['input']}
    return jsonify(output)
