from flask import Blueprint, jsonify, make_response, request

from app.service import appointment_service
from app.utils.jwt import check_authorization
from database import db

from ..models import Appointment

appointment_bp = Blueprint("appointment", __name__, url_prefix="/appointments")


@appointment_bp.route("/owner/<int:user_id>", methods=["GET"])
@check_authorization(role="owner")
def get_appointments_owner(user_id):
    response, status_code = appointment_service.get_all_appointments_for_owner(user_id)
    return make_response(jsonify(response), status_code)


@appointment_bp.route("/doctor/<int:user_id>", methods=["GET"])
@check_authorization(role="doctor")
def get_appointments_doctor(user_id):
    response, status_code = appointment_service.get_all_appointments_for_doctor(user_id)
    return make_response(jsonify(response), status_code)


@appointment_bp.route("/<int:id>", methods=["GET"])
@check_authorization(role=["owner", "doctor"])
def get_appointment(id):
    response, status_code = appointment_service.get_appointment_by_id(id)
    return make_response(jsonify(response), status_code)


@appointment_bp.route("", methods=["POST"])
@check_authorization(role="doctor")
def create_appointment():
    data = request.json
    response, status_code = appointment_service.create_appointment(data)
    return make_response(jsonify(response), status_code)


@appointment_bp.route("/<int:id>", methods=["PUT"])
@check_authorization(role="doctor")
def update_appointment(id):
    data = request.json
    response, status_code = appointment_service.update_appointment(id, data)
    return make_response(jsonify(response), status_code)


@appointment_bp.route("/<int:id>", methods=["DELETE"])
@check_authorization(role="doctor")
def delete_appointment(id):
    delete_appointment(id)
    return make_response(jsonify("Delete successful"), 202)
