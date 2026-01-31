from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Chat, Message

message_bp = Blueprint(
    "messages",
    __name__,
    url_prefix="/api/chats/<int:chat_id>/messages"
)


# Send a message to a chat endpoint
@message_bp.route("/", methods=["POST"])
@login_required
def send_message(chat_id):
    chat = Chat.query.get_or_404(chat_id)

    if chat.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Message content required"}), 400

    # Mettre à jour le titre si le chat n'a pas encore de messages
    if len(chat.messages) == 0:
        chat.title = " ".join(content.split()[:5])  # 5 premiers mots du prompt
        db.session.commit()

    # Save user message
    user_message = Message(
        role="user",
        content=content,
        chat_id=chat.id
    )
    db.session.add(user_message)

    # Mock AI response
    ai_reply = f"The backend received your message: '{content}'"
    ai_message = Message(
        role="assistant",
        content=ai_reply,
        chat_id=chat.id
    )
    db.session.add(ai_message)
    db.session.commit()

    return jsonify({
        "reply": ai_reply,
        "messages": [
            {"id": user_message.id, "role": user_message.role, "content": user_message.content},
            {"id": ai_message.id, "role": ai_message.role, "content": ai_message.content}
        ],
        "chat": {
            "id": chat.id,
            "title": chat.title
        }
    }), 201


# Get messages of a chat endpoint
@message_bp.route("/", methods=["GET"])
@login_required
def get_messages(chat_id):
    chat = Chat.query.get_or_404(chat_id)

    if chat.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.created_at).all()

    return jsonify([
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "is_image": msg.is_image,
            "created_at": msg.created_at
        }
        for msg in messages
    ])
