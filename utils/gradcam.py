import cv2
import numpy as np
import tensorflow as tf
from PIL import Image

from utils.predictor import preprocess_image


def generate_gradcam(
    uploaded_file,
    model,
    last_conv_layer_name="conv2d_2",
):
    """
    Generate Grad-CAM heatmap and overlay image.

    Returns:
        heatmap (PIL Image)
        overlay (PIL Image)

    Also saves:
        temp_heatmap.jpg
        temp_overlay.jpg
    """

    # =====================================================
    # Load Original Image
    # =====================================================

    uploaded_file.seek(0)

    original = Image.open(uploaded_file).convert("RGB")
    original = original.resize((224, 224))

    original_np = np.array(original)

    # =====================================================
    # Preprocess Image
    # =====================================================

    uploaded_file.seek(0)

    img_array = preprocess_image(uploaded_file)

    # =====================================================
    # Build Functional Model
    # (Compatible with Sequential Models in Keras 3)
    # =====================================================

    inputs = tf.keras.Input(shape=(224, 224, 3))

    x = inputs
    conv_output = None

    for layer in model.layers:

        x = layer(x)

        if layer.name == last_conv_layer_name:
            conv_output = x

    outputs = x

    grad_model = tf.keras.Model(
        inputs=inputs,
        outputs=[conv_output, outputs],
    )

    # =====================================================
    # Gradient Calculation
    # =====================================================

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        loss = predictions[:, 0]

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2),
    )

    conv_outputs = conv_outputs[0].numpy()
    pooled_grads = pooled_grads.numpy()

    # =====================================================
    # Build Heatmap
    # =====================================================

    heatmap = np.zeros(
        conv_outputs.shape[:2],
        dtype=np.float32,
    )

    for i in range(len(pooled_grads)):
        heatmap += pooled_grads[i] * conv_outputs[:, :, i]

    heatmap = np.maximum(heatmap, 0)

    max_value = np.max(heatmap)

    if max_value != 0:
        heatmap /= max_value

    # =====================================================
    # Resize Heatmap
    # =====================================================

    heatmap = cv2.resize(
        heatmap,
        (224, 224),
        interpolation=cv2.INTER_LANCZOS4,
    )

    heatmap = np.uint8(255 * heatmap)

    # =====================================================
    # Apply Color Map
    # =====================================================

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_INFERNO,
    )

    # =====================================================
    # Create Overlay
    # =====================================================

    overlay = cv2.addWeighted(
        original_np,
        0.60,
        heatmap_color,
        0.40,
        0,
    )

    overlay = cv2.cvtColor(
        overlay,
        cv2.COLOR_BGR2RGB,
    )

    # =====================================================
    # Convert to PIL
    # =====================================================

    heatmap_img = Image.fromarray(
        cv2.cvtColor(
            heatmap_color,
            cv2.COLOR_BGR2RGB,
        )
    )

    overlay_img = Image.fromarray(overlay)

    # =====================================================
    # Save Images for PDF Report
    # =====================================================

    heatmap_img.save("temp_heatmap.jpg")

    overlay_img.save("temp_overlay.jpg")

    # =====================================================
    # Return Images
    # =====================================================

    return (
        heatmap_img,
        overlay_img,
    )