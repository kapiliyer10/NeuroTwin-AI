# NeuroTwin AI

NeuroTwin AI is a digital cognitive twin prototype that ingests behavioral signals, estimates cognitive state, simulates likely intervention outcomes, and explains low-risk wellness recommendations.

The current implementation is a runnable first scaffold. It includes a FastAPI backend, deterministic starter state model, simulation and recommendation services, API tests, synthetic data generator, and a minimal dashboard component structure.

## Safety Notice

NeuroTwin AI is a wellness and productivity-oriented prototype. It must not present outputs as clinical assessment, diagnosis, or treatment. Any medical-adjacent or high-risk output should redirect users toward a qualified professional.

## Project Structure

```text
neurotwin-ai/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── ingest.py
│   │   ├── state.py
│   │   ├── simulate.py
│   │   └── recommend.py
│   ├── services/
│   │   ├── signal_fusion.py
│   │   ├── state_model.py
│   │   ├── state_store.py
│   │   ├── simulation_engine.py
│   │   ├── intervention_engine.py
│   │   └── explainability.py
│   ├── models/
│   │   ├── lstm_model.py
│   │   └── trainer.py
│   ├── schemas/
│   │   ├── input_schema.py
│   │   ├── state_schema.py
│   │   └── simulation_schema.py
│   ├── data/
│   │   └── generator.py
│   ├── utils/
│   │   └── safety.py
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── Graph.tsx
│   │   └── SimulationPanel.tsx
│   ├── styles.css
│   ├── package.json
│   └── tsconfig.json
├── requirements.txt
├── pyproject.toml
├── run.ps1
├── run.sh
└── README.md
```

## Backend

The backend is built with FastAPI and exposes the first demo flow:

- `POST /ingest`: accepts user signals, extracts normalized features, predicts cognitive state, and records the latest state in memory.
- `GET /state`: returns the latest cognitive state.
- `GET /state/history`: returns recent in-memory state records.
- `POST /simulate`: runs intervention simulations for the latest or supplied state.
- `GET /recommend`: recommends an intervention and returns a plain-language explanation.

### Example Signal Payload

```json
{
  "typing_speed": 52,
  "pause_variance": 1.8,
  "sentiment": -0.2,
  "screen_time": 7
}
```

## Core Modules

- `SignalFusion`: normalizes raw input signals into model-ready features.
- `StateModel`: deterministic starter model that estimates stress, fatigue, attention, and emotion.
- `SimulationEngine`: projects outcomes for `continue`, `short_break`, and `sleep`.
- `InterventionEngine`: scores simulations and selects the best intervention.
- `Explainability`: generates concise, non-clinical explanations.
- `Safety`: blocks diagnosis/treatment language in generated output.
- `CognitiveLSTM`: optional PyTorch model shell for future time-series training.

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run the API on Windows:

```powershell
.\run.ps1
```

Run the API on macOS/Linux:

```bash
./run.sh
```

Or run directly:

```bash
uvicorn backend.main:app --reload
```

Open the API docs at `http://127.0.0.1:8000/docs`.

## Testing

```bash
pytest
```

## Synthetic Data

Generate a starter CSV dataset:

```bash
python -m backend.data.generator
```

## Frontend

The frontend is a Next.js dashboard in `frontend/`. It starts with demo data and calls the FastAPI backend at `http://127.0.0.1:8000` by default.

Run it in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

To point the frontend at another backend URL:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

## Current Status

- FastAPI backend scaffold implemented.
- Signal ingestion, state estimation, simulation, recommendation, explainability, and safety modules implemented.
- API tests added for the core demo flow.
- Next.js frontend scaffold added with API-backed dashboard interactions.
- Next step: add persistence, authentication/user sessions, and a trained model pipeline.
