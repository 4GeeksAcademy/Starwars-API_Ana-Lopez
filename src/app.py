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
from models import db, User, Planets, Character, Favorite
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

@app.route('/user', methods=['GET'])
def handle_hello():

    try:
        # consultar a la base de datos los registros de usuarios
        query_results= User.query.all()

        # validar si la lista esta vacia
        if not query_results:
            return jsonify({"msg": "Usuarios no encontrados"}), 400 

        # aplico map para usar serialize()
        results= list(map(lambda item: item.serialize(), query_results))


        response_body = {
            "msg": "lista de usuarios encontrada",
            "results": results
        }

        return jsonify(response_body), 200
           
    except Exception as error:
         #en caso de error se captura la excepcion
        print(f"Error al obtener los ususarios: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500
    

@app.route('/planets', methods=['GET'])
def get_planets():

    try:

        # Buscar todos los planetas
        planets = Planets.query.all()

        # Convertir a lista de diccionarios
        planets_list = [planet.serialize() for planet in planets]

        # Si no hay planetas
        if len(planets_list) == 0:
            return jsonify({
                "message": "No planets found"
            }), 404

        # Respuesta exitosa
        return jsonify({
            "results": planets_list
        }), 200

    except Exception as e:

        # Manejo de errores inesperados
        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500
    
@app.route('/character', methods=['GET'])
def get_characters():

    try:

        # Buscar todos los personajes
        characters = Character.query.all()

        # Convertir objetos a diccionarios
        characters_list = [character.serialize() for character in characters]

        # Validar si no hay personajes
        if len(characters_list) == 0:
            return jsonify({
                "message": "No characters found"
            }), 404

        # Respuesta exitosa
        return jsonify({
            "results": characters_list
        }), 200

    except Exception as e:

        # Manejo de errores
        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500
    
@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):

    try:

        # Buscar personaje por ID
        character = Character.query.get(character_id)

        # Validar si no existe
        if character is None:
            return jsonify({
                "message": "Character not found"
            }), 404

        # Respuesta exitosa
        return jsonify({
            "result": character.serialize()
        }), 200

    except Exception as e:

        # Manejo de errores
        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500


@app.route('/users/favorites', methods=['GET'])
def get_favorites():

    try:

        # Simular usuario actual
        current_user_id = 1

        # Buscar favoritos del usuario
        favorites = Favorite.query.filter_by(user_id=current_user_id).all()

        # Validar lista vacía
        if len(favorites) == 0:
            return jsonify({
                "message": "No favorites found"
            }), 404

        # Serializar favoritos
        favorites_list = [favorite.serialize() for favorite in favorites]

        # Respuesta exitosa
        return jsonify({
            "results": favorites_list
        }), 200

    except Exception as e:

        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
