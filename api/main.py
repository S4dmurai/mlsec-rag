import os
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


import embedder
import qdrant

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

@app.on_event("startup")
def startup_event():
    try:
        collections = qdrant.client.get_collections().collections
        exists = any(c.name == "documents" for c in collections)
        if not exists:
          print(
              "Collection 'documents' nicht gefunden. Erstelle neue Collection..."
          )
          qdrant.new_collection("documents")
          print("Verarbeite Dokumente im Ordner /app/documents ...")
          qdrant.implement_documents("/app/documents")
          print("Dokumente erfolgreich in Qdrant indiziert!")
        else:
          print("Collection 'documents' existiert bereits.")
    except Exception as e:
        print(f"Fehler bei der Qdrant-Initialisierung: {e}")

@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/query")
def query(question: str):
    query_vector = embedder.embed_text(question).tolist()

    results = qdrant.search_documents(query_vector, limit=3)

    if not results:
        full_context = "Keine relevant Informationen in den Dokumenten gefunden."
    else:
        context_texts = [
            f"--- Dokument: {pt.payload.get('document')}, Seite {pt.payload.get('page')} ---\n{pt.payload.get('text')}"
            for pt in results
            ]
        full_context = "\n\n".join(context_texts)
    prompt = f"""You are a helpful assistant. Answer the user's question clearly and naturally, 
    incorporating any relevant information from the provided context. Clean up any 
    awkward formatting, broken characters, or raw extraction artifacts from the source text. 
    If no context is provided or found, answer the question directly using your general knowledge.
    At the end provide the names of the used Documents, aswell as the relevant page numbers.

    Context:
    {full_context}

    Question: {question}
    Response:"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
            }
        )
    if response.status_code == 200:
        answer_text = response.json().get("response", "Fehler bei der Antwortgenerierung.")
    else:
        answer_text = "Fehler bei der Kommunikation mit dem Sprachmodell."
    return {
        "answer": answer_text
        }