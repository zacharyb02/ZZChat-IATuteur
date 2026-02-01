from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User
from forms.user_forms import RegisterForm

user_bp = Blueprint("users", __name__, url_prefix="/api/users")

# Register user endpoints
@user_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    form = RegisterForm(data=data, meta={"csrf": False})

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    # Check uniqueness
    if User.query.filter_by(email=form.email.data).first():
        return jsonify({"error": "Email already exists"}), 409

    if User.query.filter_by(username=form.username.data).first():
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(
        form.password_hash.data
    ).decode("utf-8")

    user = User(
        username=form.username.data,
        email=form.email.data,
        password_hash=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": user.to_dict()
    }), 201

# Get all users endpoints
@user_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# Get one user
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Update user data
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if "username" in data:
        user.username = data["username"]

    if "email" in data:
        user.email = data["email"]

    if "password" in data:
        user.password_hash = bcrypt.generate_password_hash(
            data["password"]
        ).decode("utf-8")

    db.session.commit()
    return jsonify({"message": "User updated", "user": user.to_dict()})

# Delete user 
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


