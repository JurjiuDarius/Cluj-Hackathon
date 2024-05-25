from flask import Blueprint, jsonify, make_response, request

from app.service import pet_service
from app.utils.jwt import check_authorization

pet_bp = Blueprint("pet", __name__, url_prefix="/pet")


@document_bp.route("/<int:owner_id>", methods=["GET"])
@check_authorization(role=["doctor", "owner"])
def get_pets_for_owner(pet_id):
    authorization = request.headers.get("Authorization")
    jwt_token = authorization.split(" ")[1]
    response, status_code = pet_service.get_pets_for_owner(pet_id, jwt_token)
    return make_response(jsonify(response), status_code)


@document_bp.route(">", methods=["POST"])
@check_authorization(role=["doctor", "owner"])
def add_pet_for_owner():
    authorization = request.headers.get("Authorization")
    jwt_token = authorization.split(" ")[1]
    data = request.json
    response, status_code = pet_service.add_pet_for_owner(data, jwt_token)
    return make_response(jsonify(response), status_code)
