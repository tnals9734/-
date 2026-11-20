import streamlit as st

st.title("탄소중립 선도도시 기본계획")

tab1, tab2 = st.tabs(["노원구", "당진시"])

with tab1:
    st.image("노원.jpg")
    with open("(노원구)01_탄소중립 선도도시 기본계획(260709)_최종.pdf", "rb") as f:
        st.download_button("노원구 기본계획 PDF 받기", f, file_name="노원구_기본계획.pdf")

with tab2:
    st.image("당진.jpg")
    with open("(당진시)01_탄소중립 선도도시 기본계획(260707)_최종.pdf", "rb") as f:
        st.download_button("당진시 기본계획 PDF 받기", f, file_name="당진시_기본계획.pdf")
