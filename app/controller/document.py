from flask import Blueprint, jsonify, make_response, request

from app.service import document_service
from app.utils.jwt import check_authorization

document_bp = Blueprint("document", __name__, url_prefix="/document")


@document_bp.route("/<int:pet_id>", methods=["GET"])
@check_authorization(role=["doctor", "owner"])
def get_documents(pet_id):
    authorization = request.headers.get("Authorization")
    jwt_token = authorization.split(" ")[1]
    message, status_code = document_service.get_documents_for_pet(pet_id, jwt_token)
    return make_response(jsonify(message), status_code)


@document_bp.route("/", methods=["POST"])
@check_authorization(role="owner")
def add_document():
    json = request.json.get("email")
    authorization = request.headers.get("Authorization")
    jwt_token = authorization.split(" ")[1]
    message, status_code = document_service.add_document_for_pet(json, jwt_token)
    return make_response(jsonify(message), status_code)


@document_bp.route("/<int:pet_id>/<int:document_id>", methods=["DELETE"])
@check_authorization(role=["doctor", "owner"])
def delete_document(pet_id, document_id):
    authorization = request.headers.get("Authorization")
    jwt_token = authorization.split(" ")[1]
    message, status_code = document_service.delete_document(
        pet_id, document_id, jwt_token
    )
    return make_response(jsonify(message), status_code)
