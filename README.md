# AI_chatbot (LangGraph)

This folder contains a small chatbot based on LangGraph and a Streamlit frontend.

What's included
- `langgraph_backend.py` — backend composition and `chatbot` object
- `streamlit_frontend.py` — Streamlit UI that uses the backend
- `Dockerfile`, `requirements.txt`, `.gitignore` — for containerized deployment
- `agentop/agentop-deploy.yaml` — AgentOp deployment template (fill in values)
- `scripts/deploy_agentop.sh` — helper deploy script (template)

Quick local run

1. Create a virtualenv and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the Streamlit frontend

```bash
streamlit run streamlit_frontend.py
```

Docker (build & run)

```bash
docker build -t yourname/langgraph-chatbot:latest .
docker run -p 8501:8501 yourname/langgraph-chatbot:latest
```

CI / Deployment

- A GitHub Actions workflow is added to the repository root to run a quick smoke check and build/push Docker images to GitHub Container Registry.
- The `agentop/agentop-deploy.yaml` file is a template you can adapt for AgentOp; it expects a container image reference and environment variables.

Next steps / notes

- Replace placeholder package names in `requirements.txt` ith exact package names if you use private packages (e.g., `langgraph`).
- Add your secrets (OpenAI key, GHCR credentials, AgentOp token) to GitHub Secrets when enabling CI or deploy workflows.

- 
- <img width="1917" height="956" alt="AI_chatbot" src="https://github.com/user-attachments/assets/acaa6a1e-682a-469d-9795-c6cf2ebf3e46" />



