# Deployed Application Link

The live, fully functional public deployment of the Himbol Policy RAG assistant has been hosted on Render and can be accessed directly at:

👉 [Himbol Policy RAG Live Production URL](https://company-policy-rag-kqxc.onrender.com/)

### Deployment Architecture & Settings:

- **Hosting Cloud Platform:** Render (Free Web Service Instance)
- **Start Binding Configuration:** `streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0`
- **Secret Variables:** The production `OPENROUTER_API_KEY` is loaded securely via Render's backend environment variables dashboard, protecting it from being exposed in public repository commits.
