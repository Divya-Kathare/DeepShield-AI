import streamlit as st
from PIL import Image


def upload_info_card(uploaded_file):
    """
    Display prediction information before model analysis.
    """

    image = Image.open(uploaded_file)

    width, height = image.size

    file_size = round(uploaded_file.size / 1024, 2)

    file_type = uploaded_file.type.upper()

    st.markdown("### 📊 Prediction")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Status", "Ready")

        st.metric("Width", f"{width}px")

        st.metric("Height", f"{height}px")

    with col2:
        st.metric("Format", file_type)

        st.metric("Size", f"{file_size} KB")

        st.metric("Model", "CNN")

    st.write("")

    analyze = st.button(
        "🔍 Analyze Image",
        use_container_width=True,
    )

    return analyze

def prediction_dashboard(result):
    """
    Display the AI prediction dashboard.
    """

    label = result["label"]
    confidence = result["confidence"]
    inference = result["time"]

    # -----------------------------
    # Prediction Badge
    # -----------------------------

    if label.upper() == "FAKE":
        badge = "🔴 FAKE FACE"
        level_color = "red"
    else:
        badge = "🟢 REAL FACE"
        level_color = "green"

    # -----------------------------
    # Confidence Level
    # -----------------------------

    if confidence >= 95:
        level = "⭐⭐⭐ Very High"

    elif confidence >= 85:
        level = "⭐⭐ High"

    elif confidence >= 70:
        level = "⭐ Moderate"

    else:
        level = "Low"

    # -----------------------------
    # Dashboard
    # -----------------------------

    st.markdown("## 🛡️ Prediction Result")

    st.markdown("---")

    st.markdown(
        f"<h2 style='text-align:center;color:{level_color};'>{badge}</h2>",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Confidence", f"{confidence:.2f}%")

        st.metric("Inference", f"{inference:.3f} sec")

    with c2:
        st.metric("Model", "DeepShield CNN")

        st.metric("Level", level)

    st.write("")

    st.progress(confidence / 100)

    st.caption(f"Confidence Score : {confidence:.2f}%")

    st.success("✔ Analysis Complete")
