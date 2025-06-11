import streamlit as st
from PIL import Image
import requests
import os
from io import BytesIO
import base64

def display_base64_image(base64_str, caption):
    try:
        img_bytes = base64.b64decode(base64_str)
        img = Image.open(BytesIO(img_bytes))
        st.image(img, caption=caption, use_column_width=True)
    except Exception as e:
        st.warning(f"⚠️ Failed to display image: {e}")
    
# 🔁 Replace this with your real query to local webhook
def query_rag_system(query):
    try:
        response = requests.post(
            # "http://localhost:5678/webhook-test/query",
           "http://localhost:5678/webhook/query",
            json={"query": query},
            timeout=3000
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": "❌ Error: Failed to fetch response.",
                "sources": []
            }
    except Exception as e:
        return {
            "answer": f"❌ Exception: {str(e)}",
            "sources": []
        }

# Streamlit page setup
st.set_page_config(page_title="🧠 RAG Chatbot", layout="centered")
st.title("📚 Chat with RAG System")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander("📖 Source Context"):
                for i, src in enumerate(msg["sources"]):
                    st.markdown(f"**Source {i+1}**")
                    st.markdown(f"- **Type:** `{src.get('type', 'Unknown')}`")
                    st.markdown(f"- **Page:** `{src.get('page_number', 'N/A')}`")
                    st.markdown(f"- **File:** `{src.get('source', 'N/A')}`")
                    st.markdown(f"- **Content:** `{src.get('content', 'N/A')}`")

                    if src.get("type") == "Image":
                        if "image_base64" in src:
                            display_base64_image(src["image_base64"], caption=f"Image from page {src.get('page_number')}")
                        elif "imgbb_url" in src:
                            st.image(src["imgbb_url"], caption=f"Image from page {src.get('page_number')}", use_column_width=True)

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user input
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Spinner while waiting for response
    with st.spinner("🤖 Thinking..."):
        rag_result_list = query_rag_system(prompt)
    # st.write(rag_result_list)    
    rag_result = rag_result_list[0] if isinstance(rag_result_list, list) and rag_result_list else {"answer": "⚠️ No answer returned.", "sources": []}   
    
    answer=rag_result.get("answer")
    # answer = rag_result.get("answer", "⚠️ No answer returned.")
    sources = rag_result.get("sources", [])
    
    with st.chat_message("assistant"):
        st.markdown(answer)
        if sources:
            with st.expander("📖 Source Context"):
                for i, src in enumerate(sources):
                    st.markdown(f"**Source {i+1}**")
                    st.markdown(f"- **Type:** `{src.get('type', 'Unknown')}`")
                    st.markdown(f"- **Page:** `{src.get('page_number', 'N/A')}`")
                    st.markdown(f"- **File:** `{src.get('source', 'N/A')}`")
                    st.markdown(f"- **Content:** `{src.get('content', 'N/A')}`")

                    if src.get("type") == "Image":
                        if "image_base64" in src:
                            display_base64_image(src["image_base64"], caption=f"Image from page {src.get('page_number')}")
                        elif "imgbb_url" in src:
                            st.image(src["imgbb_url"], caption=f"Image from page {src.get('page_number')}", use_column_width=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })