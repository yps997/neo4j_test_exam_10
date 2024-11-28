from flask import Blueprint, request, jsonify

phone_blueprint = Blueprint('phone_blueprint', __name__, url_prefix='/api/phone_tracker/')


@phone_blueprint.route('/', methods=['POST'])
def get_interaction():
   print(request.json)
   return jsonify({ }), 200
