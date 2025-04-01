import os
import faiss
import pickle
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and effective

def load_pdfs_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, filename))
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            documents.append((filename, text))
    return documents

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def build_vector_index(documents):
    chunks, metadata = [], []
    for filename, doc_text in documents:
        for chunk in chunk_text(doc_text):
            chunks.append(chunk)
            metadata.append(filename)

    embeddings = model.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and metadata
    with open("rag_index.pkl", "wb") as f:
        pickle.dump((index, chunks, metadata), f)

def load_index():
    with open("rag_index.pkl", "rb") as f:
        return pickle.load(f)

def search_similar_chunks(query, top_k=3):
    index, chunks, metadata = load_index()
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0]]

def load_texts_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append((filename, text))
    return documents
