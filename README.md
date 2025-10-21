# 🧠 Patent Innovation Analysis System (Multi-Agent Architecture)

This project analyzes **patent data** to identify **technological trends** and **predict future innovations** across different industries.  
It uses a **multi-agent system** where each agent plays a specialized role in data retrieval, analysis, and forecasting.  
The system leverages **LLMs (via Ollama)**, **OpenSearch** for vector search, and **Python** for orchestration.

---

## 🚀 Project Overview

This system was built as part of my **learning journey** into AI agents, RAG (Retrieval-Augmented Generation), and data-driven innovation analysis.  
It started as an experiment to explore how AI can process **patent databases** and generate **innovation insights** — such as predicting upcoming tech trends.

---

## 🧩 System Architecture


---

# Patent Innovation Predictor

An agentic RAG (Retrieval-Augmented Generation) system that analyzes patent data to predict emerging innovations and technological trends using multi-agent orchestration, semantic search, and local LLMs.

## System Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                     User Interface Layer                      │
└───────────────────────────────────────────────────────────────┘
                │                │                │
                ▼                ▼                ▼
┌───────────────────────────────────────────────────────────────┐
│                 Agent Orchestration Layer                     │
│  ┌──────────────────┐   ┌────────────────┐  ┌───────────────┐│
│  │ Research Director│   │Patent Retriever│  │Data Analyst   ││
│  └──────────────────┘   └────────────────┘  └───────────────┘│
│                                                               │
│  ┌──────────────────┐                                         │
│  │Innovation        │                                         │
│  │Forecaster        │                                         │
│  └──────────────────┘                                         │
└───────────────────────────────────────────────────────────────┘
                │                │                │
                ▼                ▼                ▼
┌───────────────────────────────────────────────────────────────┐
│                Knowledge Processing Layer                     │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐ │
│  │ Semantic      │    │ Hybrid        │    │ Iterative     │ │
│  │ Search        │    │ Search        │    │ Search        │ │
│  └───────────────┘    └───────────────┘    └───────────────┘ │
└───────────────────────────────────────────────────────────────┘
                │                │                │
                ▼                ▼                ▼
