import io
from pathlib import Path
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Widgets Demo", page_icon="🎛️", layout="wide")

# --- sidebar controls ---
st.sidebar.title("Controls")
st.sidebar.write("My name is Bhavishya")

# Session state example: a simple visit counter
if "visits" not in st.session_state:
    st.session_state.visits = 0
st.session_state.visits += 1
st.sidebar.metric("Visits this session", st.session_state.visits)

# Cached helpers
@st.cache_data(show_spinner=False)
def count_text_bytes(text: str) -> int:
    return len(text.encode("utf-8"))

@st.cache_resource(show_spinner=False)
def get_placeholder_image():
    # Load a tiny placeholder image once
    img = Image.new("RGB", (200, 100), color=(240, 240, 240))
    return img

# --- main layout ---
st.title("Hello World")
st.caption("A compact tour of important widgets, state, layout, and caching.")

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.subheader("text and numbers")
    name = st.text_input("Your name", placeholder="Type here...")
    age = st.number_input("Your age", min_value=0, max_value=120, value=25, step=1)
    cool = st.checkbox("I like Streamlit 😎", value=True)
    mood = st.selectbox("Pick a mood", ["Happy", "Curious", "Productive", "Sleepy"], index=1)
    level = st.slider("Confidence level", min_value=0, max_value=100, value=70, step=5)

    st.write("---")
    st.subheader("file uploader")
    f = st.file_uploader("Upload an image (png/jpg)", type=["png", "jpg", "jpeg"])
    if f:
        img = Image.open(f).convert("RGB")
    else:
        img = get_placeholder_image()
    st.image(img, caption="Current image", use_column_width=True)

with col2:
    st.subheader("computed details")
    text_sample = f"Name: {name or 'Anonymous'} | Age: {age} | Mood: {mood} | Cool: {cool} | Confidence: {level}%"
    st.code(text_sample, language="text")
    st.write("Text byte length (cached):", count_text_bytes(text_sample))

    with st.expander("see raw session state"):
        st.json(st.session_state)

st.write("---")
st.subheader("chat ui preview")
st.caption("Use `st.chat_message` and `st.chat_input` to build assistants.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! Ask me anything about these widgets."}
    ]

# Render history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type a message")
if prompt:
    # Echo back and store
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = f"You said: **{prompt}**. By the way, confidence level is set to {level}%."
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

st.info("All done. Tweak inputs on the left and explore the components!") 