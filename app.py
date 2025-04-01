import streamlit as st
import subprocess
import fitz  # PyMuPDF
from smart_crawler import crawl_topic
from rags_utils import search_similar_chunks
from gemini_api import query_gemini

# --- Page Setup ---
st.set_page_config(page_title="AI Health Navigator", layout="wide")
st.title("🩺 AI Health Chat Assistant")
st.markdown("Upload medical reports and ask questions. Not a substitute for professional medical advice.")

# --- Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- File Upload (PDF only) ---
uploaded_file = st.file_uploader("📎 Upload a medical report (PDF only)", type=["pdf"])
file_context = ""

if uploaded_file:
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    file_context = text.strip()

    st.success("✅ Extracted text from PDF.")
    st.text_area("📄 Report Content (used for context):", value=file_context, height=150)

# --- Web Crawler for Topic-based Context ---
with st.expander("🌐 Update Medical Knowledge Base"):
    topic = st.text_input("Enter a health topic to crawl (e.g., 'diabetes', 'asthma')")
    if st.button("Fetch Articles"):
        with st.spinner("Crawling trusted medical sources..."):
            crawl_topic(topic)
            subprocess.run(["python", "build_index.py", "data_topic"])
            st.success("✅ Knowledge base updated!")

st.divider()

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
user_prompt = st.chat_input("Ask a medical question...")

if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.spinner("🤖 AI is thinking..."):
        retrieved_chunks = search_similar_chunks(user_prompt)
        context = (file_context + "\n\n" if file_context else "") + "\n\n".join(retrieved_chunks)
        ai_response = query_gemini(user_prompt, context)

    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    with st.expander("📄 Context from report and articles"):
        if file_context:
            st.markdown("**Uploaded Report Context:**")
            st.markdown(file_context)
            st.markdown("---")
        for i, chunk in enumerate(retrieved_chunks, 1):
            st.markdown(f"**Article Chunk {i}:**\n{chunk}")

st.caption("⚕️ Powered by Gemini Pro + RAG + Streamlit")
