from fastapi import APIRouter

from backend.schemas.input_schema import InputSchema
from backend.schemas.state_schema import StateResponse
from backend.services.signal_fusion import SignalFusion
from backend.services.state_model import StateModel
from backend.services.state_store import state_store

router = APIRouter(tags=["ingest"])


@router.post("/ingest", response_model=StateResponse)
def ingest_data(data: InputSchema) -> StateResponse:
    features = SignalFusion().extract(data)
    state = StateModel().predict(features)
    state_store.record(input_data=data, state=state, features=features)
    return StateResponse(state=state, message="Signals ingested and cognitive state estimated.")
