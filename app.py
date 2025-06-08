import streamlit as st
import requests
from transliterator import translit
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/mixtral-8x7b-instruct-v0.1"
HF_API_KEY = os.getenv("HF_API_KEY")

# Function to call Hugging Face API for LLM-based transliteration
def llm_transliterate(text):
    if not HF_API_KEY:
        st.error("Hugging Face API key not found. Please set HF_API_KEY in your environment.")
        return None
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    prompt = f"Transliterate the following Coptic text to Latin script, following standard Coptic pronunciation rules: {text}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 512, "temperature": 0.7}
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"].replace(prompt, "").strip()
    except Exception as e:
        st.error(f"Error with LLM API: {e}")
        return None

# Streamlit UI
st.title("Coptic Transliteration Tool")
st.markdown("Enter Coptic text or upload a file to transliterate to Latin script.")

# Text input
input_text = st.text_area("Enter Coptic Text", height=200)

# File uploader
uploaded_file = st.file_uploader("Upload a Coptic Text File (.txt)", type="txt")

# Transliteration logic
if st.button("Transliterate"):
    output_text = ""
    if input_text:
        # Apply rule-based transliteration as fallback
        rule_based_output = translit(input_text)
        # Try LLM-based transliteration
        llm_output = llm_transliterate(input_text)
        output_text = llm_output if llm_output else rule_based_output
    elif uploaded_file:
        # Read file content
        input_text = uploaded_file.read().decode("utf-8")
        rule_based_output = translit(input_text)
        llm_output = llm_transliterate(input_text)
        output_text = llm_output if llm_output else rule_based_output

    if output_text:
        st.subheader("Transliterated Text")
        st.write(output_text)
        # Download button
        st.download_button(
            label="Download Transliterated Text",
            data=output_text,
            file_name="transliterated_output.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please provide input text or upload a file.")

# Instructions
st.markdown("""
### Instructions
1. Enter Coptic text in the text area or upload a .txt file.
2. Click 'Transliterate' to convert the text to Latin script.
3. View the result and download it as a .txt file.

This tool combines the rule-based transliteration from [coptic-transliterator](https://github.com/shehatamichael/coptic-transliterator) with LLM-enhanced transliteration using Hugging Face's Inference API.
""")