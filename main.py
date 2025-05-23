import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any

# Set page config FIRST
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")

# Custom CSS for black and blue theme
st.markdown("""
    <style>
        :root {
            --primary: #1e3a8a;
            --secondary: #172554;
            --background: #0f172a;
            --text: #e2e8f0;
            --accent: #3b82f6;
        }
            
        .stApp {
            background-color: var(--background);
            color: var(--text);
        }
        
        .stTextArea textarea {
            background-color: var(--secondary) !important;
            color: var(--text) !important;
            border: 1px solid var(--accent) !important;
        }
        
        .stButton button {
            background-color: var(--primary) !important;
            color: white !important;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        
        .stButton button:hover {
            background-color: var(--accent) !important;
        }
        
        .stSuccess {
            background-color: var(--secondary) !important;
            border-left: 4px solid var(--accent) !important;
            padding: 1rem !important;
        }
        
        h1 {
            color: var(--accent) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load the .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Create a custom LangChain-compatible LLM wrapper
class GeminiLLM(LLM):
    model: Any = genai.GenerativeModel("gemini-1.5-flash")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.model.generate_content(prompt)
        return response.text

    @property
    def _llm_type(self) -> str:
        return "gemini-custom"

# Instantiate the model
llm = GeminiLLM()

# Streamlit UI
st.title("🤖 AI ChatBot For Saddam Hussain")

prompt = st.text_area("Enter your message:", placeholder="e.g., Who is founder of Pakistan?")

if st.button("Send"):
    if prompt.strip():
        with st.spinner("Thinking..."):
            try:
                response = llm(prompt)
                st.success("Response:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("Please enter a prompt.")