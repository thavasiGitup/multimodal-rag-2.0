import streamlit as st
import requests

st.title("Multimodal RAG 2.0")

uploaded_file = st.file_uploader("Upload File")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    requests.post("http://localhost:8000/upload",
                  files={"file": uploaded_file})
    st.success("File uploaded!")

query = st.text_input("Ask a question")

if st.button("Ask"):
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": query}
    )

    if response.status_code == 200:
        try:
            st.write(response.json().get("answer"))
        except:
            st.error("Invalid JSON response")
            st.write(response.text)
    else:
        st.error("Backend error")
        st.write(response.text)
