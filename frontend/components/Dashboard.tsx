"use client";

import { useEffect, useMemo, useState } from "react";

import Graph from "./Graph";
import SimulationPanel from "./SimulationPanel";

type CognitiveState = {
  stress: number;
  fatigue: number;
  attention: number;
  emotion: number;
};

type SimulationOutcome = CognitiveState & {
  summary: string;
};

type HistoryRecord = {
  timestamp: string;
  state: CognitiveState;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const demoState = {
  stress: 0.58,
  fatigue: 0.54,
  attention: 0.62,
  emotion: 0.57,
};

const demoTrend = [
  { label: "09:00", stress: 0.38, fatigue: 0.28, attention: 0.78 },
  { label: "10:00", stress: 0.44, fatigue: 0.34, attention: 0.72 },
  { label: "11:00", stress: 0.51, fatigue: 0.46, attention: 0.66 },
  { label: "Now", stress: demoState.stress, fatigue: demoState.fatigue, attention: demoState.attention },
];

const demoSimulations: Record<string, SimulationOutcome> = {
  continue: {
    stress: 0.73,
    fatigue: 0.66,
    attention: 0.54,
    emotion: 0.53,
    summary: "Continuing may preserve momentum but is likely to increase stress and fatigue.",
  },
  short_break: {
    stress: 0.4,
    fatigue: 0.46,
    attention: 0.76,
    emotion: 0.65,
    summary: "A short break is projected to reduce stress while improving attention.",
  },
  sleep: {
    stress: 0.23,
    fatigue: 0.12,
    attention: 0.9,
    emotion: 0.69,
    summary: "Sleep is projected to produce the strongest recovery when fatigue is elevated.",
  },
};

const demoRecommendation = "short_break";

export default function Dashboard() {
  const [state, setState] = useState<CognitiveState>(demoState);
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [simulations, setSimulations] = useState<Record<string, SimulationOutcome>>(demoSimulations);
  const [recommendation, setRecommendation] = useState(demoRecommendation);
  const [explanation, setExplanation] = useState(
    "This is based on elevated stress signals and the simulated recovery profile. NeuroTwin AI is a wellness prototype and does not provide medical diagnosis or treatment.",
  );
  const [isLoading, setIsLoading] = useState(false);

  const trend = useMemo(() => {
    if (history.length === 0) {
      return demoTrend;
    }
    return history.slice(-8).map((record) => ({
      label: new Date(record.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      stress: record.state.stress,
      fatigue: record.state.fatigue,
      attention: record.state.attention,
    }));
  }, [history]);

  async function runSignalCheck() {
    setIsLoading(true);
    try {
      const samplePayload = {
        typing_speed: 52 + Math.random() * 16,
        pause_variance: 1.2 + Math.random() * 1.8,
        sentiment: -0.35 + Math.random() * 0.7,
        screen_time: 5 + Math.random() * 4,
      };

      const ingestResponse = await fetch(`${API_BASE_URL}/ingest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(samplePayload),
      });
      const ingestJson = await ingestResponse.json();
      setState(ingestJson.state);

      const simulationResponse = await fetch(`${API_BASE_URL}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}),
      });
      const simulationJson = await simulationResponse.json();
      setSimulations(simulationJson.simulations);

      const recommendResponse = await fetch(`${API_BASE_URL}/recommend`);
      const recommendJson = await recommendResponse.json();
      setRecommendation(recommendJson.recommendation);
      setExplanation(recommendJson.explanation);

      const historyResponse = await fetch(`${API_BASE_URL}/state/history?limit=8`);
      const historyJson = await historyResponse.json();
      setHistory(historyJson.records ?? []);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void runSignalCheck();
  }, []);

  return (
    <main className="dashboard">
      <section className="intro">
        <div>
          <p className="eyebrow">Digital cognitive twin</p>
          <h1>NeuroTwin AI</h1>
        </div>
        <button type="button" onClick={runSignalCheck} disabled={isLoading}>
          {isLoading ? "Checking..." : "Run signal check"}
        </button>
      </section>

      <section className="metrics" aria-label="Current cognitive state">
        {Object.entries(state).map(([label, value]) => (
          <article className="metric" key={label}>
            <span>{label}</span>
            <strong>{Math.round(value * 100)}%</strong>
            <meter min="0" max="1" value={value} aria-label={label} />
          </article>
        ))}
      </section>

      <div className="contentGrid">
        <Graph points={trend} />
        <section className="panel recommendation">
          <div className="panelHeader">
            <h2>Recommendation</h2>
          </div>
          <strong>{recommendation.replace("_", " ")}</strong>
          <p>{explanation}</p>
        </section>
      </div>

      <SimulationPanel simulations={simulations} recommendation={recommendation} />
    </main>
  );
}
