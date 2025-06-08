import streamlit as st
import requests
from transliterator import translit
import os
from dotenv import load_dotenv
import time
from typing import Optional
import hashlib

load_dotenv()  # Load environment variables from .env file

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_API_KEY = os.getenv("HF_API_KEY")

# Cache for API responses to improve performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_llm_transliterate(text_hash: str, text: str) -> Optional[str]:
    """Cached LLM transliteration to avoid repeated API calls"""
    return llm_transliterate_internal(text)

def llm_transliterate_internal(text: str) -> Optional[str]:
    """Internal function for LLM transliteration"""
    if not HF_API_KEY:
        return None
    
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    # Improved prompt for better Coptic transliteration
    prompt = f"""Convert the following Coptic text to Latin script using standard Coptic pronunciation rules. 
Provide only the transliterated text without explanations:

Coptic: {text}
Latin: """
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.3,  # Lower temperature for more consistent results
            "return_full_text": False
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "").strip()
            # Clean up the response - remove the prompt if it's included
            if "Latin:" in generated_text:
                generated_text = generated_text.split("Latin:")[-1].strip()
            return generated_text if generated_text else None
        
        return None
        
    except requests.exceptions.Timeout:
        st.warning("⏱️ API request timed out. Using rule-based transliteration.")
        return None
    except requests.exceptions.RequestException as e:
        st.warning("🔌 API temporarily unavailable. Using rule-based transliteration.")
        return None
    except Exception as e:
        st.warning("⚠️ Using rule-based transliteration due to API issues.")
        return None

def llm_transliterate(text: str) -> Optional[str]:
    """Public function for LLM transliteration with caching"""
    if not text or not text.strip():
        return None
    
    # Create hash for caching
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return cached_llm_transliterate(text_hash, text)

