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

## 🏗️ System Architecture

┌───────────────────────────────────────────────────────────────┐
│ User Interface Layer │
└───────────────────────────────────────────────────────────────┘
│ │ │
▼ ▼ ▼
┌───────────────────────────────────────────────────────────────┐
│ Agent Orchestration Layer │
│ ┌──────────────────┐ ┌────────────────┐ ┌───────────────┐│
│ │ Research Director│ │Patent Retriever│ │Data Analyst ││
│ └──────────────────┘ └────────────────┘ └───────────────┘│
│ │
│ ┌──────────────────┐ │
│ │Innovation │ │
│ │Forecaster │ │
│ └──────────────────┘ │
└───────────────────────────────────────────────────────────────┘
│ │ │
▼ ▼ ▼
┌───────────────────────────────────────────────────────────────┐
│ Knowledge Processing Layer │
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
│ │ Semantic │ │ Hybrid │ │ Iterative │ │
│ │ Search │ │ Search │ │ Search │ │
│ └───────────────┘ └───────────────┘ └───────────────┘ │
└───────────────────────────────────────────────────────────────┘
│ │ │
▼ ▼ ▼
┌───────────────────────────────────────────────────────────────┐
│ Data Storage Layer │
│ ┌───────────────────────────────────────────────────────────┐│
│ │ OpenSearch ││
│ └───────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────┘

---

## 🪜 Step-by-Step Development Journey

This section details exactly **how I built the system**, step by step — including setup, debugging, and fixes for the problems I encountered.

---


---

## 🧠 Agents & Their Roles

| Agent | Role | Description |
|-------|------|--------------|
| **Research Director** | Planner | Determines focus areas and coordinates other agents. |
| **Patent Retriever** | Data Collector | Retrieves relevant patents from OpenSearch. |
| **Data Analyst** | Processor | Analyzes patents for trends, keywords, and citations. |
| **Innovation Forecaster** | Predictor | Predicts potential innovation areas using LLM reasoning. |

---

## 🛠️ Prerequisites

Before running the system, make sure you have the following installed:

- **Python 3.10+**
- **Docker** (for Ollama and OpenSearch)
- **VS Code** (recommended)
- **OpenSearch instance** (default: `localhost:9200`)
- **Ollama** (for local LLM models)
- Patent data (to be pre-loaded into OpenSearch)

---

## ⚙️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/patent-innovation-analyzer.git
cd patent-innovation-analyzer

### Step 2: Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate       # For Linux/Mac
# OR
.venv\Scripts\activate          # For Windows

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Start Ollama (via Docker)
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

Step 5: Pull Required Models
docker exec -it ollama ollama run deepseek-r1:1.5b
docker exec -it ollama ollama run nomic-embed-text

Step 6: Run OpenSearch
docker compose -f docker-compose.yml up

Step 7: Verify Services

OpenSearch: http://localhost:9200

Ollama: http://localhost:11434

If both respond, you’re good to go!

⚙️ Configuration

You can configure your environment using a .env file:

# Optional API keys or configuration
SERPAPI_API_KEY=your_api_key_here


The system will automatically create required indices in OpenSearch if they don’t exist.

▶️ Usage

To start the system:

python agentic_rag.py


You’ll see the agents begin communicating and performing tasks in sequence:

Research Director assigns topics

Patent Retriever fetches relevant data

Data Analyst summarizes and clusters insights

Innovation Forecaster predicts upcoming trends

💡 Step-by-Step: How I Built This Project

Concept Design

Wanted to explore how AI agents can automate research tasks like patent mining.

Started with a lithium battery case study, later expanded to all patents.

Environment Setup

Faced issues running Docker and VS Code together due to RAM usage (Docker engine consumed ~3–4GB).

Solved by limiting Docker memory allocation and closing heavy VS Code extensions.

Ollama Setup

Encountered port conflicts with previous containers.

Fixed by stopping all previous instances and cleaning Docker volumes.

OpenSearch Integration

Learned to configure indices manually using the REST API.

Created a script to auto-create indices if missing.

Agent Logic

Implemented agents step-by-step:

First tested a single retrieval agent.

Then added orchestration with async coordination.

Finally added forecasting logic.

Testing & Debugging

Faced multiple issues with async I/O blocking and memory overflow while embedding large patent texts.

Solved by batching data and caching intermediate steps.

Final Integration

Connected everything: Ollama (for LLM reasoning), OpenSearch (for semantic search), and Python orchestrator.

🧠 Lessons Learned

Managing Docker containers and VS Code simultaneously requires good system memory (8GB+ recommended).

Ollama’s local model hosting is powerful but memory-heavy.

Understanding how RAG + multi-agent orchestration works helped me understand advanced AI pipelines.

Debugging async logic in Python was one of the hardest but most valuable parts of this project.

🧩 Future Improvements

Add web-based UI (React + FastAPI backend)

Enhance data visualization with graphs of patent trends

Add automatic data ingestion from open patent APIs

Integrate more powerful LLMs (like Mistral or Llama 3)


