from flask import Blueprint, request, jsonify, current_app

from repo.phone_dispatcher_repo import Neo4jConnection

# db = Neo4jConnection()

phone_blueprint = Blueprint('phone_blueprint', __name__, url_prefix='/api/phone_tracker/')


@phone_blueprint.route('/', methods=['POST'])
def get_interaction():
   interaction_data = request.get_json()
   print(interaction_data)
   repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
   interaction_id = (repo.create_interaction(interaction_data))
   return jsonify({"interaction_id": interaction_id}), 201




