from flask import Blueprint, jsonify

from .event import EventResource

api = Blueprint(name='v2', import_name=__name__)
api = EventResource.register(api)


@api.route("/swagger.json")
def create_swagger_spec():
    """Return swagger.json"""
    return jsonify({"message": "no spec."})


@api.errorhandler(400)
def handle_errors(err):
    """Base 4xx errors handler."""
    messages = err.data.get("messages")
    messages = messages.get("form") or "Invalid request."
    if isinstance(messages, dict):
        messages = {key: value[0] if isinstance(
            value, list) else value for key, value in messages.items()}
    return jsonify({"message": messages}), 400
