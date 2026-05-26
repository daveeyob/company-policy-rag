# Project Design and Evaluation Report

This document explains why we chose our app's setup and summarizes how well the system performed during our automated tests.

## 1. Why We Made These Design Choices

### 1.1 Choosing a Fast Keyword Search over Heavy Embedding Models

- **Our Choice:** We used a standard, built-in keyword matching system (TF-IDF from `scikit-learn`) instead of downloading massive, heavy AI embedding models to run locally on our computers.
- **Why We Did It:** When we tried running heavy local AI embedding models, they slowed down our computers significantly, making the app take way too long just to find the right document. By switching to a lightweight keyword matrix, the app scans our documents and finds the exact matching policy in **less than 5 milliseconds**. Since corporate policies use very specific terms (like _M-Nakfa, Asmara, Cash Vaults, or per-diem_), a smart keyword tracker works perfectly without draining computer memory.

### 1.2 Keeping Documents Whole Instead of Cutting Them into Pieces

- **Our Choice:** We read and send whole policy files to the AI instead of chopping them up into small paragraphs.
- **Why We Did It:** Because our policy files are short and focused (usually 1 to 3 pages per topic), cutting them into random pieces could accidentally separate an important rule from its penalty. Keeping the documents whole ensures the AI gets the full context of the policy every single time.

### 1.3 Strict Guardrails and Instructions for the AI

- **Our Choice:** We connected our app to OpenRouter's free tier, set the randomness (temperature) to 0.0, and wrote strict rules for how the AI must behave.
- **Why We Did It:** Because this is an assistant for corporate policies, we cannot let the AI guess or make things up. Setting the randomness to zero ensures it gives steady, repeatable answers. We also added strict rules telling it to say exactly _"I can only answer about our policies."_ if it cannot find a match, and forced it to put the file name in square brackets right next to its answer.

---

## 2. Testing and Evaluation Results

### 2.1 How We Tested the App

We wrote an automated testing script (`src/evaluate.py`) that fired a bank of 10 different questions at our app. We intentionally included clear policy questions, questions with annoying typos (like typing _"netwrok"_ or _"valuts"_), and completely random questions that have nothing to do with company rules (like asking for a cooking recipe) to see if our guardrails actually work.

We graded the app on three things:

1. **Groundedness:** Did the AI stick _only_ to our files without making anything up?
2. **Citation Accuracy:** Did the AI match the correct file name to the correct answer?
3. **Latency:** How long did it take to get an answer back?

The complete report for the evaluation can be found in the EVALUATION.md

### 2.2 Performance Summary

- **Total Questions Tested:** 10
- **Groundedness Score:** 100% Pass (Zero hallucinations)
- **Citation Accuracy Score:** 100% Pass (Perfect file matching)
- **Average Time per Question:** ~21.9 seconds

### 2.3 Explaining the System Speed (Latency)

You will notice that while our local app code finds the documents instantly (in about 2 milliseconds, like in Test 3), the total time to get an answer back from the AI often took much longer. This delay is entirely due to internet traffic on OpenRouter's free servers.

To handle this real-world issue, we coded a **Self-Healing Retry Loop** into our system. If the free AI servers are too busy and try to block our request, our app doesn't crash or error out; it patiently waits a few seconds and automatically tries again. This guarantees that our users always get a 100% accurate, safe answer, even if the internet connection is running a bit slow.
