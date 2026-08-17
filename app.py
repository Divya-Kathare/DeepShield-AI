import streamlit as st
from PIL import Image

from utils.components import (
    show_header,
    show_hero,
    show_feature_bar,
    image_panel,
    analysis_panel,
    prediction_panel,
    reasoning_panel,
    gradcam_panel,
    report_panel,
    show_footer,
)

from utils.predictor import (
    predict_image,
    load_model,
)

from utils.gradcam import generate_gradcam
from utils.reasoning import generate_reasoning
from utils.report import generate_report

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="DeepShield AI",
    page_icon="🛡️",
    layout="wide",
)

# ==========================================================
# HEADER
# ==========================================================

show_header()

show_hero()

st.write("")

show_feature_bar()

st.write("")
st.write("")

# ==========================================================
# FILE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload Face Image",
    type=["jpg", "jpeg", "png"],
)

# ==========================================================
# MAIN CONTENT
# ==========================================================

if uploaded_file is not None:

    left, right = st.columns([1.2, 1])

    with left:
        image_panel(uploaded_file)

    with right:
        analyze = analysis_panel(uploaded_file)

    # ======================================================
    # ANALYZE
    # ======================================================

    if analyze:

        with st.spinner("Analyzing Image..."):

            # -------------------------
            # Prediction
            # -------------------------

            result = predict_image(uploaded_file)

            reasoning = generate_reasoning(result)

            # -------------------------
            # Save Original Image
            # -------------------------

            uploaded_file.seek(0)

            original = Image.open(uploaded_file).convert("RGB")

            original.save("temp_original.jpg")

            # -------------------------
            # Generate GradCAM
            # -------------------------

            uploaded_file.seek(0)

            model = load_model()

            heatmap, overlay = generate_gradcam(
                uploaded_file,
                model,
                "conv2d_2",
            )

            heatmap.save("temp_heatmap.jpg")

            overlay.save("temp_overlay.jpg")

        st.write("")

        # ==================================================
        # RESULT PANELS
        # ==================================================

        prediction_panel(result)

        reasoning_panel(reasoning)

        gradcam_panel(uploaded_file)

        # ==================================================
        # PDF REPORT
        # ==================================================

        pdf_buffer = generate_report(
            result=result,
            reasoning=reasoning,
            image_path="temp_original.jpg",
            heatmap_path="temp_heatmap.jpg",
            overlay_path="temp_overlay.jpg",
        )

        report_panel(pdf_buffer)

# ==========================================================
# FOOTER
# ==========================================================

show_footer()