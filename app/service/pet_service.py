from app.models import Pet
from app.utils.jwt import get_user_id_from_token
from database import db


def get_pets_for_owner(owner_id, jwt_token):
    jwt_owner_id = get_user_id_from_token(jwt_token)
    if jwt_owner_id != owner_id:
        return {"error": "You are not authorized to view these pets"}, 403
    pets = Pet.query.filter_by(owner_id=owner_id).all()
    return [pet.serialize() for pet in pets], 200


def add_pet_for_owner(data, jwt_token):
    jwt_owner_id = get_user_id_from_token(jwt_token)
    if jwt_owner_id != data["ownerId"]:
        return {"error": "You are not authorized to add a pet for this owner"}, 403

    new_pet = Pet(
        name=data["name"],
        breed=data["breed"],
        age=data["age"],
        owner_id=data["ownerId"],
        gender=data["gender"],
    )

    db.session.add(new_pet)
    db.session.commit()
    return new_pet.serialize(), 201
