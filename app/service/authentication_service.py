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
    if not user or not user.is_active:
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
    first_name = user.get("firstName")
    last_name = user.get("lastName")
    email = user.get("email")
    phone_number = user.get("phone")
    city = user.get("city")
    birth_date = user.get("birthDate")
    education = user.get("education")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if birth_date > "2003-01-01":
        return {"message": "You must be at least 18 years old to register!"}, 400
    if birth_date < "1900-01-01":
        return {"message": "Invalid birth date!"}, 400
    if ("@" not in email) or ("." not in email):
        return {"message": "Invalid email!"}, 400
    if role == "owner":
        query_class = Owner
    elif role == "doctor":
        query_class = Doctor
    user = query_class.query.filter_by(email=email).first()
    if user:
        return {"message": "User already exists!"}, 409
    if role == "owner":
        new_user = Owner(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            city=city,
            birth_date=birth_date,
            is_active=True,
        )
    elif role == "doctor":
        new_user = Doctor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            phone_number=phone_number,
            city=city,
            education=education,
            birth_date=birth_date,
            is_active=False,
        )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User created successfully!"}, 201
