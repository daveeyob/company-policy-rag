import os
import glob
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

def run_ingestion():
    print("🚀 Initializing Production Ingestion Engine for Himbol Financial Services Corp...")
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
    os.makedirs(db_dir, exist_ok=True)
    
    # 1. Gather all files deterministically
    file_paths = sorted(glob.glob(os.path.join(data_dir, "*.md")))
    if not file_paths:
        print(f"⚠️ Error: No policy files found in: {data_dir}")
        return
        
    print(f"📂 Found {len(file_paths)} policy files. Indexing text structures...")
    
    documents = []
    filenames = []
    
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            documents.append(f.read())
            filenames.append(os.path.basename(path))
            
    # 2. Build the TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # 3. Save the index deterministically to disk so the RAG engine can load it
    payload = {
        "vectorizer": vectorizer,
        "tfidf_matrix": tfidf_matrix,
        "filenames": filenames,
        "documents": documents
    }
    
    index_path = os.path.join(db_dir, "tfidf_index.pkl")
    with open(index_path, "wb") as f:
        pickle.dump(payload, f)
        
    print(f"✨ Ingestion complete! Saved deterministic matrix index to {index_path}")

if __name__ == "__main__":
    run_ingestion()