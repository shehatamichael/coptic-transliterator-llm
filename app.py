import streamlit as st
import requests
from transliterator import translit
import os
from dotenv import load_dotenv
import time
from typing import Optional
import hashlib
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file

# Get API key from Streamlit secrets or environment variables
try:
    # Try Streamlit secrets first (for deployed app)
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        logger.info("GEMINI_API_KEY loaded from Streamlit secrets")
    # Fallback to environment variable (for local development)
    elif "GEMINI_API_KEY" in os.environ:
        GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        logger.info("GEMINI_API_KEY loaded from environment variable")
    else:
        GEMINI_API_KEY = None
        logger.error("GEMINI_API_KEY not found in secrets or environment variables")
        st.error("⚠️ API key not configured. Please contact the administrator.")
        st.stop()

except Exception as e:
    logger.error(f"Error loading API key: {str(e)}")
    st.error("⚠️ Error loading API configuration. Please contact the administrator.")
    st.stop()

# Google AI Studio API configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-001:generateContent"  # Adjust endpoint based on Google's latest API


# Cache for API responses to improve performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_llm_transliterate(text_hash: str, text: str) -> Optional[str]:
    """Cached LLM transliteration to avoid repeated API calls"""
    return llm_transliterate_internal(text)


def llm_transliterate_internal(text: str) -> Optional[str]:
    """Internal function for LLM transliteration using Gemini 2.0 Flash"""
    if not GEMINI_API_KEY:
        return None

    headers = {
        "Content-Type": "application/json",
    }

    # Prompt optimized for Gemini 2.0 Flash Lite
    prompt = f"""You are an expert in Coptic language transliteration. Your task is to transliterate Coptic text to Latin script using standard transliteration conventions.
        
        Examples:
        - ⲡⲛⲟⲩⲧⲉ → pnoute
        - ⲧⲉⲕⲕⲗⲏⲥⲓⲁ → tekklesia  
        - ⲁⲅⲁⲡⲏ → agape
        - ⲙⲁⲣⲓⲁ → maria

        Rules:
        - Convert each Coptic character to its Latin equivalent
        - Preserve word boundaries and spacing
        - Use lowercase Latin letters
        - Do not add explanations or additional text
        - **Crucially: The output MUST contain ONLY plain, unaccented Latin characters (ASCII a-z). No Coptic characters, no diacritics, and no special Latin characters (e.g., ā, ē, ī, ō, ū) are allowed in the final transliterated text.**
        - Only return the transliterated text

        Transliterate this Coptic text to Latin script: {text}"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 2048,
            "topP": 0.9,
            "topK": 40,
        },
    }

    try:
        request_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(request_url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"API Response: {result}")

        # Extract the generated text (specific to Gemini's response structure)
        generated_text = None
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and "candidates" in result:
                for candidate in result["candidates"]:
                    if "content" in candidate and "parts" in candidate["content"]:
                        for part in candidate["content"]["parts"]:
                            if "text" in part:
                                generated_text = part["text"]
                                break
                    if generated_text:
                        break
        else:
            logger.error(
                f"Gemini API request failed with status {response.status_code}: {response.text}"
            )
            return None

        if generated_text:
            generated_text = generated_text.strip()

            # remove unwanted prefixes like "Transliteration:"
            if generated_text.lower().startswith("transliteration:"):
                generated_text = generated_text[len("transliteration:") :].strip()

            return generated_text

        return None

    except requests.exceptions.Timeout:
        st.warning(
            "⏱️ API request timed out. The model might be loading. Using rule-based transliteration."
        )
        return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            st.warning("🔧 Rate limit exceeded. Using rule-based transliteration.")
        elif e.response.status_code == 503:
            st.warning(
                "🔄 Model is loading. This may take a few minutes for the first request. Using rule-based transliteration."
            )
        else:
            st.warning(
                "🔌 API temporarily unavailable. Using rule-based transliteration."
            )
        return None
    except requests.exceptions.RequestException as e:
        st.warning("🔌 Network issue. Using rule-based transliteration.")
        logger.error(f"Request error: {e}")
        return None
    except Exception as e:
        st.warning("⚠️ Using rule-based transliteration due to API issues.")
        logger.error(f"Unexpected error: {e}")
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
    initial_sidebar_state="expanded",
)

# CSS styling
st.markdown(
    """
