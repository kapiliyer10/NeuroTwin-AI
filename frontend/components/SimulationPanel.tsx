type SimulationOutcome = {
  stress: number;
  fatigue: number;
  attention: number;
  emotion: number;
  summary: string;
};

type SimulationPanelProps = {
  simulations: Record<string, SimulationOutcome>;
  recommendation: string;
};

const labels: Record<string, string> = {
  continue: "Continue",
  short_break: "Short break",
  sleep: "Sleep",
};

export default function SimulationPanel({ simulations, recommendation }: SimulationPanelProps) {
  return (
    <section className="panel">
      <div className="panelHeader">
        <h2>Simulation</h2>
      </div>
      <div className="simulationGrid">
        {Object.entries(simulations).map(([action, outcome]) => (
          <article className={action === recommendation ? "simCard selected" : "simCard"} key={action}>
            <div className="simTitle">
              <h3>{labels[action] ?? action}</h3>
              {action === recommendation && <span>Recommended</span>}
            </div>
            <dl>
              <div>
                <dt>Stress</dt>
                <dd>{Math.round(outcome.stress * 100)}%</dd>
              </div>
              <div>
                <dt>Fatigue</dt>
                <dd>{Math.round(outcome.fatigue * 100)}%</dd>
              </div>
              <div>
                <dt>Attention</dt>
                <dd>{Math.round(outcome.attention * 100)}%</dd>
              </div>
            </dl>
            <p>{outcome.summary}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
