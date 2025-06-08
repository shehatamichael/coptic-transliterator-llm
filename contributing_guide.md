# Contributing to Enhanced Coptic Transliterator 🤝

Thank you for your interest in contributing! This project serves the Coptic Orthodox community and we welcome contributions from linguists, developers, and community members.

## 🎯 Ways to Contribute

### 1. **Linguistic Improvements**
- Improve transliteration rules and mappings
- Add contextual patterns for better accuracy
- Test with liturgical texts and provide feedback
- Document pronunciation guidelines

### 2. **Technical Development**
- Code improvements and optimizations
- Bug fixes and error handling
- New features and enhancements
- Performance improvements

### 3. **Documentation & Testing**
- Improve documentation and examples
- Create test cases with various Coptic texts
- Write tutorials and usage guides
- Translate documentation to other languages

### 4. **Community Support**
- Help users with issues and questions
- Share usage examples and success stories
- Spread awareness in Orthodox communities

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/shehatamichael/coptic-transliterator-llm.git
   cd coptic-transliterator-llm
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Verify Setup**
   ```bash
   python coptic_llm_transliterator.py --help
   ```

### Optional: AI Enhancement Setup

1. **Install Ollama**
   - Visit [ollama.ai](https://ollama.ai/) and install for your system

2. **Pull Model**
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Test AI Features**
   ```bash
   echo "ⲡⲉⲛⲛⲟⲩϯ" > test.txt
   python coptic_transliterator.py test.txt --method hybrid -v
   ```

## 📝 Development Guidelines

### Code Style

We use Python standards with these tools:

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pre-commit**: Automated checks

```bash
# Format code
black coptic_transliterator.py

# Check linting
flake8 coptic_transliterator.py

# Type checking
mypy coptic_transliterator.py
```

### Code Structure

```python
# Follow this general structure for new features
class NewFeature:
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def process(self, text: str) -> str:
        """Clear docstring explaining the method"""
        try:
            # Implementation
            return result
        except Exception as e:
            self.logger.error(f"Error in NewFeature: {e}")
            raise
```

### Linguistic Guidelines

When improving transliteration rules:

1. **Orthodox Pronunciation**: Follow modern Coptic Orthodox pronunciation
2. **Consistency**: Maintain consistent mappings across the codebase
3. **Context Awareness**: Consider surrounding characters and word patterns
4. **Documentation**: Document the linguistic reasoning for changes

```python
# Example of good rule documentation
'ⲃ': 'v',  # Veeta - modern Orthodox pronunciation (not classical 'b')
```

## 🧪 Testing

### Manual Testing

```bash
# Test with various methods
echo "ⲡⲉⲛⲛⲟⲩϯ ⲓⲏⲥⲟⲩⲥ ⲡⲉⲭⲣⲓⲥⲧⲟⲥ" > liturgy.txt

python coptic_transliterator.py liturgy.txt --method rule_based
python coptic_transliterator.py liturgy.txt --method hybrid  # If Ollama available
```

### Adding Test Cases

Create test files in the `tests/` directory:

```python
# tests/test_transliteration.py
def test_basic_words():
    transliterator = CopticTransliterator(config)
    assert transliterator.transliterate("ⲡⲉⲛⲛⲟⲩϯ") == "pennouti"
```

### Test Data

When adding test cases:
- Use public domain liturgical texts
- Include both simple and complex examples
- Test edge cases and special characters
- Provide expected outputs with reasoning

## 📋 Submission Process

### 1. **Issue First** (for major changes)
   - Open an issue to discuss your proposed changes
   - Get feedback before investing significant time
   - Reference the issue in your pull request

### 2. **Branch Naming**
   ```bash
   git checkout -b feature/improved-liturgical-rules
   git checkout -b fix/unicode-encoding-issue
   git checkout -b docs/usage-examples
   ```

### 3. **Commit Messages**
   Use clear, descriptive commit messages:
   ```bash
   git commit -m "feat: add contextual patterns for common liturgical phrases"
   git commit -m "fix: handle Unicode normalization in file reading"
   git commit -m "docs: add Docker usage examples"
   ```

### 4. **Pull Request**
   - Fill out the PR template completely
   - Include test results and screenshots if applicable
   - Reference any related issues
   - Ensure CI passes

## 🔍 Pull Request Checklist

- [ ] Code follows style guidelines (black, flake8, mypy pass)
- [ ] All tests pass locally
- [ ] New features include appropriate tests
- [ ] Documentation is updated if needed
- [ ] Linguistic changes are documented and justified
- [ ] No breaking changes without discussion
- [ ] Commit messages are clear and descriptive

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Ollama version (if using AI features)

2. **Steps to Reproduce**
   - Exact commands used
   - Input text that caused the issue
   - Expected vs. actual behavior

3. **Error Messages**
   - Full error output
   - Log files if available

4. **Sample Data**
   - Minimal example that demonstrates the bug
   - Input and expected output

## 💡 Feature Requests

For new features, please provide:

1. **Use Case**: Why is this feature needed?
2. **Linguistic Rationale**: How does it improve transliteration?
3. **Implementation Ideas**: Suggestions for how to implement
4. **Community Impact**: Who would benefit from this feature?

## 🌍 Linguistic Contributions

### Areas Needing Expertise

- **Dialectical Variations**: Bohairic vs. Sahidic transliteration
- **Liturgical Context**: Church-specific pronunciation rules
- **Historical Accuracy**: Evolution of Coptic pronunciation
- **Educational Materials**: Learning-focused transliteration

### Linguistic Review Process

1. Linguistic changes are reviewed by community members with expertise
2. Changes are tested with liturgical texts
3. Documentation must explain the linguistic reasoning
4. Community feedback is gathered before merging

## 🏆 Recognition

Contributors are recognized in:
- GitHub contributors list
- Release notes for significant contributions
- README acknowledgments
- Special recognition for linguistic expertise

## 📞 Getting Help

- **GitHub Discussions**: For questions and ideas
- **GitHub Issues**: For bugs and feature requests
- **Email**: project-maintainer@example.com
- **Community**: Orthodox computing communities

## 🙏 Code of Conduct

This project serves a religious community. Please:

- Be respectful and constructive in all interactions
- Focus on technical and linguistic merit
- Welcome newcomers and help them contribute
- Maintain the free and open nature of the project
- Respect the Orthodox Christian context of the work

---

Thank you for contributing to this important tool for the Coptic Orthodox community! 🙏