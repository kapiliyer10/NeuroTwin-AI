"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";

import Graph from "./Graph";
import SimulationPanel from "./SimulationPanel";

type RecoveryState = {
  purpose: string;
  symptom_burden: number;
  fatigue: number;
  cognitive_load: number;
  activity_tolerance: number;
  trend: string;
  risk_level: string;
  stage: number;
};

type SafetyAssessment = {
  status: string;
  message: string;
  reasons: string[];
  seek_urgent_care: boolean;
};

type Evidence = { title: string; publisher: string; url: string; reviewed: string };
type HistoryRecord = { timestamp: string; state: RecoveryState; safety: SafetyAssessment };
type SimulationOutcome = {
  action: string;
  label: string;
  projected_symptom_burden: number;
  projected_activity_tolerance: number;
  safety_status: string;
  summary: string;
};

type Purpose = "concussion" | "mental_wellbeing";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const initialState: RecoveryState = {
  purpose: "concussion",
  symptom_burden: 2,
  fatigue: 2,
  cognitive_load: 2,
  activity_tolerance: 7.5,
  trend: "baseline",
  risk_level: "low",
  stage: 1,
};

const initialForm = {
  user_id: "demo-user",
  purpose: "concussion" as Purpose,
  clinician_evaluated: false,
  recovery_stage: 1,
  activity_type: "daily",
  activity_minutes: 15,
  headache: 1,
  dizziness: 0,
  nausea: 0,
  light_sensitivity: 0,
  noise_sensitivity: 0,
  fatigue: 2,
  sleep_quality: 7,
  memory_difficulty: 1,
  concentration_difficulty: 1,
  balance_problem: 0,
  mood_change: 0,
  symptoms_after_activity: 0,
  symptoms_worsened: false,
  severe_or_worsening_headache: false,
  repeated_vomiting: false,
  seizure_or_fainting: false,
  confusion_or_slurred_speech: false,
  weakness_numbness_or_vision_change: false,
  stress_level: 0,
  mood: 5,
  social_connection: 5,
  workload_pressure: 0,
  feeling_unsafe: false,
  self_harm_thoughts: false,
};

const symptomFields = [
  ["headache", "Headache"],
  ["dizziness", "Dizziness"],
  ["nausea", "Nausea"],
  ["light_sensitivity", "Light sensitivity"],
  ["noise_sensitivity", "Noise sensitivity"],
  ["fatigue", "Fatigue"],
  ["memory_difficulty", "Memory difficulty"],
  ["concentration_difficulty", "Concentration difficulty"],
  ["balance_problem", "Balance problems"],
  ["mood_change", "Mood change"],
];

const wellbeingFields = [
  ["stress_level", "Stress level", "0 none · 10 overwhelming"],
  ["mood", "Mood today", "0 very low · 10 positive"],
  ["sleep_quality", "Sleep quality", "0 poor · 10 restorative"],
  ["concentration_difficulty", "Focus difficulty", "0 none · 10 severe"],
  ["workload_pressure", "Workload pressure", "0 none · 10 overwhelming"],
  ["social_connection", "Social connection", "0 isolated · 10 connected"],
] as const;

const recoveryStages = [
  [1, "Daily activities"],
  [2, "Light aerobic activity"],
  [3, "Individual activity, no head-impact risk"],
  [4, "Non-contact practice"],
  [5, "Unrestricted practice"],
  [6, "Return to sport"],
] as const;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) throw new Error((await response.text()) || "The recovery service is unavailable.");
  return response.json() as Promise<T>;
}

