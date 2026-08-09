# NeuroTwin AI

NeuroTwin AI is planned as a digital cognitive twin system that ingests behavioral and contextual signals, estimates cognitive state, simulates possible interventions, and explains recommendations through a modular AI backend and dashboard.

This repository currently contains the project baseline and implementation plan. The first production scaffold will be built from the included architecture described below.

## Vision

NeuroTwin AI is designed to help model short-term mental state patterns such as stress, fatigue, attention, and emotional load from user signals. The system is intended for wellness-oriented recommendations and simulation, not medical diagnosis.

Core goals:

- Ingest time-series user signals such as typing speed, pause variance, sentiment, and screen time.
- Fuse raw signals into model-ready features.
- Predict cognitive state with a modular ML wrapper, initially backed by a dummy model or LSTM.
- Simulate outcomes for actions such as continuing work, taking a break, or sleeping.
- Recommend a low-risk intervention based on simulated outcomes.
- Explain state and recommendations in plain language with safety guardrails.
- Present the state, trends, simulations, and recommendation in a simple frontend dashboard.

## Planned Architecture

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
│   │   ├── generator.py
│   │   └── dataset.csv
│   ├── utils/
│   │   └── safety.py
│   └── tests/
│       └── test_api.py
├── frontend/
│   ├── pages/
│   │   └── index.tsx
│   └── components/
│       ├── Dashboard.tsx
│       ├── Graph.tsx
│       └── SimulationPanel.tsx
├── requirements.txt
├── README.md
└── run.sh
```

## Backend Plan

The backend will use FastAPI with separated routers for ingestion, state lookup, simulation, and recommendations.

Planned endpoints:

- `POST /ingest`: accepts user signal input, extracts features, predicts the current cognitive state, and returns state metrics.
- `GET /state`: returns the latest estimated cognitive state.
- `POST /simulate`: runs intervention simulations against a provided or latest state.
- `GET /recommend`: returns the recommended intervention and explanation.

## Core Modules

- `SignalFusion`: converts raw input signals into numeric model features.
- `StateModel`: wraps cognitive-state prediction and hides model-loading details from API routes.
- `CognitiveLSTM`: planned PyTorch LSTM for time-series prediction.
- `SimulationEngine`: estimates how candidate actions may affect stress or related state values.
- `InterventionEngine`: selects the best intervention from simulation results.
- `Explainability`: generates user-facing explanations for state and recommendations.
- `Safety`: prevents medical-diagnosis language and redirects high-risk output toward professional guidance.

## Frontend Plan

The frontend will provide a minimal dashboard showing:

- Current stress or cognitive-state indicators.
- Historical trend graph.
- Simulation results by action.
- Recommended intervention.
- Plain-language explanation.

## Intended Local Run Flow

Once scaffolded, the expected local backend workflow will be:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Expected demo flow:

1. Send signal input to `/ingest`.
2. Receive estimated cognitive state.
3. Run `/simulate` against that state.
4. Fetch `/recommend`.
5. Display the explanation and recommendation in the dashboard.

## Safety Notice

NeuroTwin AI is a wellness and productivity-oriented prototype. It must not present outputs as clinical assessment, diagnosis, or treatment. Any high-risk or medical-adjacent output should be guarded with a recommendation to consult a qualified professional.

## Current Status

- Repository initialized.
- Project specification reviewed.
- README baseline created from the implementation document.
- Full application scaffold is the next implementation step.
