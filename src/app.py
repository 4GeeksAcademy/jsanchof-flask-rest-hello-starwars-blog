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
from models import db, User, People, Planet, Favorite
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

#users endpoins
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()  
        users_list = [user.serialize() for user in users] 
        
        return jsonify(users_list), 200
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        required_fields = ['username', 'email']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Optional: prevent duplicate email or username
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Username already exists"}), 400

        new_user = User(
            username=data['username'],
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.serialize()), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]

        db.session.commit()

        return jsonify(user.serialize()), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

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
    
@app.route('/planets', methods=['POST'])
def create_planet():
    try:
        data = request.get_json()

        required_fields = ['uid', 'name', 'climate', 'diameter', 'gravity',
                           'orbital_period', 'population', 'rotation_period',
                           'terrain', 'url']

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required planet fields"}), 400

        new_planet = Planet(
            uid=data['uid'],
            name=data['name'],
            climate=data['climate'],
            diameter=data['diameter'],
            gravity=data['gravity'],
            orbital_period=data['orbital_period'],
            population=data['population'],
            rotation_period=data['rotation_period'],
            terrain=data['terrain'],
            url=data['url']
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify(new_planet.serialize()), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404

        data = request.get_json()
        for key in data:
            if hasattr(planet, key):
                setattr(planet, key, data[key])

        db.session.commit()
        return jsonify(planet.serialize()), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404

        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planet deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/people', methods=['POST'])
def create_person():
    try:
        data = request.get_json()

        required_fields = ['uid', 'name', 'gender', 'skin_color', 'hair_color',
                           'height', 'eye_color', 'mass', 'homeworld',
                           'birth_year', 'url']

        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required person fields"}), 400

        new_person = People(
            uid=data['uid'],
            name=data['name'],
            gender=data['gender'],
            skin_color=data['skin_color'],
            hair_color=data['hair_color'],
            height=data['height'],
            eye_color=data['eye_color'],
            mass=data['mass'],
            homeworld=data['homeworld'],
            birth_year=data['birth_year'],
            url=data['url']
        )

        db.session.add(new_person)
        db.session.commit()

        return jsonify(new_person.serialize()), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    try:
        person = People.query.get(people_id)
        if not person:
            return jsonify({"error": "Person not found"}), 404

        data = request.get_json()
        for key in data:
            if hasattr(person, key):
                setattr(person, key, data[key])

        db.session.commit()
        return jsonify(person.serialize()), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    try:
        person = People.query.get(people_id)
        if not person:
            return jsonify({"error": "Person not found"}), 404

        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Character deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

    
#favorites endpoints
@app.route('/favorite', methods=['GET']) 
def get_all_favorites(): 
    try:
        favorites = Favorite.query.all()
        favorites_list = [favorite.serialize() for favorite in favorites] 
        
        return jsonify(favorites_list), 200
    
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    try:
        #need to simulate an user as currently there is no users created or logging 
        user_id = 1 

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404

        existing = Favorite.query.filter_by(user_id=user_id, favorite_id=planet_id, favorite_type='planet').first()
        if existing:
            return jsonify({"message": "Planet already in favorites"}), 400

        favorite = Favorite(
            user_id=user_id,
            favorite_id=planet_id,
            favorite_type='planet'
        )
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"message": "Planet added to favorites"}), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    try:
        user_id = 1

        person = People.query.get(people_id)
        if not person:
            return jsonify({"error": "Character not found"}), 404

        existing = Favorite.query.filter_by(user_id=user_id, favorite_id=people_id, favorite_type='character').first()
        if existing:
            return jsonify({"message": "Character already in favorites"}), 400

        favorite = Favorite(
            user_id=user_id,
            favorite_id=people_id,
            favorite_type='character'
        )
        db.session.add(favorite)
        db.session.commit()

        return jsonify({"message": "Character added to favorites"}), 201

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    try:
        user_id = 1  

        favorite = Favorite.query.filter_by(
            user_id=user_id,
            favorite_id=planet_id,
            favorite_type='planet'
        ).first()

        if not favorite:
            return jsonify({"error": "Favorite planet not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite planet deleted"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    try:
        user_id = 1

        favorite = Favorite.query.filter_by(
            user_id=user_id,
            favorite_id=people_id,
            favorite_type='character'
        ).first()

        if not favorite:
            return jsonify({"error": "Favorite character not found"}), 404

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({"message": "Favorite character deleted"}), 200

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
