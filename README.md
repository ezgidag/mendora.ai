# Mendora.AI - Personal Wellness Tracking Application

## Project Overview

Mendora.AI is a hybrid AI-powered wellness tracking web application designed to help users monitor their emotional well-being through daily journaling, automated analysis, and positive reinforcement. It combines rule-based keyword analysis with Google's Gemini Flash 2.5 API to provide personalized feedback and insights.

**Target Users:**
- Individuals seeking better emotional awareness
- People wanting to track their daily mood patterns  
- Users wanting to develop mindfulness habits
- Anyone interested in tracking their emotional patterns over time

**Problems Addressed:**
- **Negative Thought Patterns**: Helps identify recurring themes through keyword analysis.
- **Daily Stress**: Provides immediate feedback and coping strategies.
- **Lack of Self-Awareness**: Increases self-awareness through consistent tracking and reflection.
- **Personal Growth**: Offers a private, judgment-free environment for self-reflection.

## Features

Mendora.AI offers a suite of features designed to support emotional well-being:

1.  **Daily Journal Module (`pages/journal.py`)**: Allows users to write daily thoughts and feelings, which are then processed by rule-based and AI-powered analysis for instant feedback.
2.  **AI Feedback System (`utils/ai_feedback.py`)**: Integrates with Google Gemini Flash 2.5 API for advanced sentiment analysis, personalized recommendations, and emotion detection.
3.  **Daily Affirmations (`pages/affirmations.py`)**: Displays random positive affirmations daily, with a mechanism to track displayed messages to avoid repetition.
4.  **Measurements Dashboard (`pages/measurements.py`)**: Provides a visual overview of historical journal entries, analysis results, and mood trends over time.

## Technical Architecture

### Core Technologies
-   **Frontend**: Streamlit (Python-based web framework)
-   **AI Integration**: Google Gemini Flash 2.5 API (via `google-generativeai`)
-   **Database**: SQLite (for development/Streamlit Cloud temporary storage)
-   **Data Manipulation**: Pandas
-   **Charting**: Plotly Express
-   **Authentication**: Streamlit's built-in session state management
-   **Document Processing (Future/Planned)**: `pypdf`, `langchain`, `chromadb`, `sentence-transformers` (for PDF analysis, vector databases)

### Hybrid AI Approach
-   **Local Processing**: Basic keyword matching, simple categorization, data validation.
-   **Cloud Processing**: Complex emotion analysis, personalized recommendations via Gemini API.
-   **Decision Logic**: Simple categorizations handled locally; complex analysis sent to API.

## Local Setup and Running

To run Mendora.AI locally on your machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME/mendora-ai
    ```
    *(Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and repository name.)*

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Gemini API Key:**
    The application uses the Google Gemini Flash 2.5 API. You need to obtain an API key from Google AI Studio.
    *   Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
    *   Create an API key.
    *   Set this API key as an environment variable named `GEMINI_API_KEY`.
        *   **For Windows (Command Prompt):**
            ```cmd
            set GEMINI_API_KEY=YOUR_API_KEY
            ```
        *   **For Windows (PowerShell):**
            ```powershell
            $env:GEMINI_API_KEY="YOUR_API_KEY"
            ```
        *   **For macOS/Linux:**
            ```bash
            export GEMINI_API_KEY="YOUR_API_KEY"
            ```
        *(Replace `YOUR_API_KEY` with your actual Gemini API key. For permanent setup, add this to your system's environment variables or your shell's profile file (.bashrc, .zshrc, etc.).)*

5.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser (usually at `http://localhost:8501`).

## Usage

1.  **Login / Register:** Upon launching the application, you will be prompted to log in or register. If you are a new user, create an account.
2.  **Home Page:** After successful login, you will be redirected to the "Home" page. From here, you can navigate to different modules:
    *   **📝 My Journal**: Write your daily thoughts and get AI-powered insights.
    *   **✨ Affirmations**: Receive a new positive affirmation each day.
    *   **📈 My Measurements**: View your historical journal entries and analyze mood trends.

## Deployment on Streamlit Cloud

To deploy Mendora.AI on Streamlit Cloud, follow these steps:

1.  **Ensure Code is on GitHub:** Your entire `mendora-ai` project, including `requirements.txt`, must be pushed to a GitHub repository.
2.  **Go to Streamlit Cloud:** Visit [Streamlit Cloud](https://streamlit.io/cloud) and log in with your GitHub account.
3.  **Deploy a New App:**
    *   Click "New app" or "Deploy an app."
    *   Select your GitHub repository.
    *   For "Main file path," provide the direct URL to your `app.py` file on GitHub. It will look something like: `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME/blob/main/mendora-ai/app.py`
    *   In "Advanced settings" -> "Secrets," add your `GEMINI_API_KEY` as a secret. This is crucial for the AI functionality.
        *   The format should be:
            ```
            GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
            ```
    *   Click "Deploy!"

## Contribution

We welcome contributions to Mendora.AI! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file (to be created) for guidelines on how to contribute.

## License

This project is licensed under the [MIT License](LICENSE) (to be created).

## Contact

For any questions or support, please open an issue on the GitHub repository.

---

**Mendora.AI** - Empowering mental health awareness through intelligent analysis and positive reinforcement.
