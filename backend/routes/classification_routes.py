from flask import Blueprint, request, jsonify
import os
import uuid

from tools.CNN_test import predict_image

classification_bp = Blueprint(
    "classification",
    __name__,
    url_prefix="/api/classification"
)

UPLOAD_FOLDER = "tmp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@classification_bp.route("/", methods=["POST"])
def classify_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files["image"]

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(filepath)

    result = predict_image(filepath)

    os.remove(filepath)

    return jsonify(result), 200