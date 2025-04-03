"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()  
        users_list = [user.serialize() for user in users] 
        
        return jsonify(users_list), 200
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
#people Endpoints
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    people_list = [character.serialize() for character in people] 
    return jsonify(people_list), 200 

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_by_id(people_id):
    try:
        person = People.query.get(people_id) 
        if person is None:
            return jsonify({"error": "Character not found"}), 404

        return jsonify(person.serialize()), 200 
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

#Planet Endpoints

@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()  # Ensure the correct model name
        planets_list = [planet.serialize() for planet in planets]  # Correct variable name
        return jsonify(planets_list), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['GET']) 
def get_planet_by_id(planet_id): 
    try:
        planet= Planet.query.get(planet_id)  
        if planet is None: 
            return jsonify({"error": "Planet not found"}), 404 

        return jsonify(planet.serialize()), 200  
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
