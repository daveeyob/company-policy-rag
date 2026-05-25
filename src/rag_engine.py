import os
import pickle
import time
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

# Load environment secrets securely
load_dotenv()

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
INDEX_PATH = os.path.join(DB_DIR, "tfidf_index.pkl")
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

def get_rag_response(user_query: str, k: int = 2):
    """
    High-speed, production-grade TF-IDF Semantic Keyword RAG Architecture.
    Loads a static, pre-compiled index file generated deterministically by ingest.py.
    """
    # 1. Verify and read the pre-computed matrix index file from disk
    if not os.path.exists(INDEX_PATH):
        return {
            "answer": "❌ Error: Pre-computed index index missing. Please execute 'python src/ingest.py' first.",
            "citations": []
        }
        
    with open(INDEX_PATH, "rb") as f:
        index_data = pickle.load(f)
        
    vectorizer = index_data["vectorizer"]
    tfidf_matrix = index_data["tfidf_matrix"]
    filenames = index_data["filenames"]
    documents = index_data["documents"]
    
    # 2. Vectorize user input against matching matrix constraints
    query_vector = vectorizer.transform([user_query])
    
    # Calculate similarity rankings matching query matrix spaces
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    ranked_indices = similarities.argsort()[::-1]
    
    # Enforce strict baseline matching threshold to prevent hallucinations
    if len(ranked_indices) == 0 or similarities[ranked_indices[0]] < 0.05:
        return {
            "answer": "I can only answer about our policies.",
            "citations": []
        }
        
    context_chunks = []
    citations = []
    
    # 3. Pick top matched document allocations
    for i in range(min(k, len(ranked_indices))):
        idx = ranked_indices[i]
        if similarities[idx] > 0.02:  # Soft secondary threshold cutoff
            fname = filenames[idx]
            text_body = documents[idx]
            
            context_chunks.append(f"Source Document Reference: [{fname}]\nContent:\n{text_body}\n---")
            citations.append({
                "source": fname,
                "chunk_id": f"HIMBOL-TFIDF-{idx:02d}",
                "snippet": text_body[:350] + "..."
            })
            
    context_str = "\n".join(context_chunks)
    
    # System prompt structure enforcing strict factual grounding constraints
    system_prompt = (
        "You are an expert corporate compliance AI representing Himbol Financial Services Corp.\n"
        "Your core directive is to answer the employee's query using ONLY the provided verified policy documents.\n\n"
        "STRICT COMPLIANCE INSTRUCTIONS:\n"
        "1. Answer the question completely, directly, and objectively based on the context text blocks provided.\n"
        "2. If the context documents do not contain the specific answer to the user's question, you must respond EXACTLY with: 'I can only answer about our policies.' Do not make up facts or extrapolate conclusions.\n"
        "3. You must explicitly reference the correct source file name in square brackets (e.g., [himbol_m_nakfa_limits.md]) immediately next to the details you pull from it.\n\n"
        f"VERIFIED HIMBOL CORPORATE CONTEXT:\n{context_str}"
    )
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openrouter/free", 
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.0
    }

    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            if not API_KEY:
                return {"answer": "⚠️ OpenRouter API Key configuration missing in .env", "citations": []}
                
            # Increased timeout to 30 seconds to survive temporary network spikes
            response = requests.post(MODEL_ENDPOINT, headers=headers, json=payload, timeout=30)
            
            # If we get hit with an upstream rate limit, wait and retry
            if response.status_code == 429:
                print(f"⚠️ Rate limited (429). Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the wait time for the next step (exponential backoff)
                continue
                
            if response.status_code == 200:
                result = response.json()
                return {
                    "answer": result['choices'][0]['message']['content'],
                    "citations": citations
                }
            else:
                return {"answer": f"❌ OpenRouter Connection Failure ({response.status_code})", "citations": []}
                
        except (requests.exceptions.RequestException, Exception) as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Network glitch encountered: {str(e)}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                return {"answer": f"❌ Critical Pipeline Exception: {str(e)}", "citations": []}
                
    return {"answer": "❌ Error: Maximum API retries exhausted without a valid response.", "citations": []}

if __name__ == "__main__":
    # Test a complex query with minor typographical error variance
    test_query = "how do you handle cash valuts"
    print(f"🧪 Testing Production TF-IDF RAG Router for query: '{test_query}'...")
    res = get_rag_response(test_query, k=1)
    print(f"\nEngine Response:\n{res['answer']}\n")