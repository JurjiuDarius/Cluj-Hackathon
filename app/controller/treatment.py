from flask import Blueprint, jsonify, make_response, request

from app.service import treatment_service
from app.utils.jwt import check_authorization

treatment_bp = Blueprint(
    "treatment",
    __name__,
    url_prefix="/treatment",
)


@treatment_bp.route("", methods=["POST"])
@check_authorization(role="doctor")
def create_treatment():
    data = request.json
    response, status = treatment_service.create_treatment(data)
    return make_response(jsonify(response), status)


@treatment_bp.route("/<treatment_id>", methods=["GET"])
@check_authorization(role=["owner", "doctor"])
def get_treatment_by_id(treatment_id):
    response, status = treatment_service.get_treatment(treatment_id)
    return make_response(jsonify(response), status)


@treatment_bp.route("", methods=["PUT"])
@check_authorization(role="doctor")
def update_treatment():
    data = request.json
    response, status = treatment_service.update_treatment(data)
    return make_response(jsonify(response), status)


@treatment_bp.route("/<treatment_id>", methods=["DELETE"])
@check_authorization(role="doctor")
def delete_treatment(treatment_id):
    response, status = treatment_service.delete_treatment(treatment_id)
    return make_response(jsonify(response), status)


@treatment_bp.route("/new-stage", methods=["POST"])
@check_authorization(role="doctor")
def add_stage():
    data = request.json
    response, status = treatment_service.add_treatment_stage(data)
    return make_response(jsonify(response), status)


@treatment_bp.route("/stage/<treatment_id>/<stage_number>", methods=["DELETE"])
@check_authorization(role="doctor")
def delete_stage(treatment_id, stage_number):
    response, status = treatment_service.delete_treatment_stage(
        treatment_id, stage_number
    )
    return make_response(jsonify(response), status)


@treatment_bp.route("/complete-stage/<treatment_id>/<stage_number>", methods=["PUT"])
@check_authorization(role="doctor")
def delete_stage(treatment_id, stage_number):
    response, status = treatment_service.complete_treatment_stage(
        treatment_id, stage_number
    )
    return make_response(jsonify(response), status)
