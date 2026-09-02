from flask import jsonify, request
from sqlalchemy import select
from models import db, User, People, Planet, FavoritePlanet, FavoritePeople

CURRENT_USER_ID = 1

def setup_routes(app):
    """
    Función contenedora para registrar los endpoints en la app de Flask.
    Asegúrate de que esta función sea llamada desde tu inicializador.
    """


    @app.route('/people', methods=['GET'])
    def get_all_people():
        people = db.session.scalars(select(People)).all()
        return jsonify([p.serialize() for p in people]), 200

    @app.route('/people/<int:people_id>', methods=['GET'])
    def get_single_person(people_id):
        person = db.session.get(People, people_id)
        if not person:
            return jsonify({"msg": "Personaje no encontrado"}), 404
        return jsonify(person.serialize()), 200

    @app.route('/planets', methods=['GET'])
    def get_all_planets():
        planets = db.session.scalars(select(Planet)).all()
        return jsonify([p.serialize() for p in planets]), 200

    @app.route('/planets/<int:planet_id>', methods=['GET'])
    def get_single_planet(planet_id):
        planet = db.session.get(Planet, planet_id)
        if not planet:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        return jsonify(planet.serialize()), 200



    @app.route('/users', methods=['GET'])
    def get_all_users():
        users = db.session.scalars(select(User)).all()
        return jsonify([u.serialize() for u in users]), 200

    @app.route('/users/favorites', methods=['GET'])
    def get_user_favorites():
        fav_planets = db.session.scalars(select(FavoritePlanet).filter_by(user_id=CURRENT_USER_ID)).all()
        fav_people = db.session.scalars(select(FavoritePeople).filter_by(user_id=CURRENT_USER_ID)).all()
        
        return jsonify({
            "planets": [p.serialize() for p in fav_planets],
            "people": [p.serialize() for p in fav_people]
        }), 200

    @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
    def add_favorite_planet(planet_id):
        # Validar existencia en la BD local
        planet = db.session.get(Planet, planet_id)
        if not planet:
            return jsonify({"msg": "El planeta no existe"}), 404
            
        exists = db.session.scalar(select(FavoritePlanet).filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id))
        if exists:
            return jsonify({"msg": "El planeta ya está en tus favoritos"}), 400

        new_favorite = FavoritePlanet(user_id=CURRENT_USER_ID, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg": "Planeta añadido a favoritos"}), 201

    @app.route('/favorite/people/<int:people_id>', methods=['POST'])
    def add_favorite_people(people_id):
        person = db.session.get(People, people_id)
        if not person:
            return jsonify({"msg": "El personaje no existe"}), 404
            
        exists = db.session.scalar(select(FavoritePeople).filter_by(user_id=CURRENT_USER_ID, people_id=people_id))
        if exists:
            return jsonify({"msg": "El personaje ya está en tus favoritos"}), 400

        new_favorite = FavoritePeople(user_id=CURRENT_USER_ID, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg": "Personaje añadido a favoritos"}), 201

    @app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
    def delete_favorite_planet(planet_id):
        favorite = db.session.scalar(select(FavoritePlanet).filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id))
        if not favorite:
            return jsonify({"msg": "Favorito no encontrado"}), 404
            
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

    @app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
    def delete_favorite_people(people_id):
        favorite = db.session.scalar(select(FavoritePeople).filter_by(user_id=CURRENT_USER_ID, people_id=people_id))
        if not favorite:
            return jsonify({"msg": "Favorito no encontrado"}), 404
            
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Personaje eliminado de favoritos"}), 200
