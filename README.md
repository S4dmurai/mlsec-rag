# RAG System

[![Docker Image](https://img.shields.io/docker/v/sadmurai/mlsec-rag-rag-api-1?label=Docker%20Hub&color=blue)](https://hub.docker.com/r/sadmurai/mlsec-rag-rag-api-1)

Ein simples Docker basiertes Rag System basierend auf **FastAPI**, **Qdrant** (Vektordatenbank), **Sentence-Transformers** und **Ollama**.

## Voraussetzungen 
- **Docker Desktop** (installiert und gestartet)
- **Ollama Engine & Modell (`llama3.2`):**
	-**Option A (Lokal):** [Ollama](https://ollama.com/) auf dem Host-System installieren und vorab das Modell `llama3.2` laden.
	-**Option B (Docker):** Kein lokales Ollama erforderlich.

	Linux: OLLAMA_BASE_URL=http://ollama:11434 docker compose --profile full up -d \
	docker exec -it mlsec-rag-ollama-1 ollama pull llama3.2

	Windows: $env:OLLAMA_BASE_URL="http://ollama:11434"; docker compose --profile full up -d \
	docker exec -it mlsec-rag-ollama-1 ollama pull llama3.2

## Start

Vektordatenbank wird beim ersten Start mit PDFs in ./documents befüllt.

Beispielsweise zum Thema LLM-Sec:
https://doi.org/10.1016/j.hcc.2024.100211
https://dl.acm.org/doi/pdf/10.1145/3605764.3623985
https://arxiv.org/pdf/2307.15043
https://www.proceedings.com/content/075/075280-3508open.pdf
https://arxiv.org/pdf/2209.07858
https://proceedings.mlr.press/v202/wan23b/wan23b.pdf

Nach start des Docker Containers ist das RAG System über http://localhost:8000 erreichbar.