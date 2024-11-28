from flask import Blueprint, request, jsonify, current_app

from repo.phone_dispatcher_repo import Neo4jConnection

phone_blueprint = Blueprint('phone_blueprint', __name__, url_prefix='/api/phone_tracker/')


@phone_blueprint.route('/', methods=['POST'])
def get_interaction():
    interaction_data = request.get_json()
    print(interaction_data)
    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    interaction_id = (repo.create_interaction(interaction_data))
    return jsonify({"interaction_id": interaction_id}), 201


@phone_blueprint.route("/bluetooth-connections", methods=['GET'])
def get_bluetooth_connections():
      repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
      interaction_id = (repo.get_bluetooth_connections())
      return jsonify({"interaction_id": interaction_id}), 201


@phone_blueprint.route("/strong-connections", methods=['GET'])
def get_strong_connections():
    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    interaction_id = (repo.get_strong_connections())
    return jsonify({"interaction_id": interaction_id}), 201



@phone_blueprint.route("/device/<device_id>", methods=['GET'])
def count_device_connections(device_id):
    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    count = (repo.count_device_connections())
    return jsonify({"device_id": device_id, "connection_count": count})



