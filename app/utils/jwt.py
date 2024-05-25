from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
import os
import jwt
from dotenv import load_dotenv
import os
from flask import current_app

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_JWT_KEY", "secret")


def check_authorization(role):
    def check_role(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_app.config["TESTING"] == True:
                return f(*args, **kwargs)
            if role == None:
                return f(*args, **kwargs)
            if not request.headers.get("Authorization"):
                return jsonify({"message": "Token is missing!"}), 401

            try:
                token = request.headers.get("Authorization").split(" ")[1]
            except Exception as e:
                return jsonify({"message": "Token is invalid!"}), 401
            if not token:
                return jsonify({"message": "Token is missing!"}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except Exception:
                return jsonify({"message": "Token is invalid!"}), 401

            if not data:
                return jsonify({"message": "Token is invalid!"}), 401
            if "role" not in data:
                return jsonify({"message": "Token is invalid!"}), 401

            if type(role) == list and data["role"] not in role:
                return (
                    jsonify({"message": "You do not have access to this resource!"}),
                    401,
                )

            if type(role) == str and data["role"] != role:
                return (
                    jsonify({"message": "You do not have access to this resource!"}),
                    401,
                )

            return f(*args, **kwargs)

        return decorated

    return check_role


def create_token(user_id, user_role):
    payload = {"userId": user_id, "role": user_role}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def get_user_id_from_token(token):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if "userId" not in data:
        return None
    else:
        return data["userId"]


def get_user_role_from_token(token):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if "role" not in data:
        return None
    else:
        return data["role"]
