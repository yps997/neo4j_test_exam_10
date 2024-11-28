from flask import Flask
from routes.phone_dispatcher_route import phone_blueprint
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os


load_dotenv(verbose=True)


neo4j_uri = os.getenv('NEO4J_URI')
if not neo4j_uri:
    raise ValueError("NEO4J_URI environment variable not found")

app = Flask(__name__)
app.register_blueprint(phone_blueprint)

# Initialize Neo4j driver
driver = GraphDatabase.driver(
    neo4j_uri,
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)
app.config['NEO4J_DRIVER'] = driver

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
