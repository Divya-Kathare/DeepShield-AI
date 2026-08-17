import streamlit as st

st.title("Metric Test")

st.metric("Confidence", "99.25%")

col1, col2 = st.columns(2)

with col1:
    st.metric("Width", "224")

with col2:
    st.metric("Height", "224")

st.success("Everything loaded")