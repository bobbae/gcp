import random, json
from flask import jsonify

def randomgen(request):
    randomNum = random.randint(1,100)
    output = {"random":randomNum}
    return jsonify(output)
