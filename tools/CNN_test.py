import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# --------------------------------------------------
# Load model ONCE at import time
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model_CNN.h5")

CLASS_NAMES = ['banana', 'pizza', 'sushi', 'tomato']

model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={
        "preprocess_input": tf.keras.applications.mobilenet_v2.preprocess_input
    }
)

def predict_image(img_path: str):
    """
    Run CNN inference on an image path
    """
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    preds = model.predict(img_array, verbose=0)[0]

    idx = int(np.argmax(preds))
    return {
        "label": CLASS_NAMES[idx],
        "confidence": float(preds[idx] * 100)
    }