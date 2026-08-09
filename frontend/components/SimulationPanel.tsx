type SimulationOutcome = { label: string; projected_symptom_burden: number; projected_activity_tolerance: number; safety_status: string; summary: string };
type SimulationPanelProps = { simulations: Record<string, SimulationOutcome>; recommendation: string };

export default function SimulationPanel({ simulations, recommendation }: SimulationPanelProps) {
  return <section className="panel"><div className="panelHeader"><div><p className="eyebrow">What-if comparison</p><h2>Possible next steps</h2></div></div><div className="simulationGrid">{Object.entries(simulations).map(([action, outcome]) => <article className={action === recommendation ? "simCard selected" : "simCard"} key={action}><div className="simTitle"><h3>{outcome.label}</h3>{action === recommendation && <span>Suggested</span>}</div><dl><div><dt>Projected symptoms</dt><dd>{outcome.projected_symptom_burden}/10</dd></div><div><dt>Activity tolerance</dt><dd>{outcome.projected_activity_tolerance}/10</dd></div></dl><p>{outcome.summary}</p></article>)}</div></section>;
}
