# First GenAI App - Gemini Chat Applications

This repository contains two Streamlit applications that demonstrate how to build interactive chat interfaces using Google's Gemini AI models. Perfect for beginners learning about Generative AI and Streamlit development.

## 🎯 What You'll Learn

### Core Concepts
- **Generative AI Integration**: How to connect and use Google's Gemini models
- **Streamlit Development**: Building interactive web applications with Python
- **Chat Interface Design**: Creating multi-turn conversational experiences
- **Session State Management**: Maintaining conversation history
- **Error Handling**: Graceful handling of API errors and edge cases

### Technical Skills
- Setting up Python virtual environments
- Managing dependencies with pip
- Environment variable configuration
- Real-time chat functionality
- Model parameter tuning

## 📁 Project Structure

```
First GenAI App/
├── app.py              # General purpose Gemini chat app
├── app copy.py         # Space-focused chat assistant
├── requirements.txt    # Python dependencies
├── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install streamlit google-generativeai python-dotenv pillow
```

### Step 3: Configure API Key
```bash
# Copy the environment template
cp env.example .env

# Edit .env file and add your API key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### Step 4: Run the Applications

#### General Chat App
```bash
streamlit run app.py
```

#### Space Assistant App
```bash
streamlit run "app copy.py"
```

Both apps will open in your browser at `http://localhost:8501`

## 📱 Applications Overview

### 1. General Chat App (`app.py`)
A versatile chat interface that can handle any topic:
- **Features**: Multi-turn conversations, model selection, parameter tuning
- **Use Cases**: General Q&A, brainstorming, content creation
- **Learning Focus**: Basic Gemini integration and Streamlit UI components

### 2. Space Assistant (`app copy.py`)
A specialized space-themed chat assistant:
- **Features**: Space-focused responses, themed UI elements
- **Use Cases**: Astronomy questions, space exploration topics
- **Learning Focus**: System prompts, specialized AI assistants

## ⚙️ Configuration Options

### Model Selection
- **gemini-2.0-flash**: Latest model, best performance
- **gemini-1.5-flash**: Good balance of speed and capability
- **gemini-2.5-flash**: Advanced model for complex tasks

### Generation Parameters
- **Temperature**: Controls creativity (0.0 = deterministic, 2.0 = very creative)
- **Top-p**: Nucleus sampling threshold for response diversity
- **Top-k**: Limits vocabulary selection for more focused responses
- **Max Tokens**: Maximum length of generated responses
---

**Happy coding! 🚀**
