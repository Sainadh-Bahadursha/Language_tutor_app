# Language Tutor App

An interactive web-based language learning tool powered by **Streamlit** and **OpenAI GPT-4o mini**. The app helps students improve their language skills through visual comprehension, grammar exercises, and translation practice.

## Features

### 1. **Image Comprehension**
- Displays a random image.
- Student describes the image.
- GPT-4o mini provides detailed feedback on grammar, vocabulary, and clarity.

### 2. **Grammar Practice**
- Offers two types of questions:
  - Fill-in-the-blank
  - Multiple Choice Questions (MCQs)
- Students input their answers.
- GPT-4o evaluates responses, gives correct answers, and constructive feedback.

### 3. **Reading & Translation**
- Presents prompts in a random language (English, French, Spanish, etc.).
- Students are asked to translate them into English.
- GPT-4o validates the translation and offers corrections with explanations.

## Tech Stack

- **Streamlit** – UI for interactive web app
- **OpenAI GPT-4o mini** – Core LLM for language understanding and feedback
- **Wave** – Audio/voice integration (if applicable)

## Folder Structure

```
language-tutor-app/
├── app.py                      # Main app launcher
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── pages/
    ├── home.py                 # Welcome/Landing page
    ├── image_comprehension.py # Image description module
    ├── grammar_fun.py         # Grammar quiz module
    └── reading_translation.py # Translation module
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/language-tutor-app.git
   cd language-tutor-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key**
   - Create a `.streamlit/secrets.toml` file (or set it via environment variable)
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
