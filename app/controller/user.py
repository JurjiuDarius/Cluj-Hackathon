from flask import Blueprint, jsonify, make_response, request

from app.service import user_service
from app.utils.jwt import check_authorization

user_bp = Blueprint("user", __name__, url_prefix="/users")


@user_bp.route("/doctor-owners/<int:doctor_id>", methods=["GET"])
@check_authorization(role="doctor")
def get_owners(doctor_id):
    owners, status_code = user_service.get_owners_for_doctor(doctor_id)
    return make_response(jsonify(owners), status_code)


@user_bp.route("/add-owner/<int:doctor_id>", methods=["POST"])
@check_authorization(role="doctor")
def add_owner(doctor_id):
    owner_email = request.json.get("email")
    name, status_code = user_service.add_owner_for_doctor(doctor_id, owner_email)
    return make_response(jsonify(name), status_code)


@user_bp.route("/modify", methods=["PUT"])
@check_authorization(role=["owner", "doctor"])
def modify_user():
    data = request.json
    authorization = request.headers.get("Authorization")
    name, status_code = user_service.modify_user(data, authorization)
    return make_response(jsonify(name), status_code)


@user_bp.route("/<int:user_id>", methods=["GET"])
@check_authorization(role={"owner", "doctor"})
def get_user_by_id(user_id):
    authorization = request.headers.get("Authorization")
    name, status_code = user_service.get_user_by_id(user_id, authorization)
    return make_response(jsonify(name), status_code)
