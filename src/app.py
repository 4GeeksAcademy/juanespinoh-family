"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({"first_name":"John","age":33,"lucky_numbers":[7,13,22]})
jackson_family.add_member({"first_name":"Jane","age":35,"lucky_numbers":[10,14,3]})
jackson_family.add_member({"first_name":"Jimmy","age":5,"lucky_numbers":[1]})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {

        "family": members
    }
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def add_member():
    data=request.get_json()

    first_name=data.get("first_name", None)
    age=data.get("age", None)
    lucky_numbers=data.get("lucky_numbers", None)
    id=data.get("id", None)

    if not first_name or not age or not lucky_numbers:
        return jsonify({"msg":"faltan campos por agregar"}), 400
    
    reulst=jackson_family.add_member({'first_name':first_name,'age':age,'lucky_numbers':lucky_numbers,'id':id})
    # this is how you can use the Family datastructure by calling its methods

    response_body = {
        "result": reulst,

    }
    return jsonify(reulst), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def del_member(id):

    
    reulst=jackson_family.delete_member(id)
    # this is how you can use the Family datastructure by calling its methods

    response_body = {
        "result": reulst,

    }
    return jsonify({"done":True}), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_single_member(id):
    reulst=jackson_family.get_member(id)
    # this is how you can use the Family datastructure by calling its methods

    response_body = {
        "result": reulst,

    }
    return jsonify(reulst), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