<style>
    /* Global dark theme settings */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Info boxes with dark theme visibility */
    .info-box {
        background: linear-gradient(135deg, #262730 0%, #1e1e2e 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .info-box h4 {
        color: #ffffff;
        margin-top: 0;
        font-weight: 600;
    }
    
    .info-box ul {
        margin-bottom: 0;
    }
    
    .info-box li {
        margin: 0.5rem 0;
        color: #ffffff;
    }
    
    /* Result box styling */
    .result-info {
        background: linear-gradient(135deg, #1a4d2e 0%, #0f3320 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #28a745;
        margin: 1rem 0;
        color: #ffffff;
        box-shadow: 0 2px 10px rgba(40, 167, 69, 0.2);
    }
    
    .result-info strong {
        color: #ffffff;
    }
    
    /* Results section styling */
    .results-container {
        background: linear-gradient(135deg, #2a2d3a 0%, #1f2029 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #667eea;
        margin: 2rem 0;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    .method-header {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .rule-based-header {
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        border: 1px solid #718096;
    }
    
    .ai-enhanced-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 1px solid #667eea;
    }
    
    /* Text area */
    .stTextArea textarea {
        background-color: #1a1a2e !important;
        border: 2px solid #404040 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #888888 !important;
        opacity: 0.8 !important;
    }
    
    .stTextArea textarea[disabled] {
        background-color: #2d3748 !important;
        border-color: #4a5568 !important;
        color: #f7fafc !important;
        opacity: 1 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        line-height: 1.7 !important;
        text-shadow: 0 0 1px rgba(255,255,255,0.5) !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #262730 !important;
        border: 2px dashed #404040 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: transform 0.2s ease !important;
        min-height: 44px !important;
        white-space: normal !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Ensure button containers are visible */
    .stButton {
        display: block !important;
        width: 100% !important;
    }
    
    /* Download button specific styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #218838 0%, #1e9a7e 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Section headers - FIXED */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Ensure columns are visible */
    .stColumn {
        color: #ffffff !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Footer styling */
    .footer-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .footer-box h3 {
        margin-top: 0;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1a1a2e !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background-color: #667eea !important;
    }
    
    /* Expander styling */
    .streamlit-expander {
        background-color: #262730 !important;
        border: 1px solid #404040 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expander .streamlit-expanderHeader {
        background-color: #262730 !important;
        color: #ffffff !important;
    }
    
    .streamlit-expander .streamlit-expanderContent {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
    }
    
    /* Metric styling for sidebar */
    .metric-container {
        background-color: #262730 !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #404040 !important;
    }
    
    /* Alert/warning boxes */
    .stAlert {
        background-color: #262730 !important;
        border: 1px solid #404040 !important;
        color: #ffffff !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #1a4d2e !important;
        border: 1px solid #28a745 !important;
        color: #ffffff !important;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #4d3319 !important;
        border: 1px solid #ffc107 !important;
        color: #ffffff !important;
    }
    
    /* Info message styling */
    .stInfo {
        background-color: #1a2a4d !important;
        border: 1px solid #17a2b8 !important;
        color: #ffffff !important;
    }
    
    /* Error message styling */
    .stError {
        background-color: #4d1a1a !important;
        border: 1px solid #dc3545 !important;
        color: #ffffff !important;
    }
    
    /* General text */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        display: block !important;
        visibility: visible !important;
    }
    
    p, li, span {
        color: #ffffff !important;
    }
    
    /* Markdown content styling */
    .stMarkdown {
        color: #ffffff !important;
        display: block !important;
        visibility: visible !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* labels visiblilty */
    label {
        color: #ffffff !important;
    }
    
    /* Help text styling */
    .stTextInput > div > div > input + div {
        color: #888888 !important;
    }
    
    /* Download section styling */
    .download-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #3b82f6;
    }
    
    .download-section h4 {
        color: #ffffff;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    /* Ensure all main containers are visible */
    div[data-testid="stVerticalBlock"] {
        display: block !important;
        visibility: visible !important;
    }
    
    div[data-testid="column"] {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Make sure button containers are always visible */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        visibility: visible !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
    [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/shehatamichael/coptic-transliterator-llm)
    """
    )

    st.markdown("---")

    st.markdown(
        """
    ### 🤝 Contribute
    - [Report Issues](https://github.com/shehatamichael/coptic-transliterator-llm/issues)
    - [Submit Pull Requests](https://github.com/shehatamichael/coptic-transliterator-llm/pulls)
    - [Fork the Project](https://github.com/shehatamichael/coptic-transliterator-llm/fork)
    """
    )

    st.markdown("---")

    # API Status indicator with debugging
    st.markdown("### 🔌 AI Model Status")
    if GEMINI_API_KEY:
        st.success("✅ AI Enhancement Available")
        st.info("Using Gemini 2.0 Flash Lite for superior accuracy")

    else:
        st.warning("⚠️ Rule-based Mode Only")
        st.info("Set GEMINI_API_KEY for AI enhancement")

    st.markdown("---")

    # Usage statistics
    if "transliteration_count" not in st.session_state:
        st.session_state.transliteration_count = 0

    st.markdown(f"### 📊 Session Stats")
    st.metric("Transliterations", st.session_state.transliteration_count)

    st.markdown("---")

    st.markdown("### ℹ️ How It Works")
    st.markdown(
        """
    <div class="info-box">
        <h4>Two-Method Comparison:</h4>
        <strong>1️⃣ Rule-based</strong> transliteration (fast, consistent)<br>
        <strong>2️⃣ AI enhancement</strong> with Gemini 2.0 Flash Lite (context-aware improvements)<br><br>
        <strong>📊 Side-by-side results</strong> let you compare both methods!
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 Features")
    st.markdown(
        """
    <div class="info-box">
        <ul>
            <li>✅ Handles complex Coptic characters</li>
            <li>✨ Advanced AI with Gemini 2.0 Flash Lite</li>
            <li>📊 Method comparison view</li>
            <li>📱 Mobile-friendly interface</li>
            <li>⬇️ Download results</li>
            <li>🆓 Completely free to use</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        """
    ### 📧 Contact
    **Michael Shehata**  
    📧 shehatam.dev@gmail.com
    
    ### ⭐ Support
    If this tool helps you, consider giving it a star on GitHub!
    """
    )

# Main header
st.markdown(
    """
<div class="main-header">
    <h1>📱 Coptic Transliteration Tool</h1>
    <p>AI-enhanced transliteration with Gemini 2.0 Flash Lite for Coptic text to Latin script</p>
</div>
""",
    unsafe_allow_html=True,
)

# Initialize session state for input text
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Quick examples section
st.markdown("#### ✨ Try These Examples")
st.markdown("---")

# Force visibility for this section
st.markdown(
    '<div style="display: block !important; visibility: visible !important;">',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

example_texts = [("ⲡⲛⲟⲩⲧⲉ", "God"), ("ⲧⲉⲕⲕⲗⲏⲥⲓⲁ", "Church"), ("ⲁⲅⲁⲡⲏ", "Love")]

for i, (coptic, english) in enumerate(example_texts):
    with [col1, col2, col3][i]:
        button_html = f"""
        <div style="display: block !important; visibility: visible !important; margin-bottom: 1rem;">
        """
        st.markdown(button_html, unsafe_allow_html=True)

        if st.button(
            f"{coptic}\n({english})",
            key=f"example_{i}",
            use_container_width=True,
            help=f"Click to load example: {coptic} ({english})",
        ):
            st.session_state.input_text = coptic
            st.rerun()  # Force a rerun to update the input field

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # Close the forced visibility div

# MAIN INTERFACE
st.markdown("---")
st.markdown("#### 🔄 Transliteration Interface")
st.markdown("---")

# Create two main columns: Input (left) and Results (right)
main_col1, main_col2 = st.columns([1, 1])

with main_col1:
    st.markdown("##### 📝 Input")

    # Text input with session state management
    input_text = st.text_area(
        "Enter Coptic Text",
        height=200,
        placeholder="Paste your Coptic text here or click an example above...",
        value=st.session_state.input_text,
        help="You can type or paste Coptic Unicode text here",
        key="text_input",
    )

    # Update session state when text changes
    if input_text != st.session_state.input_text:
        st.session_state.input_text = input_text

    # File uploader
    uploaded_file = st.file_uploader(
        "Or Upload a Text File",
        type="txt",
        help="Upload a .txt file containing Coptic text",
    )

    # Transliteration button
    if st.button("🚀 Transliterate Text", type="primary", use_container_width=True):
        processing_text = ""

        # Check for input text from text area
        if input_text and input_text.strip():
            processing_text = input_text.strip()
        # Check for uploaded file
        elif uploaded_file:
            try:
                processing_text = uploaded_file.read().decode("utf-8").strip()
            except Exception as e:
                st.error(
                    "❌ Error reading file. Please ensure it's a valid UTF-8 text file."
                )

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
                llm_output = None
                if GEMINI_API_KEY:
                    status_text.text("✨ Enhancing with Gemini 2.0 Flash Lite...")
                    progress_bar.progress(75)

                    llm_output = llm_transliterate(processing_text)

                    # Debug information
                    if llm_output:
                        st.success("✅ AI enhancement successful!")
                    else:
                        st.info(
                            "ℹ️ AI enhancement unavailable (model may be loading), showing rule-based result in both columns"
                        )
                        llm_output = (
                            rule_based_output  # Fallback to rule-based for display
                        )
                else:
                    st.info(
                        "ℹ️ API key not configured, showing rule-based result in both columns"
                    )
                    llm_output = rule_based_output  # Fallback to rule-based for display

                progress_bar.progress(100)
                status_text.text("✅ Transliteration completed!")

                # Update session stats
                st.session_state.transliteration_count += 1

                # Store results in session state to display them in the right column
                st.session_state.results = {
                    "rule_based": rule_based_output,
                    "llm_output": llm_output,
                    "processing_text": processing_text,
                    "has_results": True,
                }

                # Clear progress indicators
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()

            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(
                    f"❌ An error occurred during transliteration. Please try again."
                )
                st.error(f"Error details: {str(e)}")

        else:
            st.warning("⚠️ Please provide input text or upload a file.")

with main_col2:
    st.markdown("##### 📊 Results")

    # Display results if they exist
    if "results" in st.session_state and st.session_state.results.get(
        "has_results", False
    ):
        # Method information
        rule_based_output = st.session_state.results["rule_based"]
        llm_output = st.session_state.results["llm_output"]
        processing_text = st.session_state.results["processing_text"]

        ai_status = (
            "Gemini 2.0 Flash Lite Enhanced"
            if GEMINI_API_KEY and llm_output != rule_based_output
            else "Rule-based (Fallback)"
        )
        st.markdown(
            f"""
        <div class="result-info">
            <strong>Input Length:</strong> {len(processing_text)} characters<br>
            <strong>Rule-based Output:</strong> {len(rule_based_output)} characters<br>
            <strong>AI-Enhanced Output:</strong> {len(llm_output)} characters<br>
            <strong>AI Model:</strong> {ai_status}
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Rule-based result
        st.markdown(
            '<div class="method-header rule-based-header">📝 Rule-based Method</div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "Rule-based Transliteration",
            value=(
                rule_based_output
                if rule_based_output
                else "Results will appear here after transliteration"
            ),
            height=100,
            disabled=True,
            key="rule_result_display",
            help="Fast, consistent transliteration based on linguistic rules",
            label_visibility="collapsed",
        )

        # AI-enhanced result
        st.markdown(
            '<div class="method-header ai-enhanced-header">✨ Gemini 2.0 Flash Lite Enhanced</div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "AI-Enhanced Transliteration",
            value=(
                llm_output
                if llm_output
                else "Results will appear here after transliteration"
            ),
            height=100,
            disabled=True,
            key="ai_result_display",
            help="Context-aware improvements using Meta Gemini 2.0 Flash Lite model",
            label_visibility="collapsed",
        )

        # Download section
        st.markdown("#### ⬇️ Download Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="📝 Rule-based",
                data=rule_based_output,
                file_name=f"rule_based_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download the rule-based transliteration",
            )

        with col2:
            st.download_button(
                label="✨ Gemini Enhanced",
                data=llm_output,
                file_name=f"gemini_enhanced_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download the Gemini 2.0 Flash Lite enhanced transliteration",
            )

        with col3:
            # Combined download with both methods
            combined_output = (
                f"Rule-based Transliteration:\n{rule_based_output}\n\n"
                + f"Gemini 2.0 Flash Lite Enhanced Transliteration:\n{llm_output}\n\n"
                + f"Original Coptic Text:\n{processing_text}"
            )

            st.download_button(
                label="📊 Both",
                data=combined_output,
                file_name=f"combined_results_{int(time.time())}.txt",
                mime="text/plain",
                use_container_width=True,
                help="Download both transliterations in one file",
            )

        # Additional information if methods differ
        if rule_based_output != llm_output and GEMINI_API_KEY:
            st.info(
                "💡 **Different Results Detected:** The AI-enhanced method produced a different result than the rule-based method. Compare both to see which better fits your needs!"
            )
        elif not GEMINI_API_KEY:
            st.warning(
                "🔑 **API Key Not Configured:** Set your Google AI Studio API key to enable AI-enhanced transliteration for potentially improved results."
            )

    else:
        # Placeholder when no results
        st.info(
            "Enter text or upload a file and click 'Transliterate' to see results here!"
        )

        # Show empty text areas as placeholders
        st.markdown(
            '<div class="method-header rule-based-header">📝 Rule-based Method</div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "Rule-based Transliteration",
            value="Results will appear here after transliteration",
            height=100,
            disabled=True,
            key="rule_placeholder",
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="method-header ai-enhanced-header">✨ AI-Enhanced Method</div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            "AI-Enhanced Transliteration",
            value="Results will appear here after transliteration",
            height=100,
            disabled=True,
            key="ai_placeholder",
            label_visibility="collapsed",
        )

# Instructions section
st.markdown("---")
st.markdown("### 📖 Instructions")

with st.expander("📖 How to Use This Tool", expanded=False):
    st.markdown(
        """
    ### 🚀 Quick Start Guide
    
    1. **Choose Input Method:**
       - Type/paste Coptic text directly in the text area
       - Upload a `.txt` file containing Coptic text
       - Click one of the example buttons for quick testing
    
    2. **Transliterate:**
       - Click the "🚀 Transliterate Text" button
       - Wait for processing (usually takes 2-5 seconds)
       - View your results in the Results panel on the right
    
    3. **Compare & Choose:**
       - Review both the Rule-based and AI-Enhanced results
       - Choose the method that works best for your text
       - Download individual results or both together
    
    4. **Save Results:**
       - Download rule-based results as `.txt` file
       - Download AI-enhanced results as `.txt` file
       - Download combined results with both methods
    
    ### 🔧 Technical Details
    
    **Rule-based Transliteration:**
    - Fast and consistent
    - Based on linguistic rules
    - Works offline
    - Handles all standard Coptic characters
    - Always available as fallback
    
    **AI Enhancement:**
    - Uses Gemini 2.0 Flash Lite language model
    - Context-aware improvements
    - Better handling of ambiguous cases
    - Requires internet connection and API key
    - Shows rule-based result if unavailable
    
    ### 📊 Side-by-Side Comparison
    
    **Why Both Methods?**
    - Different approaches may yield different results
    - Rule-based is consistent and predictable
    - AI-enhanced considers context and patterns
    - You can choose the best result for your needs
    """
    )

# Footer
st.markdown("---")
st.markdown(
    """
<div class="footer-box">
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
""",
    unsafe_allow_html=True,
)
