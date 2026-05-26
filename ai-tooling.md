# AI Tooling Documentation

This document describes how AI code assistants were utilized to help design, build, and troubleshoot the Himbol Financial Services Corp Policy RAG application.

## 1. AI Tools Used

- **Primary Tool:** Gemini / LLM Chat Assistant
- **Role in Project:** Co-pilot for writing Python code scripts, setting up the Streamlit UI, drafting documentation, and debugging connection errors.

## 2. What Worked Well

- **Speedy Code Generation:** The AI was incredibly helpful for quickly writing the framework for the ingestion script (`src/ingest.py`) and setting up the basic layout for our Streamlit web interface.
- **Simplifying the Math:** Instead of having to manually code how the app calculates keyword matching arrays, the AI instantly suggested using `scikit-learn`'s built-in TF-IDF vector tools. This made our local search happen in under 5 milliseconds.
- **Setting up CI/CD:** Writing GitHub Actions code (`.github/workflows/ci-test.yml`) from scratch can be tricky with formatting, but the AI drafted a working automation layout that runs flawlessly on every push.

## 3. What Didn't Work Well & How We Fixed It

- **The "Typos" Roadblock:** Early on, when we used basic word matching, the app would panic and say it couldn't find a policy if there was a simple typo (like typing "netwrok" instead of "network"). The AI helped us fix this by introducing `ngram_range=(1, 2)`, which lets the system match parts of words so typos don't break the search.
- **Handling API Rate Limits (429 Errors):** During our initial testing runs, sending multiple questions to OpenRouter's free servers caused the connection to drop because we were hitting request limits. The AI helped us design a **Self-Healing Retry Loop** with a minor pause (`time.sleep`) between questions. This fixed the problem completely, allowing our automated evaluation to pass with a perfect 100% score.
- **Too Complex at First:** Some of the initial architectural suggestions made by the AI were a bit too dense and technical. We had to guide the AI to scale back the complexity and re-write our project reports in a clear, straightforward tone that matches our level of understanding.
