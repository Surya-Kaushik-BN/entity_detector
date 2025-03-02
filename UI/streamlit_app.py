import streamlit as st
import json
import os
import sys

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_path)
from container.container_wire import container


def process_file(uploaded_file, entity, method):
    if uploaded_file is not None:
        try:
            conversations = json.load(uploaded_file)
            
            # Placeholder for actual entity detection logic
            entity_found = False  # Replace with your actual function call
            
            # Call your detection classes based on entity and method selection
            if entity == "Profanity Detection" and method == "Pattern Matching":
                detector = container.profane_regex_detector()
            elif entity == "Profanity Detection" and method == "LLM":
                detector = container.profane_llm_detector()
            elif entity == "Privacy and Compliance Detection" and method == "Pattern Matching":
                detector = container.verification_regex_detector()
            elif entity == "Privacy and Compliance Detection" and method == "LLM":
                detector = container.verification_llm_detector()
            
            entity_found = detector.detect_entity(conversations_list=conversations)
            st.write(f"Entity Matched: {'Yes' if entity_found else 'No'}")
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON.")
    else:
        st.warning("Please upload a JSON file.")

# Streamlit UI
st.title("Entity Detector")

# File upload
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

# Dropdown selections
entity = st.selectbox("Select Entity", ["Profanity Detection", "Privacy and Compliance Detection"])
method = st.selectbox("Select Method", ["Pattern Matching", "LLM"])

# Process file when button is clicked
if st.button("Detect Entity"):
    process_file(uploaded_file, entity, method)
