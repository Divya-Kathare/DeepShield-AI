import time
import numpy as np
from PIL import Image
import tensorflow as tf
import streamlit as st


# ==========================================================
# LOAD MODEL (Loads only once)
# ==========================================================

@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("DeepShield_CNN.keras")
    return model


# ==========================================================
# PREPROCESS IMAGE
# ==========================================================

def preprocess_image(uploaded_file):
    """
    Convert uploaded image into model input.
    """

    image = Image.open(uploaded_file).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image)

    image_array = image_array.astype("float32") / 255.0

    image_array = np.expand_dims(image_array, axis=0)

    return image_array


# ==========================================================
# PREDICT IMAGE
# ==========================================================

def predict_image(uploaded_file, model=None):

    if model is None:
        model = load_model()

    image = preprocess_image(uploaded_file)

    start = time.time()

    prediction = model.predict(image, verbose=0)

    end = time.time()

    score = float(prediction[0][0])

    inference_time = round(end - start, 3)

    if score >= 0.5:
        label = "REAL"
        confidence = score * 100
    else:
        label = "FAKE"
        confidence = (1 - score) * 100

    result = {
        "label": label,
        "confidence": round(confidence, 2),
        "probability": round(score, 4),
        "time": inference_time
    }

    return result