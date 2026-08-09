# NeuroTwin AI

NeuroTwin Recovery is a concussion-recovery support prototype that records symptom check-ins, tracks activity tolerance, compares possible next steps, and explains evidence-grounded recommendations.

The product is designed for people who have already been evaluated by a healthcare professional. It supports symptom-guided return to daily activity, school, work, and exercise. It does not diagnose concussion, provide treatment, or clear anyone for sport.

## Safety Notice

This is a hackathon prototype and is not medical advice. It cannot diagnose concussion, assess severity, prescribe medication, or provide return-to-play clearance. Red-flag inputs trigger an urgent-care message. Users should follow their healthcare professional's plan.

Evidence sources currently represented in the app:

- [Amsterdam 2022 concussion consensus statement](https://bjsm.bmj.com/content/57/11/695)
- [Living Concussion Guidelines](https://concussionsontario.org/concussion/guideline-section/return-to-activity_work_school_considerations)
- [CDC HEADS UP clinical guidance](https://www.cdc.gov/heads-up/hcp/clinical-guidance/index.html)

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

The backend is built with FastAPI and exposes the recovery flow:

- `POST /ingest`: records a symptom and activity check-in, runs safety screening, and estimates recovery state.
- `GET /state`: returns the latest recovery state and evidence references.
- `GET /state/history`: returns the recent recovery timeline.
- `DELETE /state`: deletes all local demo check-ins.
- `POST /simulate`: compares symptom-tolerated next steps.
- `GET /recommend`: returns the latest recommendation, explanation, safety status, and sources.

### Example Check-in Payload

```json
{
  "user_id": "demo-user",
  "clinician_evaluated": true,
  "recovery_stage": 2,
  "activity_type": "school",
  "activity_minutes": 30,
  "headache": 3,
  "fatigue": 4,
  "concentration_difficulty": 4,
  "symptoms_after_activity": 1
}
```

## Core Modules

- `SignalFusion`: creates transparent concussion symptom features.
- `RecoveryStateModel`: interpretable symptom burden, cognitive load, and activity tolerance model.
- `SimulationEngine`: compares gentle continuation, reduced activity, and rest/check-in options.
- `InterventionEngine`: applies red-flag overrides before selecting a next step.
- `Explainability`: produces plain-language explanations with explicit limitations.
- `evidence.py`: keeps guideline references visible in API and UI responses.
- `StateStore`: stores check-ins in a local SQLite database with deletion support.

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

The script launches Uvicorn through Python, so the standalone `uvicorn` command does not need to be on your `PATH`.

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

- Concussion-specific check-in and recovery workflow implemented.
- Red-flag escalation and professional-care messaging implemented.
- Guideline references surfaced in the application.
- SQLite persistence and delete-my-data action implemented for the prototype.
- Accessible responsive dashboard implemented with symptom trends and what-if comparisons.
- Remaining work: production authentication, encrypted deployment storage, clinical review, and validated model evaluation.
