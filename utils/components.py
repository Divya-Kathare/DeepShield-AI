import streamlit as st
from PIL import Image

from utils.gradcam import generate_gradcam
from utils.predictor import load_model


# ==========================================================
# HEADER
# ==========================================================

def show_header():
    col1, col2 = st.columns([4, 1], vertical_alignment="bottom")

    with col1:
        # Control logo size directly using width (adjust pixels if needed, e.g., 200 to 250)
        st.image("assets/logo_horizontal.png", width=370)
        
        st.markdown(
            """
            <div style="
                color: #94A3B8; 
                font-size: 16px; 
                margin-bottom: 2px; 
                font-weight: 500;
                letter-spacing: 0.3px;">
                Explainable Deepfake Detection Platform
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style="
                text-align: right; 
                color: #64748B; 
                font-weight: 600;
                margin-bottom: 2px; 
                font-size: 15px;">
                Version 1.0
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()


# ==========================================================
# HERO
# ==========================================================

def show_hero():

    st.markdown(
        """
<div class="hero-box">

<h1>
Detect AI Generated Faces with Explainable AI
</h1>

<p>
Upload a facial image and receive an AI prediction,
confidence score, visual explanation and downloadable report.
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# FEATURE BAR
# ==========================================================

def show_feature_bar():

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info("🧠 AI Detection")

    with c2:
        st.info("📊 Confidence")

    with c3:
        st.info("🔥 Explainability")

    with c4:
        st.info("📄 PDF Report")


# ==========================================================
# IMAGE PANEL
# ==========================================================

def image_panel(uploaded_file):

    st.markdown("## 🖼 Uploaded Image")

    st.image(
        uploaded_file,
        use_container_width=True
    )


# ==========================================================
# ANALYSIS PANEL
# ==========================================================

def analysis_panel(uploaded_file):

    image = Image.open(uploaded_file)

    width, height = image.size

    size = round(uploaded_file.size / 1024, 2)

    st.markdown("## 🤖 AI Analysis")

    st.metric("Status", "Ready")

    c1, c2 = st.columns(2)

    with c1:

        st.metric("Width", f"{width}px")

        st.metric("Height", f"{height}px")

    with c2:

        st.metric("Format", uploaded_file.type.upper())

        st.metric("Size", f"{size} KB")

    st.write("")

    analyze = st.button(
        "🔍 Analyze Image",
        use_container_width=True,
        type="primary"
    )

    return analyze


# ==========================================================
# PREDICTION PANEL
# ==========================================================
def prediction_panel(result):

    label = result["label"]
    confidence = result["confidence"]
    inference = result["time"]

    is_fake = label.upper() == "FAKE"

    # -----------------------------
    # Prediction Banner
    # -----------------------------

    if is_fake:
        st.markdown("""
        <div style="
            background:#4A2327;
            padding:22px;
            border-radius:18px;
            border-left:8px solid #FF1744;
            margin-bottom:25px;">
            <h1 style="color:white;margin:0;">
            🔴 FAKE FACE
            </h1>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            background:#103C2E;
            padding:22px;
            border-radius:18px;
            border-left:8px solid #00E676;
            margin-bottom:25px;">
            <h1 style="color:white;margin:0;">
            🟢 REAL FACE
            </h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 📊 Prediction Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

        if confidence >= 90:
            level = "Very High"
        elif confidence >= 75:
            level = "High"
        elif confidence >= 60:
            level = "Medium"
        else:
            level = "Low"

        st.metric(
            "Confidence Level",
            level
        )

    with c2:

        st.metric(
            "Inference Time",
            f"{inference:.3f} sec"
        )

        st.metric(
            "Prediction",
            label
        )

    st.progress(confidence / 100)

    st.caption(
        f"Prediction: **{label}** | Confidence: **{confidence:.2f}%**"
    )

    st.markdown("---")

# ==========================================================
# AI REASONING PANEL
# ==========================================================

def reasoning_panel(reasoning):

    st.markdown("## 🧠 AI Reasoning")

    for i, reason in enumerate(reasoning, start=1):

        st.success(f"{i}. {reason}")

    st.markdown("---")


# ==========================================================
# GRADCAM PANEL
# ==========================================================


def gradcam_panel(uploaded_file):

    st.markdown("---")
    st.markdown("## 🔥 Explainability (Grad-CAM)")

    if uploaded_file is None:
        st.info("Grad-CAM visualization will appear here.")
        return

    try:

        model = load_model()

        uploaded_file.seek(0)
        heatmap, overlay = generate_gradcam(
            uploaded_file,
            model,
            "conv2d_2"
        )

        uploaded_file.seek(0)

        tab1, tab2, tab3 = st.tabs(
            ["Original", "Heatmap", "Overlay"]
        )

        with tab1:
            c1, c2, c3 = st.columns([1, 3, 1])
            with c2:
                uploaded_file.seek(0)
                st.image(
                    uploaded_file,
                    width=400
                )
                st.caption("Original Uploaded Image")
                
            

        with tab2:
            c1, c2, c3 = st.columns([1, 3, 1])
            with c2:
                st.image(
                    heatmap,
                    width=400
                )
                st.caption("Grad-CAM Heatmap")
              

        with tab3:
            c1, c2, c3 = st.columns([1, 3, 1])
            with c2:
                st.image(
                    overlay,
                    width=400
                )
                st.caption("Grad-CAM Overlay")
             

    except Exception as e:
        st.error(f"GradCAM Error: {e}")

# ==========================================================
# REPORT PANEL
# ==========================================================

def report_panel(pdf_buffer):

    st.markdown("---")
    st.markdown("## 📄 Export Report")

    st.download_button(
        label="⬇ Download DeepShield Report",
        data=pdf_buffer,
        file_name="DeepShield_Report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.success("Report is ready for download.")


# ==========================================================
# FOOTER
# ==========================================================

def show_footer():

    st.divider()

    st.markdown(
        """
<div style="text-align:center;
            color:#94A3B8;
            padding:20px;">

© 2026 DeepShield AI

Built with ❤️ using TensorFlow & Streamlit

</div>
""",
        unsafe_allow_html=True
    )