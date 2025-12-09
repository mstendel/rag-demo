# 🚀 Lokales RAG-System in Kubernetes  
### *Ollama · ChromaDB · FastAPI · Kubernetes · Docker*

Dieses Repository enthält eine vollständige, reproduzierbare **On-Prem KI-Architektur**, mit der ein lokales Retrieval-Augmented-Generation-System (RAG) betrieben werden kann — ohne Cloud, ohne externe APIs.

Das System kombiniert:

- **Ollama** → Lokaler LLM-Server (z. B. Llama 3)  
- **ChromaDB** → Moderne Vektordatenbank  
- **FastAPI** → RAG-Backend mit `/ingest` und `/query`  
- **Kubernetes** → Orchestrierung, Networking, Deployment  
- **Docker** → Containerisierung der Anwendung  

Diese Anleitung ist so geschrieben, dass **Auszubildende** oder **Einsteiger:innen** den kompletten Aufbau nachvollziehen können und gleichzeitig **professionelle Qualität** für erfahrene Techniker bietet.

---

# 📘 Inhaltsverzeichnis

1. [Überblick](#-überblick)
2. [Architekturdiagramm](#-architekturdiagramm)
3. [Systemkomponenten](#️-systemkomponenten)
4. [Installation & Setup](#-installation--setup)
5. [Deployments](#️-deployments)
6. [End-to-End-Tests](#-end-to-end-tests)
7. [Troubleshooting](#-troubleshooting)
8. [Weiterführende Dokumentation](#-weiterführende-dokumentation)
9. [Projekt für Auszubildende](#-projekt-für-auszubildende)

---

# 🧭 Überblick

Dieses Repository zeigt, wie man ein modernes KI-System aufbaut, das:

- **eigene Dokumente speichert**
- **semantisch durchsuchen kann**
- **Fragen mithilfe eines LLM beantwortet**
- **vollständig lokal und offline funktioniert**

RAG = Retrieval-Augmented Generation  
→ Ein LLM erzeugt Antworten **auf Basis externer Dokumente**, nicht nur aus seinem Training.

Dies ist die Architektur, wie sie heute in KI-Projekten in Unternehmen, Behörden und Forschung üblich ist.

---

# 🧠 Architekturdiagramm

             ┌──────────────────────────────┐
             │            Nutzer             │
             └───────────────┬──────────────┘
                             │  HTTP / API
                             ▼
             ┌──────────────────────────────┐
             │           FastAPI             │
             │         rag-api Backend       │
             │   /ingest     /query          │
             └───────────────┬──────────────┘
                             │ Kontextsuche
                             ▼
             ┌──────────────────────────────┐
             │           ChromaDB            │
             │     Vektordatenbank           │
             └───────────────┬──────────────┘
                             │ Embeddings / Chat
                             ▼
             ┌──────────────────────────────┐
             │             Ollama            │
             │  Lokale LLM + Embeddings      │
             └──────────────────────────────┘
---

# 🧩 Systemkomponenten

## 🔹 **Ollama – Lokaler LLM-Server**
- führt LLMs lokal aus (z. B. Llama 3, Mistral)  
- erstellt Embeddings (`/api/embeddings`)  
- generiert Antworten (`/api/chat`)  
- arbeitet vollständig **offline**  

## 🔹 **ChromaDB – Vektordatenbank**
Speichert Dokumente + Embeddings und ermöglicht:

- semantische Suche  
- Retrieval für RAG  
- effiziente Kontextfindung  

## 🔹 **FastAPI (rag-api)**
Das Backend koordiniert:

- `/ingest` → Dokument speichern  
- `/query` → Frage stellen + Kontext holen + LLM antworten lassen  

## 🔹 **Kubernetes**
Betreibt alle Komponenten zuverlässig:

- Deployments  
- Services  
- Netzwerk  
- Neustart bei Ausfällen  
- Skalierung  

## 🔹 **Docker**
Verpackt die Anwendung in portable Images für K8s.

---

# 🛠 Installation & Setup

Die komplette Setup-Anleitung findest du hier:

📄 **[`docs/K8S_SETUP.md`](docs/K8S_SETUP.md)**

Sie umfasst:

- Installation von Docker  
- Installation von Kubernetes (kubeadm)  
- Netzwerk-Konfiguration (`br_netfilter`, `ip_forward`)  
- Installation von Flannel  
- Cluster-Validierung  

---

# ☸️ Deployments

Alle Kubernetes-Manifeste liegen unter:
k8s/
├─ namespaces/
├─ ollama/
├─ chroma/
└─ rag-api/

---

### ▶ Ollama installieren

```bash
kubectl apply -f k8s/namespaces/llm-namespace.yaml
kubectl apply -f k8s/ollama/ollama-deployment.yaml
kubectl apply -f k8s/ollama/ollama-service.yaml

Dann Modelle laden:

kubectl -n llm exec -it deploy/ollama -- bash
ollama pull llama3:8b
ollama pull nomic-embed-text

ChromaDB deployen

kubectl apply -f k8s/chroma/chroma-deployment.yaml
kubectl apply -f k8s/chroma/chroma-service.yaml

RAG-API deployen

kubectl apply -f k8s/rag-api/rag-api-deployment.yaml
kubectl apply -f k8s/rag-api/rag-api-service.yaml

🔍 End-to-End Tests

kubectl -n rag-demo run curl-test --image=curlimages/curl -- sleep 3600
kubectl -n rag-demo exec -it curl-test -- sh

Dokument einfügen

curl -X POST http://rag-api:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{"text": "Dies ist ein Testdokument.", "doc_id": "test1"}'

Frage stellen

curl -X POST http://rag-api:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Worum geht es im Dokument?"}'

🛠 Troubleshooting

Siehe:

📄 docs/TROUBLESHOOTING.md￼

Typische Themen:
	•	flannel CrashLoopBackOff
	•	ollama /api/embeddings Fehler
	•	Chroma-Service nicht erreichbar
	•	JSON-Strukturfehler bei FastAPI
	•	ImagePullBackOff

⸻

📚 Weiterführende Dokumentation
	•	Architektur → docs/ARCHITECTURE.md￼
	•	Kubernetes Setup → docs/K8S_SETUP.md￼
	•	RAG Grundlagen → docs/RAG_CONCEPTS.md￼
	•	Troubleshooting → docs/TROUBLESHOOTING.md￼
	•	Übungen → training/EXERCISES.md￼
	•	Kompetenz-Check → training/CHECKLIST.md￼
	•	Projektaufgabe → training/PROJECT_TASK.md