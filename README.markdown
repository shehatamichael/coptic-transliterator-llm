# Coptic Transliteration Tool with LLM

A web-based tool for transliterating Coptic text to Latin script, combining rule-based transliteration from [shehatamichael/coptic-transliterator](https://github.com/shehatamichael/coptic-transliterator) with Large Language Model (LLM) enhancements via the Hugging Face Inference API. Built with Streamlit and hosted on Netlify, this tool provides a user-friendly interface for English speakers to access accurate Coptic pronunciations, ideal for following church services.

## Features
- Input Coptic text via a text box or upload a `.txt` file.
- Transliterates to Latin script using rule-based logic (from `coptic-transliterator`) with optional LLM enhancement.
- Download transliterated text as a `.txt` file.
- Free to use, leveraging Hugging Face's free tier API and Netlify hosting.

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/shehatamichael/coptic-transliterator-llm.git
   cd coptic-transliterator-llm
   ```

2. **Install Dependencies**:
   - Ensure [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is installed for Pynini.
   - Create a Conda environment and install dependencies:
     ```bash
     conda create --name coptic-llm python=3.9
     conda activate coptic-llm
     conda install -c conda-forge pynini
     pip install -r requirements.txt
     ```

3. **Set Environment Variables**:
   - Get a Hugging Face API key from [Hugging Face](https://huggingface.co/settings/tokens).
   - Create a `.env` file in the project root:
     ```
     HF_API_KEY=your-api-key
     ```
   - Alternatively, set the environment variable manually:
     ```bash
     export HF_API_KEY=your-api-key
     ```

4. **Run Locally**:
   ```bash
   streamlit run app.py
   ```

## Deployment on Netlify
1. Push the repository to GitHub.
2. Connect the repository to Netlify via the Netlify dashboard.
3. Set the `HF_API_KEY` environment variable in Netlify's deployment settings (Site settings > Build & deploy > Environment variables).
4. Deploy the site (Netlify will use `netlify.toml` for configuration).
5. Access the app at the provided Netlify URL (e.g., `https://your-app-name.netlify.app`).

## Notes
- The `transliterator.py` file is sourced from [shehatamichael/coptic-transliterator](https://github.com/shehatamichael/coptic-transliterator) and provides rule-based transliteration as a fallback.
- The LLM model (Mixtral-8x7B) is used for enhanced transliteration. You can switch to a different Hugging Face model by updating `HF_API_URL` in `app.py`.
- Ensure compliance with Hugging Face's free tier limits (e.g., model size < 10GB).
- For advanced users, consider fine-tuning a smaller LLM (e.g., Mistral-7B) on Coptic-specific data for better accuracy.

## Citation
If you use this tool in your program or research, please cite:
> [Coptic Transliteration Tool](https://github.com/shehatamichael/coptic-transliterator/blob/master/Coptic%20Transliteration%20Tool.pdf), May 2020, Michael Shehata, Montclair State University of New Jersey, U.S.

## License
MIT License

## Interested in Contributing?
Please contact Michael Shehata (shehatam.dev@gmail.com)