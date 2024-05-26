from flask import Blueprint, jsonify, make_response, request

from app.service import chat_service
from app.utils.jwt import check_authorization

chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/chat",
)


@chat_bp.route("", methods=["POST"])
@check_authorization(role="owner")
def create_diagnostic():
    data = request.json
    response, status = chat_service.get_completion_for_text(data)
    return make_response(jsonify(response), status)
