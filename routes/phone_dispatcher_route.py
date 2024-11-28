from flask import Blueprint, request, jsonify, current_app
from repo.phone_dispatcher_repo import Neo4jConnection

phone_blueprint = Blueprint('phone_blueprint', __name__, url_prefix='/api/phone_tracker')


@phone_blueprint.route('/interaction', methods=['POST'])
def create_interaction():
    interaction_data = request.get_json()
    if not interaction_data:
        return jsonify({"error": "No data provided"}), 400

    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        interaction_id = repo.create_interaction(interaction_data)
        return jsonify({"interaction_id": interaction_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()


@phone_blueprint.route("/bluetooth-connections", methods=['GET'])
def get_bluetooth_connections():
    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        connections = repo.get_bluetooth_connections()
        return jsonify({"connections": connections}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()


@phone_blueprint.route("/strong-connections", methods=['GET'])
def get_strong_connections():
    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        connections = repo.get_strong_connections()
        return jsonify({"connections": connections}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()


@phone_blueprint.route("/device/<device_id>/connections", methods=['GET'])
def count_device_connections(device_id):
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400

    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        count = repo.count_device_connections(device_id)
        return jsonify({"device_id": device_id, "connection_count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()


@phone_blueprint.route("/direct-connection/<device1_id>/<device2_id>", methods=['GET'])
def check_direct_connection(device1_id, device2_id):
    if not device1_id or not device2_id:
        return jsonify({"error": "Both device IDs are required"}), 400

    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        has_connection = repo.check_direct_connection(device1_id, device2_id)
        return jsonify({"has_direct_connection": has_connection}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()


@phone_blueprint.route("/device/<device_id>/latest-interaction", methods=['GET'])
def get_latest_interaction(device_id):
    if not device_id:
        return jsonify({"error": "Device ID is required"}), 400

    repo = Neo4jConnection(current_app.config['NEO4J_DRIVER'])
    try:
        result = repo.get_latest_interaction(device_id)
        return jsonify({"latest_interaction": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        repo.close()
