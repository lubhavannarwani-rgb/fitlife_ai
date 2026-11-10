# FitLife AI

Personalised fitness report, meal plan and workout, with an AI chat
(memory + knowledge base).

## Run locally

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```

On Mac or Linux, use `source venv/bin/activate` instead of the activate line above.

Open http://127.0.0.1:8000

Create a `.env` file in the project folder with this line:

```
GROQ_API_KEY=your_groq_api_key_here
```

The plan works without an API key. Only the AI chat needs it.

## Command-line version

```
python main.py
```

## Project layout

- `api.py`: web backend (FastAPI)
- `plan_service.py`: builds the plan and runs automatic checks
- `models.py`: user profile model
- `static/index.html`: frontend
- `fitlife_agent.py`: AI agent (tools, memory, knowledge base)
- `rag.py` and `knowledge/`: knowledge base
- `fitness_calculator.py`, `meal_planner.py`, `workout_generator.py`, `food_database.py`: core logic

## Deploy

Use Docker on Render or Railway: connect the GitHub repo, choose Docker,
and add `GROQ_API_KEY` as an environment variable.

*General guidance only, not medical advice.*