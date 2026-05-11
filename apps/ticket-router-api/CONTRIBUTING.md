# Contributing to Intelligent Support Assistant

First off, thanks for taking the time to contribute! 🎉

The **Intelligent Support Assistant** is a pipeline built with precision and simplicity in mind. Whether you are fixing a typo in the documentation, optimizing the TF-IDF vectorizer, or upgrading the API to support FastAPI websockets, your help is welcome.

## 🧠 Core Philosophy
- **Simplicity First:** We prefer classic ML over Deep Learning if the accuracy difference is negligible.
- **Local AI:** We lean towards local models and Apple Silicon optimization.
- **Strict Typing:** All Python code must be typed.

## 🛠 How to Contribute

### 1. Reporting Bugs
- Use the GitHub Issue Tracker.
- Describe the bug clearly. Provide steps to reproduce, what you expected to happen, and what actually happened.

### 2. Suggesting Enhancements
- Open an issue describing your idea.
- Explain **why** this enhancement would be useful to most users.

### 3. Pull Requests
1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests in the `tests/` directory.
3. Ensure the test suite passes (`pytest tests/`).
4. Update the `README.md` or documentation if your changes affect the public API or installation process.
5. Issue the pull request!

## 🧪 Development Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note:** If you are running this on Apple Silicon, ensure you have `libomp` installed (`brew install libomp`) for CatBoost/LightGBM compatibility.