export default function Dashboard() {
  const [form, setForm] = useState(initialForm);
  const [selectedPurpose, setSelectedPurpose] = useState<Purpose | null>(null);
  const [state, setState] = useState(initialState);
  const [safety, setSafety] = useState<SafetyAssessment>({ status: "monitor", message: "Complete a check-in to begin.", reasons: [], seek_urgent_care: false });
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [evidence, setEvidence] = useState<Evidence[]>([]);
  const [simulations, setSimulations] = useState<Record<string, SimulationOutcome>>({});
  const [recommendation, setRecommendation] = useState("continue_gently");
  const [explanation, setExplanation] = useState("Your recovery timeline will appear here after your first check-in.");
  const [hasCheckIn, setHasCheckIn] = useState(false);
  const [lastUpdated, setLastUpdated] = useState("");
  const [error, setError] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function refreshHistory() {
    const result = await request<{ records: HistoryRecord[] }>(`/state/history?limit=12&user_id=${encodeURIComponent(form.user_id)}`);
    setHistory(result.records);
  }

  async function submitCheckIn(event: FormEvent) {
    event.preventDefault();
    setIsLoading(true);
    setError("");
    try {
      const result = await request<{
        state: RecoveryState;
        safety: SafetyAssessment;
        recommendation: string;
        explanation: string;
        evidence: Evidence[];
      }>("/ingest", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(form) });
      setState(result.state);
      setSafety(result.safety);
      setRecommendation(result.recommendation);
      setExplanation(result.explanation);
      setEvidence(result.evidence);
      setHasCheckIn(true);
      setLastUpdated(new Date().toLocaleString([], { dateStyle: "medium", timeStyle: "short" }));
      const simulation = await request<{ simulations: Record<string, SimulationOutcome> }>("/simulate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
      setSimulations(simulation.simulations);
      await refreshHistory();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to save the check-in.");
    } finally {
      setIsLoading(false);
    }
  }

  async function deleteData() {
    if (!window.confirm("Delete all recovery check-ins from this demo?")) return;
    setError("");
    setStatusMessage("");
    try {
      const response = await fetch(`${API_BASE_URL}/state?user_id=${encodeURIComponent(form.user_id)}`, { method: "DELETE" });
      if (!response.ok) throw new Error("The server could not delete your recovery data.");
      setHistory([]);
      setEvidence([]);
      setSimulations({});
      setState(initialState);
      setSafety({ status: "monitor", message: "Your local recovery data was deleted.", reasons: [], seek_urgent_care: false });
      setHasCheckIn(false);
      setLastUpdated("");
      setForm({ ...initialForm, purpose: selectedPurpose ?? "concussion" });
      setStatusMessage("Your recovery data was deleted.");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to delete your data.");
    }
  }

  useEffect(() => {
    void refreshHistory().catch(() => undefined);
  }, []);

  const trend = useMemo(() => history.map((record) => ({
    label: new Date(record.timestamp).toLocaleDateString([], { month: "short", day: "numeric" }),
    symptom_burden: record.state.symptom_burden,
    activity_tolerance: record.state.activity_tolerance,
  })), [history]);

  function updateField(name: string, value: string | number | boolean) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function choosePurpose(purpose: Purpose) {
    setSelectedPurpose(purpose);
    setForm((current) => ({ ...current, purpose }));
  }

  function changePurpose() {
    setSelectedPurpose(null);
    setHasCheckIn(false);
    setHistory([]);
    setEvidence([]);
    setSimulations({});
    setState(initialState);
    setSafety({ status: "monitor", message: "Complete a check-in to begin.", reasons: [], seek_urgent_care: false });
    setRecommendation("continue_gently");
    setExplanation("Your check-in will appear here after you choose a purpose.");
    setLastUpdated("");
    setError("");
    setStatusMessage("");
  }

  if (!selectedPurpose) {
    return (
      <main className="purposeGate">
        <div className="purposeBrand"><p className="eyebrow">Symptom-guided support</p><span className="demoBadge">Prototype demo</span></div>
        <h1>NeuroTwin</h1>
        <p className="purposeLead">What kind of support are you looking for today?</p>
        <div className="purposeChoices">
          <button type="button" className="purposeChoice" onClick={() => choosePurpose("concussion")}><span className="purposeNumber">01</span><strong>Concussion recovery</strong><small>Track symptoms and activity while returning to daily life.</small></button>
          <button type="button" className="purposeChoice" onClick={() => choosePurpose("mental_wellbeing")}><span className="purposeNumber">02</span><strong>Mental wellbeing</strong><small>Reflect on stress, mood, sleep, workload, and connection.</small></button>
        </div>
        <p className="purposeLimit">This prototype offers supportive guidance, not diagnosis or treatment.</p>
        {statusMessage && <p className="successMessage" role="status">{statusMessage}</p>}
      </main>
    );
  }

  return (
    <main className="dashboard">
      <header className="intro">
        <div>
          <div className="eyebrowLine"><p className="eyebrow">{selectedPurpose === "concussion" ? "Concussion recovery support" : "Mental wellbeing support"}</p><span className="demoBadge">Prototype demo</span></div>
          <h1>NeuroTwin {selectedPurpose === "concussion" ? "Recovery" : "Wellbeing"}</h1>
          <p className="subtitle">{selectedPurpose === "concussion" ? "A private, evidence-grounded companion for returning to daily activity after a clinician-evaluated concussion." : "A private reflection space for noticing stress, mood, sleep, workload, and connection without diagnosing mental health conditions."}</p>
        </div>
        <div className="headerActions"><button className="quietButton" type="button" onClick={changePurpose}>Change purpose</button><button className="quietButton" type="button" onClick={deleteData}>Delete my data</button></div>
      </header>

      {error && <div className="alert error" role="alert">{error}</div>}
      {statusMessage && <div className="alert success" role="status">{statusMessage}</div>}
      {safety.status !== "monitor" && <div className={`alert ${safety.seek_urgent_care ? "urgent" : "caution"}`} role="alert"><strong>{safety.message}</strong>{safety.reasons.length > 0 && <span> Detected: {safety.reasons.join(", ")}.</span>}</div>}

      <div className="mainGrid">
        <form className="panel checkIn" onSubmit={submitCheckIn}>
          <div className="panelHeader"><div><p className="eyebrow">Daily check-in</p><h2>How are your symptoms today?</h2></div><span className="scaleHint">0 = none · 10 = severe</span></div>
          <div className="formRow twoColumns">
            {selectedPurpose === "concussion" ? <label>Activity type<select value={form.activity_type} onChange={(event) => updateField("activity_type", event.target.value)}>{["daily", "school", "work", "screen", "walking", "exercise", "sport"].map((value) => <option key={value}>{value}</option>)}</select><small className="fieldHint">What activity did you do or plan to do?</small></label> : <label>Check-in context<select value={form.activity_type} onChange={(event) => updateField("activity_type", event.target.value)}>{["daily", "school", "work", "screen"].map((value) => <option key={value}>{value}</option>)}</select><small className="fieldHint">What part of your day are you reflecting on?</small></label>}
            <label>Minutes today<input type="number" min="0" max="1440" value={form.activity_minutes} onChange={(event) => updateField("activity_minutes", Number(event.target.value))} /></label>
          </div>
          <details className="scaleGuide" open><summary>How to read the 0–10 scale</summary>{selectedPurpose === "concussion" ? <div className="scaleRows"><span><b>0</b> None</span><span><b>1–2</b> Mild</span><span><b>3–5</b> Moderate</span><span><b>6–7</b> High</span><span><b>8–10</b> Very high</span></div> : <div className="scaleGuideText"><p><strong>Strain scales</strong> such as stress, focus difficulty, and workload: 0–2 low, 3–5 moderate, 6–7 high, 8–10 very high.</p><p><strong>Positive scales</strong> such as mood, sleep, and social connection: 0–2 low, 3–5 mixed, 6–7 good, 8–10 strong.</p></div>}<small className="fieldHint">These are personal reflection ratings, not clinical measurements or diagnoses.</small></details>
          <div className="symptomGrid">{(selectedPurpose === "concussion" ? symptomFields : wellbeingFields).map((field) => { const [name, label, hint] = field; return <label key={name}>{label}<input type="range" min="0" max="10" value={form[name as keyof typeof form] as number} onChange={(event) => updateField(name, Number(event.target.value))} /><output>{form[name as keyof typeof form]}</output>{hint && <small className="fieldHint">{hint}</small>}</label>; })}</div>
          <div className="formRow twoColumns">
            <label>{selectedPurpose === "concussion" ? "Symptoms after activity" : "Change after activity"}<input type="range" min="0" max="10" value={form.symptoms_after_activity} onChange={(event) => updateField("symptoms_after_activity", Number(event.target.value))} /><output>{form.symptoms_after_activity}</output><small className="fieldHint">0 no change · 10 much worse</small></label>
            {selectedPurpose === "concussion" ? <label>Recovery stage<select value={form.recovery_stage} onChange={(event) => updateField("recovery_stage", Number(event.target.value))}>{recoveryStages.map(([stage, label]) => <option key={stage} value={stage}>Stage {stage}: {label}</option>)}</select><small className="fieldHint">Use the stage provided by your healthcare professional. This app does not clear you to advance.</small></label> : <div />}
          </div>
          {selectedPurpose === "concussion" && <><label className="checkbox"><input type="checkbox" checked={form.clinician_evaluated} onChange={(event) => updateField("clinician_evaluated", event.target.checked)} /> I have been evaluated by a healthcare professional</label><label className="checkbox"><input type="checkbox" checked={form.symptoms_worsened} onChange={(event) => updateField("symptoms_worsened", event.target.checked)} /> My symptoms are worse than my recent baseline</label><details className="safetyDetails"><summary>Safety check</summary><div className="checkboxList">{([["severe_or_worsening_headache", "Severe or worsening headache"], ["repeated_vomiting", "Repeated vomiting"], ["seizure_or_fainting", "Seizure or fainting"], ["confusion_or_slurred_speech", "Confusion or slurred speech"], ["weakness_numbness_or_vision_change", "Weakness, numbness, or vision changes"]] as const).map(([name, label]) => <label className="checkbox" key={name}><input type="checkbox" checked={form[name]} onChange={(event) => updateField(name, event.target.checked)} /> {label}</label>)}</div></details></>}
          {selectedPurpose === "mental_wellbeing" && <details className="safetyDetails"><summary>Private safety check</summary><div className="checkboxList"><label className="checkbox"><input type="checkbox" checked={form.feeling_unsafe} onChange={(event) => updateField("feeling_unsafe", event.target.checked)} /> I feel unsafe right now</label><label className="checkbox"><input type="checkbox" checked={form.self_harm_thoughts} onChange={(event) => updateField("self_harm_thoughts", event.target.checked)} /> I am having thoughts of harming myself</label><small className="fieldHint">If either is selected, the app will encourage immediate local support.</small></div></details>}
          <button className="primaryButton" type="submit" disabled={isLoading}>{isLoading ? "Saving check-in..." : "Save check-in"}</button>
        </form>

        <section className="panel nextStep"><div className="panelHeader"><div><p className="eyebrow">Your next step</p><h2>{hasCheckIn ? recommendation.replaceAll("_", " ") : "Complete a check-in to begin"}</h2></div>{hasCheckIn && <span className={`status ${safety.status}`}>{safety.status.replaceAll("_", " ")}</span>}</div><p>{hasCheckIn ? explanation : "Your recommendation will be based on your check-in after you save it."}</p><div className="stateList"><div><span>{selectedPurpose === "concussion" ? "Symptom burden" : "Wellbeing strain"}</span><strong>{hasCheckIn ? `${state.symptom_burden}/10` : "Not recorded"}</strong></div><div><span>{selectedPurpose === "concussion" ? "Prototype tolerance estimate" : "Prototype capacity estimate"}</span><strong>{hasCheckIn ? `${state.activity_tolerance}/10` : "Not recorded"}</strong></div><div><span>Trend</span><strong>{hasCheckIn ? state.trend : "Waiting"}</strong></div>{selectedPurpose === "concussion" && <div><span>Current stage</span><strong>{state.stage} of 6</strong></div>}{lastUpdated && <div><span>Last updated</span><strong>{lastUpdated}</strong></div>}</div></section>
      </div>

      <div className="contentGrid"><Graph points={trend} purpose={selectedPurpose} /><section className="panel evidence"><div className="panelHeader"><div><p className="eyebrow">Transparent by design</p><h2>Evidence and limits</h2></div></div><p>{selectedPurpose === "concussion" ? "Recommendations are symptom-guided. They do not diagnose concussion or provide medical clearance." : "Reflections are supportive prompts. They do not diagnose or treat mental-health conditions."}</p>{evidence.map((item) => <a key={item.url} href={item.url} target="_blank" rel="noreferrer">{item.title}<small>{item.publisher}</small></a>)}</section></div>
      {safety.status === "urgent" && <section className="panel urgentPanel"><p className="eyebrow">Safety takes priority</p><h2>Activity comparisons are hidden</h2><p>Follow the urgent-care guidance above. The app will not compare activity options while a serious safety concern is active.</p></section>}
      {Object.keys(simulations).length > 0 && safety.status !== "urgent" && <SimulationPanel simulations={simulations} recommendation={recommendation} />}
    </main>
  );
}
