# streamlit_gemini_multiturn_app.py
# A multi-turn Streamlit app using Gemini 2.0 Flash (text only).
# Run locally:
#   pip install --upgrade streamlit google-generativeai
#   streamlit run streamlit_gemini_multiturn_app.py

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import Google Generative AI
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Page configuration
st.set_page_config(page_title="Space Assistant", page_icon="🚀", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.title("Settings")
    
    # API Key input
    api_key = st.text_input("GEMINI_API_KEY", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    
    # Model selection (prioritizing free tier friendly models)
    model_name = st.selectbox("Model", 
                             ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-2.5-pro"])
    
    # System instruction for space focus
    system_instruction = st.text_area(
        "System instruction",
        value="You are a space expert assistant. You only provide information about space, astronomy, planets, stars, galaxies, and space exploration. If asked about anything else, politely redirect to space topics.",
        height=80
    )
    
    # Generation parameters
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05)
    top_k = st.slider("Top-k", 1, 100, 40, 1)
    max_tokens = st.slider("Max output tokens", 32, 2048, 512, 32)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = None

# Cache the model to avoid recreating it
@st.cache_resource(show_spinner=False)
def get_model(api_key, model_name, system_instruction):
    if genai is None:
        raise ImportError("google-generativeai is not installed")
    if not api_key:
        raise ValueError("API key missing")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name, system_instruction=system_instruction)

# Main app
st.title("🚀 Space Assistant")
st.caption("Ask me anything about space, planets, stars, and space exploration!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask about space...")

# Process user input
if user_prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Get model
    try:
        model = get_model(api_key, model_name, system_instruction)
    except Exception as e:
        st.error(str(e))
        st.stop()
    
    # Generation configuration
    gen_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }
    
    # Initialize chat session if needed
    if st.session_state.chat is None:
        history = []
        for msg in st.session_state.messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": msg["content"]})
        st.session_state.chat = model.start_chat(history=history)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Exploring space..."):
            try:
                response = st.session_state.chat.send_message(user_prompt, generation_config=gen_config)
                answer = response.text or "(No response generated)"
            except Exception as e:
                answer = f"Error: {e}"
            st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})