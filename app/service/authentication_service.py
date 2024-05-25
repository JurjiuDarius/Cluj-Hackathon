import hashlib

from app.models.user import Doctor, Owner
from app.utils.jwt import create_token
from database import db


def login(data):
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    if role == "owner":
        query_class = Owner
    elif role == "doctor":
        query_class = Doctor

    user = query_class.query.filter_by(email=email).first()
    if not user:
        return {"message": "User not found!"}, 404
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if not hashed_password == user.password:
        return {"message": "Incorrect password!"}, 401
    token = create_token(user.id, role)
    return {"token": token, "user": user.serialize()}, 200


def sign_up(data):
    user = data.get("user")
    role = data.get("role")
    password = user.get("password")
    email = user.get("email")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if ("@" not in email) or ("." not in email):
        return {"message": "Invalid email!"}, 400
    if role == "owner":
        query_class = Owner
    elif role == "doctor":
        query_class = Doctor
    else:
        return {"message": "Invalid role!"}, 400

    user = query_class.query.filter_by(email=email).first()
    if user:
        return {"message": "User already exists!"}, 409
    if role == "owner":
        new_user = Owner(
            email=email,
            password=hashed_password,
        )
    elif role == "doctor":
        new_user = Doctor(
            email=email,
            password=hashed_password,
        )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully!"}, 201
