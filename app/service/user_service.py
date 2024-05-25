from app.models import Doctor, Owner
from app.utils.jwt import get_user_id_from_token, get_user_role_from_token
from database import db


def get_owners_for_doctor(doctor_id):
    owners = Owner.query.filter(Owner.doctors.any(id=doctor_id)).all()
    return [owner.serialize() for owner in owners], 200


def add_owner_for_doctor(doctor_id, owner_email):
    doctor = Doctor.query.get(doctor_id)
    owner = Owner.query.filter_by(email=owner_email).first()
    if not owner:
        return {"message": "Owner not found!"}, 404
    doctor.owners.append(owner)
    db.session.commit()
    return owner.email, 201


def modify_user(data, authorization):
    if "id" not in data:
        return {"message": "User not found"}, 404

    token = authorization.split(" ")[1]

    user_id = data["id"]
    token_id = get_user_id_from_token(token)
    role = get_user_role_from_token(token)
    if user_id != token_id:
        return {"message": "Unauthorized"}, 401

    if role == "owner":
        user = Owner.query.get(user_id)
    elif role == "doctor":
        user = Doctor.query.get(user_id)
        user.education = data["education"]
    if not user:
        return {"message": "User not found"}, 404
    try:
        user.first_name = data["firstName"]
        user.last_name = data["lastName"]
        user.email = data["email"]
        user.phone_number = data["phone"]
        user.city = data["city"]
        user.birth_date = data["birthDate"]
    except Exception:
        return {"message": "Invalid data"}, 400
    db.session.commit()
    return user.serialize(), 201


def get_user_by_id(user_id, authorization):
    token = authorization.split(" ")[1]
    token_id = get_user_id_from_token(token)
    if user_id != token_id:
        return {"message": "Unauthorized"}, 401
    role = get_user_role_from_token(token)

    if role == "owner":
        user = Owner.query.get(user_id)
    elif role == "doctor":
        user = Doctor.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404
    return user.serialize(), 200
