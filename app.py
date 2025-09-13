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

# Helper functions to determine if a question is related to specific roles
def is_programming_related(text):
    programming_keywords = [
        'code', 'programming', 'function', 'variable', 'loop', 'algorithm', 'debug', 'error', 'syntax',
        'python', 'javascript', 'java', 'c++', 'html', 'css', 'sql', 'api', 'database', 'framework',
        'library', 'package', 'import', 'class', 'method', 'array', 'string', 'integer', 'boolean',
        'git', 'github', 'repository', 'commit', 'branch', 'merge', 'pull request', 'deploy',
        'server', 'client', 'frontend', 'backend', 'fullstack', 'web development', 'mobile app',
        'software', 'application', 'script', 'command', 'terminal', 'console', 'ide', 'editor'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in programming_keywords)

def is_mental_health_related(text):
    mental_health_keywords = [
        'anxiety', 'depression', 'stress', 'mental health', 'therapy', 'counseling', 'emotions',
        'feelings', 'mood', 'wellness', 'mindfulness', 'meditation', 'self-care', 'coping',
        'trauma', 'ptsd', 'bipolar', 'adhd', 'autism', 'psychology', 'psychiatrist', 'therapist',
        'emotional', 'psychological', 'mental', 'wellbeing', 'happiness', 'sadness', 'anger',
        'fear', 'worry', 'panic', 'phobia', 'addiction', 'recovery', 'support', 'help'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in mental_health_keywords)

def is_science_related(text):
    science_keywords = [
        'science', 'physics', 'chemistry', 'biology', 'mathematics', 'research', 'experiment',
        'hypothesis', 'theory', 'scientific', 'discovery', 'molecule', 'atom', 'cell', 'dna',
        'evolution', 'genetics', 'quantum', 'relativity', 'gravity', 'energy', 'force', 'matter',
        'space', 'universe', 'galaxy', 'planet', 'star', 'earth', 'climate', 'environment',
        'laboratory', 'data', 'analysis', 'statistics', 'formula', 'equation', 'calculation',
        'observation', 'measurement', 'evidence', 'proof', 'study', 'investigation'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in science_keywords)

def is_story_related(text):
    story_keywords = [
        'story', 'storytelling', 'narrative', 'plot', 'character', 'protagonist', 'antagonist',
        'fiction', 'novel', 'book', 'writing', 'author', 'creative', 'imagination', 'fantasy',
        'adventure', 'romance', 'mystery', 'thriller', 'horror', 'comedy', 'drama', 'genre',
        'chapter', 'scene', 'dialogue', 'description', 'setting', 'theme', 'conflict', 'resolution',
        'beginning', 'middle', 'end', 'climax', 'twist', 'ending', 'character development',
        'world building', 'pacing', 'tone', 'style', 'voice', 'point of view', 'perspective'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in story_keywords)

def is_child_psychology_related(text):
    child_psychology_keywords = [
        'child', 'children', 'kid', 'kids', 'toddler', 'baby', 'infant', 'teenager', 'teen',
        'parenting', 'parent', 'family', 'development', 'behavior', 'behavioral', 'discipline',
        'education', 'learning', 'school', 'teacher', 'classroom', 'homework', 'study',
        'social', 'emotional', 'cognitive', 'physical', 'milestone', 'growth', 'maturity',
        'tantrum', 'aggression', 'shyness', 'anxiety', 'adhd', 'autism', 'special needs',
        'play', 'toys', 'games', 'activities', 'creativity', 'imagination', 'friendship',
        'bullying', 'peer pressure', 'self-esteem', 'confidence', 'independence', 'responsibility',
        'sleep', 'bedtime', 'eating', 'nutrition', 'screen time', 'technology', 'safety',
        'therapy', 'counseling', 'intervention', 'support', 'guidance', 'advice'
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in child_psychology_keywords)

def is_general_related(text):
    # Personal Assistant can handle general topics, so this returns True for most things
    # unless it's clearly specialized (programming, mental health, science, story, or child psychology)
    return not (is_programming_related(text) or is_mental_health_related(text) or 
                is_science_related(text) or is_story_related(text) or is_child_psychology_related(text))

# Page configuration
st.set_page_config(page_title="Gemini Chat", page_icon="🤖", layout="wide")

# Sidebar configuration
with st.sidebar:
    st.title("Settings")
    
    # API Key input
    api_key = st.text_input("GEMINI_API_KEY", type="password", 
                           value=os.getenv("GEMINI_API_KEY", ""))
    
    # Model selection
    model_name = st.selectbox("Model", 
                             ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"])
    
    # AI Role Selection
    st.subheader("AI Role Selection")
    ai_role = st.radio(
        "Select AI Role:",
        ["Code Generator", "Mental Health Consultant", "Science Buff", "Story Writer", "Personal Assistant", "Child Psychology"],
        index=0
    )
    
    # System instruction based on selected role
    role_instructions = {
        "Code Generator": "You are a code generator assistant. You only provide programming help, code examples, debugging assistance, and technical solutions. If asked about anything else, politely redirect to programming topics.",
        "Mental Health Consultant": "You are a mental health consultant. You provide supportive, empathetic responses about mental health, wellness, and emotional support. You are not a replacement for professional therapy.",
        "Science Buff": "You are a science expert. You provide detailed explanations about scientific concepts, research, discoveries, and scientific methodology. You make complex topics accessible and engaging.",
        "Story Writer": "You are a creative story writer. You help with storytelling, creative writing, character development, plot ideas, and narrative techniques. You inspire creativity and imagination.",
        "Personal Assistant": "You are a helpful personal assistant. You help with productivity, organization, scheduling, general knowledge, and daily tasks. You are friendly and efficient.",
        "Child Psychology": "You are a child psychology expert. You provide guidance on child development, behavioral issues, parenting strategies, educational approaches, and age-appropriate activities. You focus on healthy child development and positive parenting techniques."
    }
    
    system_instruction = role_instructions[ai_role]
    
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
st.title("Pushap Chehal's personal AI platform")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_prompt = st.chat_input("Ask something...")

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
        with st.spinner("Thinking..."):
            try:
                # Check if user is asking something outside the selected role
                if ai_role == "Code Generator" and not is_programming_related(user_prompt):
                    answer = "I am a code generator, please select appropriate option from the settings bar."
                elif ai_role == "Mental Health Consultant" and not is_mental_health_related(user_prompt):
                    answer = "I am a mental health consultant, please select appropriate option from the settings bar."
                elif ai_role == "Science Buff" and not is_science_related(user_prompt):
                    answer = "I am a science expert, please select appropriate option from the settings bar."
                elif ai_role == "Story Writer" and not is_story_related(user_prompt):
                    answer = "I am a story writer, please select appropriate option from the settings bar."
                elif ai_role == "Child Psychology" and not is_child_psychology_related(user_prompt):
                    answer = "I am a child psychology expert, please select appropriate option from the settings bar."
                elif ai_role == "Personal Assistant" and not is_general_related(user_prompt):
                    answer = "I am a personal assistant, please select appropriate option from the settings bar."
                else:
                    response = st.session_state.chat.send_message(user_prompt, generation_config=gen_config)
                    answer = response.text or "(No text in response)"
            except Exception as e:
                answer = f"Error: {e}"
            st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})