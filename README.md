# 🔤 Coptic Transliteration Tool with LLM

> A modern web-based tool for transliterating Coptic text to Latin script, perfect for English speakers following church services.

<!-- TODO: Update with actual images from netlify -->
<!-- [![Netlify Status](https://api.netlify.com/api/v1/badges/your-badge-id/deploy-status)](https://app.netlify.com/sites/your-site-name/deploys)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) -->

---

## ✨ Features

- **🖊️ Flexible Input**: Enter Coptic text directly or upload `.txt` files
- **🤖 AI-Enhanced**: Combines rule-based transliteration with LLM improvements via Hugging Face
- **📱 User-Friendly**: Clean Streamlit interface accessible from any device  
- **⬇️ Export Ready**: Download transliterated results as `.txt` files
- **💰 Free to Use**: Leverages Hugging Face's free tier and Netlify hosting

---

## 🚀 Quick Start

### Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (required for Pynini)
- [Hugging Face Account](https://huggingface.co/join) (for API access)

### Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shehatamichael/coptic-transliterator-llm.git
   cd coptic-transliterator-llm
   ```

2. **Create Environment**
   ```bash
   conda create --name coptic-llm python=3.9
   conda activate coptic-llm
   ```

3. **Install Dependencies**
   ```bash
   conda install -c conda-forge pynini
   pip install -r requirements.txt
   ```

4. **Configure API Access**
   - Get your [Hugging Face API key](https://huggingface.co/settings/tokens)
   - Create `.env` file:
     ```env
     HF_API_KEY=your-hugging-face-api-key-here
     ```

5. **Launch the App**
   ```bash
   streamlit run app.py
   ```

   Your app will be available at `http://localhost:8501`

---

## 🌐 Deploy to Netlify

### Step-by-Step Deployment

1. **Prepare Your Repository**
   - Push your code to GitHub
   - Ensure `netlify.toml` is in your root directory
   - Verify all dependencies are listed in `requirements.txt`

2. **Connect to Netlify**
   - Log in to [Netlify](https://netlify.com)
   - Click "New site from Git"
   - Select your GitHub repository

3. **Configure Environment Variables**
   - Go to Site settings → Build & deploy → Environment variables
   - Add your Hugging Face API key:
     ```
     Key: HF_API_KEY
     Value: your-hugging-face-api-key-here
     ```

4. **Deploy**
   - Netlify will automatically build and deploy using `netlify.toml`
   - Your app will be live at `https://your-app-name.netlify.app`

### Deployment Configuration

The repository includes a `netlify.toml` file that handles:
- Python runtime setup
- Dependency installation
- Streamlit app startup

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │  Rule-based      │    │  Hugging Face   │
│   Frontend      │───▶│  Transliterator  │───▶│  LLM API        │
│                 │    │  (Fallback)      │    │  (Enhancement)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

- **Frontend**: Streamlit provides the web interface
- **Core Logic**: Rule-based transliteration from `coptic-transliterator`
- **Enhancement**: Mixtral-8x7B model via Hugging Face API
- **Hosting**: Netlify for free, scalable deployment

---

## 📁 Project Structure

```
coptic-transliterator-llm/
├── app.py                 # Main Streamlit application
├── transliterator.py      # Core transliteration logic
├── requirements.txt       # Python dependencies
├── netlify.toml          # Netlify deployment config
├── .env                  # Environment variables (local)
└── README.md             # This file
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HF_API_KEY` | Hugging Face API key for LLM access | Yes |

### Model Configuration

The default LLM model is Mixtral-8x7B. To use a different model, update the `HF_API_URL` in `app.py`:

```python
HF_API_URL = "https://api-inference.huggingface.co/models/your-model-name"
```

> **Note**: Ensure your chosen model is under 10GB to stay within Hugging Face's free tier limits.

---

## 🔧 Advanced Usage

### Fine-tuning for Better Accuracy

For improved Coptic-specific results, consider:

1. **Custom Model Training**: Fine-tune Mistral-7B on Coptic datasets
2. **Prompt Engineering**: Optimize prompts for better transliteration
3. **Hybrid Approach**: Combine multiple models for enhanced accuracy

### API Integration

The tool can be integrated into other applications via the Streamlit API or by extracting the core transliteration functions.

---

## 📊 Performance & Limitations

### Free Tier Considerations

- **Hugging Face**: Rate limits apply to API calls
- **Netlify**: 300 build minutes/month, 100GB bandwidth
- **Cold Starts**: Initial requests may be slower due to model loading

### Accuracy Notes

- Rule-based transliteration provides consistent baseline results
- LLM enhancement improves context-aware transliteration
- Performance varies with input complexity and model availability

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
4. **Submit a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code style
- Add tests for new functionality
- Update documentation as needed
- Ensure compatibility with free tier services

---

## 📚 Citation

If you use this tool in your research or projects, please cite:

```bibtex
@misc{shehata2020coptic,
  title={Coptic Transliteration Tool},
  author={Michael Shehata},
  year={2020},
  institution={Montclair State University of New Jersey},
  url={https://github.com/shehatamichael/coptic-transliterator}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/shehatamichael/coptic-transliterator-llm/issues)
- **Email**: shehatam.dev@gmail.com
- **Contributions**: Pull requests welcome!

---

## 🙏 Acknowledgments

- Based on the original [coptic-transliterator](https://github.com/shehatamichael/coptic-transliterator) by Michael Shehata
- Powered by [Hugging Face](https://huggingface.co/) Inference API
- Hosted on [Netlify](https://netlify.com/)
- Built with [Streamlit](https://streamlit.io/)

---

<div align="center">
  <p><strong>Made with ❤️ for the Coptic community</strong></p>
</div>