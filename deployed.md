# Deployed Application Link

The live, fully functional public deployment of the Himbol Policy RAG assistant has been hosted on Render and can be accessed directly at:

👉 [Himbol Policy RAG Live Production URL](https://hcfs-policy-rag.onrender.com/)

### Deployment Architecture & Settings:

- **Hosting Cloud Platform:** Render (Free Web Service Instance)
- **Start Binding Configuration:** `streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0`
- **Secret Variables:** The production `OPENROUTER_API_KEY` is loaded securely via Render's backend environment variables dashboard, protecting it from being exposed in public repository commits.

### Critical Deployment & Performance Notes:

1. **Initial Spin-Up Delay (Cold Starts):** Because this application is hosted on Render’s Free Tier, the server automatically goes to sleep after periods of inactivity. If the link takes 1–2 minutes to open or shows a temporary session initialization notice, please allow the container a moment to fully wake up and complete its initialization boot.
2. **Response Speed (Latency):** While our local retrieval index scans and pairs documents instantly (~2ms), the final answer compilation relies on public free-tier routes through OpenRouter. During periods of heavy web traffic, API responses may stream slowly or encounter rate limits.
3. **Resilience & Fault Tolerance:** To counter these external internet delays and prevent app crashes, we engineered an **Automated Retry Loop** into the backend. If a timeout occurs, the app will safely self-heal and try the request again automatically.
