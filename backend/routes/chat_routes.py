from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Chat

chat_bp = Blueprint("chats", __name__, url_prefix="/api/chats")


# Create a new chat endpoint
@chat_bp.route("/", methods=["POST"])
@login_required
def create_chat():
    data = request.get_json(silent=True) or {}

    title = data.get("title", "New Chat")

    chat = Chat(
        title=title,
        user_id=current_user.id
    )

    db.session.add(chat)
    db.session.commit()

    return jsonify({
        "message": "Chat created",
        "chat": {
            "id": chat.id,
            "title": chat.title,
            "created_at": chat.created_at
        }
    }), 201


# Get all chats for current user endpoint
@chat_bp.route("/", methods=["GET"])
@login_required
def get_chats():
    chats = Chat.query.filter_by(user_id=current_user.id).order_by(Chat.updated_at.desc()).all()

    return jsonify([
        {
            "id": chat.id,
            "title": chat.title,
            "created_at": chat.created_at,
            "updated_at": chat.updated_at
        }
        for chat in chats
    ])


# Get one chat with messages endpoint
@chat_bp.route("/<int:chat_id>", methods=["GET"])
@login_required
def get_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)

    if chat.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    return jsonify({
        "id": chat.id,
        "title": chat.title,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "is_image": msg.is_image,
                "created_at": msg.created_at
            }
            for msg in chat.messages
        ]
    })


# Delete a chat endpoint
@chat_bp.route("/<int:chat_id>", methods=["DELETE"])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.get_or_404(chat_id)

    if chat.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(chat)
    db.session.commit()

    return jsonify({"message": "Chat deleted"})
