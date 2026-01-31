from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from models import User
from routes.user_routes import user_bp
from extensions import db, bcrypt, login_manager
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.message_routes import message_bp


def create_app():
    app = Flask(__name__)
    
    CORS(
    app,
    supports_credentials=True,          # << permet l'envoi de cookies
    origins=["http://localhost:5173"]  
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "thisisasecretkey"

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(message_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # @app.route("/api/chat/message", methods=["POST"])
    # def chat_message():
    #     data = request.get_json()

    #     user_message = data.get("message")
    #     chat_id = data.get("chatId")

    #     if not user_message or not chat_id:
    #         return jsonify({"error": "Missing data"}), 400

    #     # 1️⃣ Save user message
    #     message = Message(
    #         role="user",
    #         content=user_message,
    #         chat_id=chat_id
    #     )
    #     db.session.add(message)

    #     # 2️⃣ Mock AI response
    #     ai_reply = f"The backend received your message: '{user_message}'"

    #     ai_message = Message(
    #         role="assistant",
    #         content=ai_reply,
    #         chat_id=chat_id
    #     )
    #     db.session.add(ai_message)

    #     db.session.commit()

    #     return jsonify({"reply": ai_reply})

    @app.route("/")
    def home():
        return "Hello from the other side !!!!"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
