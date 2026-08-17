import streamlit as st
from utils.components import (
    upload_info_card,
    prediction_dashboard,
)
from utils.predictor import predict_image

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="DeepShield AI",
    page_icon="🛡️",
    layout="wide",
)

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

with open("css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown(
        "<h2 style='margin:0;color:#2563EB;'>🛡️ DeepShield AI</h2>",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        "<p style='text-align:right;color:#64748B;margin-top:12px;'>Version 1.0</p>",
        unsafe_allow_html=True,
    )

st.divider()

# ---------------------------------------------------
# HERO
# ---------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>Detect AI-Generated Faces with Explainable AI</h1>
        <p>
            Upload a facial image and receive a prediction,
            confidence score, AI reasoning, and Grad-CAM
            visualization.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ---------------------------------------------------
# FEATURES
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("🧠 AI Detection")

with c2:
    st.info("🔥 Grad-CAM")

with c3:
    st.info("📊 Confidence")

with c4:
    st.info("📄 PDF Report")

st.write("")
st.write("")

# ---------------------------------------------------
# UPLOAD
# ---------------------------------------------------

st.subheader("Upload Face Image")

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG or PNG image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:

    left, right = st.columns([1.2, 1])

    with left:
        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True,
        )

    with right:
        analyze = upload_info_card(uploaded_file)
        if analyze:
            with st.spinner("Analyzing image..."):
                 result = predict_image(uploaded_file)
            prediction_dashboard(result)
            



# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#94A3B8;">
        DeepShield AI • Built with Streamlit & TensorFlow
    </div>
    """,
    unsafe_allow_html=True,
)