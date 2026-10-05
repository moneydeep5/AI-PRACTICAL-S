# MoodLens AI — Explainable NLP Mini Project

A college-friendly mini AI application built with **Python + Flask + HTML + CSS + JavaScript**.

## What it does

- Classifies text as **Positive, Negative, or Neutral**.
- Uses a small built-in NLP dataset, so no model download or API key is needed.
- Implements an explainable Naive Bayes classifier directly in Python.
- Shows confidence values and influential words.
- Includes an ethics and responsible-AI section in the interface.

## Technologies

- Python
- Flask
- HTML5
- CSS3
- Vanilla JavaScript

No React, Node.js, database, or external AI API is required.

## How to run in VS Code

Open the `moodlens_ai` folder in VS Code.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

If PowerShell blocks script execution, open **Command Prompt** and use:

```cmd
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

`http://127.0.0.1:5000`

## Project structure

```text
moodlens_ai/
│
├── app.py
├── requirements.txt
├── README.md
├── ETHICS_AND_EXPLAINABILITY_REPORT.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## Viva explanation

**Why Naive Bayes?**
It is simple, fast, suitable for text classification, and easy to explain in a mini project.

**What is NLP here?**
The application tokenizes text, removes common stopwords, learns word frequencies from labeled examples, and uses those probabilities to classify new text.

**What makes it explainable?**
The app shows words that have the largest probability difference between classes, giving the user visible evidence for the prediction.

**Main limitation?**
The built-in dataset is very small and handcrafted. The model can fail on sarcasm, slang, long context, spelling variations, or language styles not represented in the examples.
