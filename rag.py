from fastapi import FastAPI, Body
from openai import OpenAI
import chromadb

client = OpenAI()
chroma_client = chromadb.HttpClient(host="chroma", port=8000)
collection = chroma_client.get_or_create_collection("docs")

app = FastAPI()

# Einfacher Ingest: Text rein, wird als ein Chunk gespeichert
@app.post("/ingest")
def ingest_doc(text: str = Body(..., embed=True), doc_id: str = "doc-1"):
    # Embedding erzeugen
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[emb],
        metadatas=[{"source": doc_id}]
    )
    return {"status": "ok", "stored_tokens": len(text.split())}

# Query-Endpunkt: Frage → Embedding → semantische Suche → Antwort
@app.post("/query")
def query_rag(query: str = Body(..., embed=True)):
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=3
    )

    docs = results["documents"][0]

    # Einfach: Kontext + Frage an GPT schicken
    prompt = "Nutze NUR diesen Kontext, um die Frage zu beantworten:\n\n"
    for d in docs:
        prompt += d + "\n---\n"
    prompt += f"\nFrage: {query}"

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = completion.choices[0].message.content
    return {"answer": answer, "context_docs": docs}