┌───────────────────────────────────────────────────────────────┐
│                     Data Storage Layer                        │
│  ┌───────────────────────────────────────────────────────────┐│
│  │                       OpenSearch                          ││
│  └───────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────┘
```

## Features

- **Multi-Agent System**: Coordinated agents (Research Director, Patent Retriever, Data Analyst, Innovation Forecaster) work together to analyze patent data
- **Hybrid Search**: Combines semantic search (embeddings) with keyword filtering for optimal retrieval
- **Local LLM Integration**: Uses Ollama for running models locally (DeepSeek, Nomic-Embed)
- **Patent Analysis**: Clustering, summarization, and trend detection from patent datasets
- **Innovation Forecasting**: Predicts emerging technologies with confidence scores

## Prerequisites

- **Python 3.10+**
- **Docker** (Docker Desktop recommended)
- **Docker Compose**
- **Ollama** (via Docker container)
- **OpenSearch** instance running (default: localhost:9200)
- Access to patent data (pre-loaded in OpenSearch or available for ingestion)
- **Recommended**: 8GB+ RAM (16GB recommended for comfortable local model + OpenSearch operation)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/patent-innovation-predictor.git
cd patent-innovation-predictor
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama as a Docker Container

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 5. Pull required models

```bash
docker exec -it ollama ollama run deepseek-r1:1.5b
docker exec -it ollama ollama run nomic-embed-text   # For embeddings
```

### 6. Start OpenSearch

```bash
docker compose -f docker-compose.yml up -d
```

Make sure your OpenSearch instance is running on `localhost:9200` (or update the connection settings in the code).

## Configuration

Create a `.env` file in the project root or set environment variables:

```env
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_INDEX=patents
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=deepseek-r1:1.5b
BATCH_SIZE=16
```

Adjust `BATCH_SIZE` to control memory and throughput when creating embeddings.

## Data Ingestion

### Example OpenSearch Mapping

```json
PUT /patents
{
  "mappings": {
    "properties": {
      "patent_id": { "type": "keyword" },
      "title": { "type": "text" },
      "abstract": { "type": "text" },
      "claims": { "type": "text" },
      "publication_date": { "type": "date" },
      "assignee": { "type": "keyword" },
      "cpc": { "type": "keyword" },
      "embedding": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```

### Batch Indexing (Python)

```python
from utils.opensearch_client import get_client
client = get_client()

def index_batch(docs):
    actions = []
    for d in docs:
        actions.append({"index": {"_index": "patents", "_id": d['patent_id']}})
        actions.append(d)
    client.bulk(body=actions)
```

### Embedding Pipeline

1. Generate embeddings in batches (size controlled by `BATCH_SIZE`)
2. Attach embedding field and index documents into OpenSearch

## Agent Architecture

### Message Schema

JSON-based message format for agent-to-agent communication:

```json
{
  "id": "msg-001",
  "from": "ResearchDirector",
  "to": "PatentRetriever",
  "instructions": "Find patents related to 'battery thermal management' in last 5 years with high citation.",
  "payload": { "query": "battery thermal management", "years": 5 }
}
```

### Agent Roles

#### ResearchDirector
- Accepts user topic or prompt
- Expands to keywords + seed queries (uses LLM to expand synonyms and related topics)
- Sends structured instructions to PatentRetriever

#### PatentRetriever
- Executes hybrid search:
  - Keyword filter (CPC, assignee, dates)
  - Semantic search using embeddings + dot-product similarity
- Returns top-K documents and metadata

#### DataAnalyst
- Abstract summarization (LLM)
- Keyword extraction (TF-IDF + LLM)
- Clustering (k-means on embeddings or agglomerative)
- Citation-network features (if citation graph available)
- Stores results in local cache & index for speed

#### InnovationForecaster
- Consumes cluster summaries and trend features
- Prompts LLM to reason and list 5–10 likely near-term innovations
- Provides confidence scores and suggested research directions

## Usage

### Start Services

1. Start OpenSearch and Ollama
2. Index your patent dataset (see ingestion above)

### Run the Orchestrator

```bash
python agentic_rag.py --topic "battery thermal management" --years 5
```

### Sample Output

```
[ResearchDirector] Seed queries created: ["battery thermal runaway", "thermal management cells", ...]
[PatentRetriever] Found 128 candidate patents (top-K 40)
[DataAnalyst] Clustered into 6 clusters: cluster labels [0..5]
[InnovationForecaster] Predictions:
  - Hybrid passive-active cooling for pouch cells (confidence 0.78)
  - Modular thermal sensors + faster local balancing (confidence 0.72)
```

## Testing & Debugging

### Testing Tips

- Unit test agents in isolation
- Mock OpenSearch responses for PatentRetriever
- Use a small dataset (100 patents) while developing
- Log everything: message flows, LLM requests/responses, timing
- Cache LLM outputs on disk (`./cache/`) to avoid repeated cost

### Test Ollama Endpoint

```bash
curl -X POST http://localhost:11434/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"deepseek-r1:1.5b",
    "input":"Summarize: Lithium cell thermal management techniques in two lines."
  }'
```

## Troubleshooting

### 1. Docker + VS Code + Ollama System Freeze

**Symptom**: Laptop becomes unresponsive when starting Ollama and VS Code.

**Fix**:
- Increase Docker Desktop memory (Settings → Resources → Memory) to 4-8 GB
- Close unused VS Code windows and disable heavy extensions
- Start services sequentially (OpenSearch first, then Ollama)

```bash
docker ps -a
docker stop <container_id>
docker rm <container_id>
docker system prune -f
```

### 2. Ollama Volume/Permission Errors

**Symptom**: Container fails with mount errors.

**Fix**:
```bash
docker volume rm ollama
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama
```

On Windows, ensure Docker has drive permission (Docker Desktop → Resources → File Sharing).

### 3. OpenSearch Out-of-Memory

**Symptom**: OpenSearch crashes during bulk indexing.

**Fixes**:
- Reduce bulk batch size to 50 docs per request
- Set JVM options in `docker-compose.yml`:

```yaml
environment:
  - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx1g
```

- Use ingestion script with `yield` and sleep between batches

### 4. LLM Output Parsing Issues

**Symptom**: LLM returns free-form text instead of JSON.

**Fix**:
- Use strong system instructions: "OUTPUT MUST BE JSON"
- Add fallback parser to retry with format correction
- Example instruction:

```
You are an assistant. Output MUST be a single valid JSON object with keys: 
predictions (list), confidences (list), rationale (string).
```

### 5. Async Blocking and Timeouts

**Symptom**: Orchestrator blocks on LLM calls.

**Fix**:
```python
import asyncio
await asyncio.wait_for(run_llm_call(...), timeout=30)
```

Use `asyncio.get_running_loop().run_in_executor()` for blocking I/O.

### 6. VS Code Wrong Python Interpreter

**Symptom**: Import errors due to global Python instead of `.venv`.

**Fix**: `Ctrl+Shift+P` → Python: Select Interpreter → choose `.venv`

## Performance Tuning

- **Batch embeddings**: Use `BATCH_SIZE=8/16` on low-memory machines; increase to 64+ on servers
- **Cache embeddings**: Store on disk to avoid recomputation
- **Index optimization**: Only required fields in OpenSearch; compress long texts
- **Distributed inference**: Run heavy LLM inference on separate machine
- **Monitoring**: Use `docker stats` and OpenSearch logs

## Future Roadmap

- [ ] Web UI (Streamlit / Next.js) for cluster visualization and forecasts
- [ ] Evaluation & backtesting on historical patent data
- [ ] Cloud-hosted LLM integration option
- [ ] Automated patent ingestion from USPTO/WIPO APIs
- [ ] Multi-lingual support for non-English patents

## Quick Commands Summary

```bash
# Clone
git clone https://github.com/yourusername/patent-innovation-predictor.git
cd patent-innovation-predictor

# Environment
python -m venv .venv
source .venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama run deepseek-r1:1.5b
docker exec -it ollama ollama run nomic-embed-text

# OpenSearch
docker compose -f docker-compose.yml up -d

# Run
python agentic_rag.py --topic "battery thermal management" --years 5
```

## License

MIT License - Free to use and modify for learning/research.

## Author

**Subham Mohapatra**

---

**Note**: Update the repository URL and add any additional configuration files (`requirements.txt`, `docker-compose.yml`) to your GitHub repository.
