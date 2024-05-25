from flask import Blueprint, jsonify, make_response, request

from app.service import diagnostic_service
from app.utils.jwt import check_authorization

diagnostic_bp = Blueprint(
    "diagnostic",
    __name__,
    url_prefix="/diagnostic",
)


@diagnostic_bp.route("", methods=["POST"])
@check_authorization(role="doctor")
def create_diagnostic():
    data = request.json
    response, status = diagnostic_service.create_diagnostic(data)
    return make_response(jsonify(response), status)


@diagnostic_bp.route("/<image_id>", methods=["GET"])
@check_authorization(role=["owner", "doctor"])
def get_diagnostic_for_image(image_id):
    response, status = diagnostic_service.get_diagnostic_for_image(image_id)
    return make_response(jsonify(response), status)


@diagnostic_bp.route("/<diagnostic_id>", methods=["GET"])
@check_authorization(role=["owner", "doctor"])
def get_diagnostic_by_id(diagnostic_id):
    response, status = diagnostic_service.get_diagnostic(diagnostic_id)
    return make_response(jsonify(response), status)


@diagnostic_bp.route("", methods=["PUT"])
@check_authorization(role="doctor")
def update_diagnostic():
    data = request.json
    response, status = diagnostic_service.update_diagnostic(data)
    return make_response(jsonify(response), status)


@diagnostic_bp.route("/<diagnostic_id>", methods=["DELETE"])
@check_authorization(role="doctor")
def delete_diagnostic(diagnostic_id):
    response, status = diagnostic_service.delete_diagnostic(diagnostic_id)
    return make_response(jsonify(response), status)
