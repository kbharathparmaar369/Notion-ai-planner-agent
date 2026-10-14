# Notion AI Planner Agent

A ReAct-style AI agent that plans your day using your real Notion tasks and live weather data. Built with FastAPI, LangChain, Groq, and Streamlit.

## What it does

Ask it things like "plan my day" or "what tasks do I have," and it reasons step by step: 
checking your Notion tasks, checking the weather, and building a plan around both. 
It can also create tasks and update task statuses in Notion, but always asks for 
confirmation before making any changes.

## Architecture

User → Streamlit chat UI → FastAPI `/chat` endpoint → LangChain agent (powered by Groq) 
→ tools (Notion API, Open-Meteo API) → agent reasons over results → final plan returned to user.

## Tech stack

- FastAPI (backend API)
- LangChain + Groq (the reasoning agent)
- Streamlit (chat frontend)
- Notion API (tasks)
- Open-Meteo API (weather)
- Docker + docker-compose
- GitHub Actions (CI)

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your keys:
   - `GROQ_API_KEY` — from [console.groq.com](https://console.groq.com)
   - `NOTION_API_KEY` — from your Notion integration
   - `NOTION_DATABASE_ID` — the database you want the agent to manage
3. Your Notion database needs these properties: `Name` (title), `Status` (status), `Due Date` (date)

## Running locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Terminal 1:
```bash
uvicorn app.main:app --reload
```

Terminal 2:
```bash
streamlit run frontend/app.py
```

## Running with Docker

```bash
docker compose up --build
```

Then open `http://localhost:8501`.

## Example prompts

- "What tasks do I have?"
- "Plan my day, I'm in [your city]"
- "Create a task called 'call the dentist' for tomorrow"
- "Mark [task] as done"

## Notes

- The agent always asks for confirmation before creating or updating anything in Notion.
- Conversation memory is kept per session, in memory, it resets if the server restarts.