# Page configuration
st.set_page_config(
    page_title="Coptic Transliteration Tool",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .example-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with enhanced information
with st.sidebar:
    st.markdown("## 🔗 Quick Links")
    
    st.markdown("""
    ### 📁 Source Code
    [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/shehatamichael/coptic-transliterator-llm)
    
    **[View Source Code →](https://github.com/shehatamichael/coptic-transliterator-llm)**
    """)
    
    st.markdown("""
    ### 🤝 Contribute
    - [Report Issues](https://github.com/shehatamichael/coptic-transliterator-llm/issues)
    - [Submit Pull Requests](https://github.com/shehatamichael/coptic-transliterator-llm/pulls)
    - [Fork the Project](https://github.com/shehatamichael/coptic-transliterator-llm/fork)
    """)
    
    st.markdown("---")
    
    # API Status indicator
    st.markdown("### 🔌 API Status")
    if HF_API_KEY:
        st.success("✅ AI Enhancement Active")
        st.info("Using Mixtral-8x7B for improved accuracy")
    else:
        st.warning("⚠️ Rule-based Mode Only")
        st.info("Set HF_API_KEY for AI enhancement")
    
    st.markdown("---")
    
    # Usage statistics (if you want to track)
    if 'transliteration_count' not in st.session_state:
        st.session_state.transliteration_count = 0
    
    st.markdown(f"### 📊 Session Stats")
    st.metric("Transliterations", st.session_state.transliteration_count)
    
    st.markdown("---")
    
    st.markdown("""
    ### 📧 Contact
    **Michael Shehata**  
    📧 shehatam.dev@gmail.com
    
    ### ⭐ Support
    If this tool helps you, consider giving it a star on GitHub!
    """)

# Enhanced main header
st.markdown("""
<div class="main-header">
    <h1>📱 Coptic Transliteration Tool</h1>
    <p style="margin: 0; opacity: 0.9;">AI-enhanced transliteration for Coptic text to Latin script</p>
</div>
""", unsafe_allow_html=True)

# Quick examples section
st.markdown("### ✨ Try These Examples")
col1, col2, col3 = st.columns(3)

example_texts = [
    ("ⲡⲛⲟⲩⲧⲉ", "God"),
    ("ⲧⲉⲕⲕⲗⲏⲥⲓⲁ", "Church"),
    ("ⲁⲅⲁⲡⲏ", "Love")
]

for i, (coptic, english) in enumerate(example_texts):
    with [col1, col2, col3][i]:
        if st.button(f"{coptic}\n({english})", key=f"example_{i}", use_container_width=True):
            st.session_state.example_text = coptic

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Input")
    
    # Use example text if selected
    default_text = st.session_state.get('example_text', '')
    
    # Text input with better placeholder
    input_text = st.text_area(
        "Enter Coptic Text", 
        height=200, 
        placeholder="Paste your Coptic text here or click an example above...",
        value=default_text,
        help="You can type or paste Coptic Unicode text here"
    )
    
    # Clear the example text after use
    if 'example_text' in st.session_state:
        del st.session_state.example_text

    # File uploader with better description
    uploaded_file = st.file_uploader(
        "Or Upload a Text File", 
        type="txt",
        help="Upload a .txt file containing Coptic text"
    )

with col2:
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    <div class="example-box">
    <strong>Two-Stage Process:</strong><br>
    1️⃣ <strong>Rule-based</strong> transliteration (fast, consistent)<br>
    2️⃣ <strong>AI enhancement</strong> (context-aware improvements)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    - ✅ Handles complex Coptic characters
    - 🤖 AI-powered improvements
    - 📱 Mobile-friendly interface
    - ⬇️ Download results
    - 🆓 Completely free to use
    """)

# Enhanced transliteration section
st.markdown("---")

# Transliteration button with better styling
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Transliterate Text", type="primary", use_container_width=True):
        processing_text = ""
        
        if input_text.strip():
            processing_text = input_text.strip()
        elif uploaded_file:
            try:
                processing_text = uploaded_file.read().decode("utf-8").strip()
            except Exception as e:
                st.error("❌ Error reading file. Please ensure it's a valid UTF-8 text file.")
        
        if processing_text:
            # Create progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Starting transliteration...")
            progress_bar.progress(25)
            
            try:
                # Rule-based transliteration (always works)
                status_text.text("📝 Applying rule-based transliteration...")
                progress_bar.progress(50)
                
                rule_based_output = translit(processing_text)
                
                # AI enhancement (if available)
                if HF_API_KEY:
                    status_text.text("🤖 Enhancing with AI...")
                    progress_bar.progress(75)
                    
                    llm_output = llm_transliterate(processing_text)
                    final_output = llm_output if llm_output else rule_based_output
                    method_used = "AI-Enhanced" if llm_output else "Rule-based"
                else:
                    final_output = rule_based_output
                    method_used = "Rule-based"
                
                progress_bar.progress(100)
                status_text.text("✅ Transliteration completed!")
                
                # Update session stats
                st.session_state.transliteration_count += 1
                
                # Clear progress indicators
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                st.markdown("### 📄 Results")
                
                st.markdown(f"""
                <div class="result-box">
                <strong>Method Used:</strong> {method_used}<br>
                <strong>Input Length:</strong> {len(processing_text)} characters<br>
                <strong>Output Length:</strong> {len(final_output)} characters
                </div>
                """, unsafe_allow_html=True)
                
                # Result text area
                st.text_area(
                    "Transliterated Text", 
                    value=final_output, 
                    height=150, 
                    disabled=True,
                    help="This is your transliterated text. Use the download button below to save it."
                )
                
                # Enhanced download section
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="⬇️ Download Result",
                        data=final_output,
                        file_name=f"transliterated_{int(time.time())}.txt",
                        mime="text/plain",
                        type="secondary",
                        use_container_width=True,
                        help="Download the transliterated text as a .txt file"
                    )
                
                with col2:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.info("💡 Use Ctrl+A then Ctrl+C to copy the text above")
                
                # Comparison view if AI was used
                if HF_API_KEY and llm_output and llm_output != rule_based_output: # type: ignore
                    with st.expander("🔍 Compare Methods", expanded=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Rule-based:**")
                            st.text_area("", value=rule_based_output, height=100, disabled=True, key="rule_result")
                        
                        with col2:
                            st.markdown("**AI-Enhanced:**")
                            st.text_area("", value=llm_output, height=100, disabled=True, key="ai_result")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ An error occurred during transliteration. Please try again.")
                st.error(f"Error details: {str(e)}")
        
        else:
            st.warning("⚠️ Please provide input text or upload a file.")

# Enhanced instructions
st.markdown("---")

with st.expander("📖 Detailed Instructions", expanded=False):
    st.markdown("""
    ### 🚀 Quick Start Guide
    
    1. **Choose Input Method:**
       - Type/paste Coptic text directly in the text area
       - Upload a `.txt` file containing Coptic text
       - Click one of the example buttons for quick testing
    
    2. **Transliterate:**
       - Click the "🚀 Transliterate Text" button
       - Wait for processing (usually takes 2-5 seconds)
       - View your results below
    
    3. **Save Results:**
       - Download as a `.txt` file for later use
       - Copy text manually using the text area
    
    ### 🔧 Technical Details
    
    **Rule-based Transliteration:**
    - Fast and consistent
    - Based on linguistic rules
    - Works offline
    - Handles all standard Coptic characters
    
    **AI Enhancement:**
    - Uses Mixtral-8x7B language model
    - Context-aware improvements
    - Better handling of ambiguous cases
    - Requires internet connection
    
    ### 📚 Supported Characters
    
    This tool handles all standard Coptic Unicode characters including:
    - Basic Coptic alphabet (ⲁ-ⲱ)
    - Extended characters (ϣ, ϥ, ϧ, ϩ, ϫ, ϭ, ϯ)
    - Both uppercase and lowercase
    - Punctuation and spaces
    
    ### 🎯 Best Practices
    
    - **Text Quality:** Ensure your Coptic text uses proper Unicode characters
    - **File Format:** Use UTF-8 encoded `.txt` files for uploads
    - **Length:** Works best with text under 1000 characters per request
    - **Context:** Longer texts generally get better AI enhancement
    """)

# Enhanced footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 15px; margin: 20px 0; color: white;">
    <h3>🛠️ Open Source & Free Forever</h3>
    <p style="font-size: 1.1em; margin: 15px 0;">
        This tool is completely open source and will always be free to use!
    </p>
    <p>
        <a href="https://github.com/shehatamichael/coptic-transliterator-llm" target="_blank" 
           style="text-decoration: none; color: white;">
            <img src="https://img.shields.io/badge/⭐_Star_on_GitHub-white?style=for-the-badge&logo=github&logoColor=black" 
                 alt="Star on GitHub">
        </a>
    </p>
    <p style="margin-top: 20px; font-size: 1.1em;">
        <strong>Made with ❤️ for the Coptic community</strong>
    </p>
    <p style="font-style: italic; opacity: 0.9;">
        Preserving ancient language through modern technology
    </p>
</div>
""", unsafe_allow_html=True)

# Developer info
st.markdown("""
<div style="text-align: center; margin-top: 20px; padding: 15px; background-color: #f8f9fa; 
            border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin: 5px 0; color: #6c757d;">
        💡 <strong>Suggestions?</strong> 
        <a href="https://github.com/shehatamichael/coptic-transliterator-llm/issues/new" target="_blank">Report issues</a> | 
        <a href="https://github.com/shehatamichael/coptic-transliterator-llm/discussions" target="_blank">Feature requests</a> |
        <a href="mailto:shehatam.dev@gmail.com">Contact developer</a>
    </p>
</div>
""", unsafe_allow_html=True)