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
def get_user():

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

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):

    try:

        # Buscar planeta por ID
        planet = Planets.query.get(planet_id)

        # Validar si existe
        if planet is None:
            return jsonify({
                "message": "Planet not found"
            }), 404

        # Respuesta exitosa
        return jsonify({
            "result": planet.serialize()
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

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def create_planet_fav(user_id, planet_id ):

    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg": "no se encontro el usuario"}), 400

    planet= Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "no se encontro el planeta"}), 400

    #verificamos si ya existe un registro de favoritos con esos datos
    exists= Favorite.query.filter_by(
        id_user=user_id,
        id_planet=planet_id
    ).first()
    if exists:
        return jsonify({"msg": "El planeta ya esta en favoritos "}), 400


    fav= Favorite(id_user= user_id, id_planet=planet_id)

    db.session.add(fav)
    db.session.commit()

    return jsonify({"msg": "El planeta se agrego a favoritos"}), 201

@app.route('/users/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def create_character_fav(user_id, character_id ):

    user= User.query.get(user_id)
    if not user:
        return jsonify({"msg": "no se encontro el usuario"}), 400

    character= character.query.get(character_id)
    if not character:
        return jsonify({"msg": "no se encontro el personaje"}), 400

    #verificamos si ya existe un registro de favoritos con esos datos
    exists= Favorite.query.filter_by(
        id_user=user_id,
        id_charcater=character_id
    ).first()
    if exists:
        return jsonify({"msg": "El personaje ya esta en favoritos "}), 400


    fav= Favorite(id_user= user_id, id_character=character_id)

    db.session.add(fav)
    db.session.commit()

    return jsonify({"msg": "El personaje se agrego a favoritos"}), 201

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):

    try:

        user= User.query.get(user_id)
        if not user:
            return jsonify({"msg": "no se encontro el usuario"}), 400
    
        # buscamos el favorito
        favorite = Favorite.query.filter_by(
            planet_id=planet_id
        ).first()

        # validamos si existe
        if not favorite:
            return jsonify({
                "msg": "El planeta no esta en favoritos"
            }), 404

        # eliminamos favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            "msg": "El planeta fue eliminado de favoritos"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500
    
@app.route('/users/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id, user_id):

    try:

        user= User.query.get(user_id)
        if not user:
            return jsonify({"msg": "no se encontro el usuario"}), 400
    
        # buscamos el favorito
        favorite = Favorite.query.filter_by(
            character_id=character_id
        ).first()

        # validamos si existe
        if not favorite:
            return jsonify({
                "msg": "El personaje no esta en favoritos"
            }), 404

        # eliminamos favorito
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            "msg": "El personaje fue eliminado de favoritos"
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": "Something went wrong",
            "message": str(e)
        }), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
