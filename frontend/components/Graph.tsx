type GraphPoint = {
  label: string;
  stress: number;
  fatigue: number;
  attention: number;
};

type GraphProps = {
  points: GraphPoint[];
};

export default function Graph({ points }: GraphProps) {
  const width = 520;
  const height = 180;
  const padding = 24;

  const toX = (index: number) =>
    points.length <= 1 ? padding : padding + (index * (width - padding * 2)) / (points.length - 1);
  const toY = (value: number) => height - padding - value * (height - padding * 2);

  const line = (key: keyof Omit<GraphPoint, "label">) =>
    points.map((point, index) => `${toX(index)},${toY(point[key])}`).join(" ");

  return (
    <section className="panel">
      <div className="panelHeader">
        <h2>State Trend</h2>
      </div>
      <svg className="chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Cognitive state trend">
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} className="axis" />
        <line x1={padding} y1={padding} x2={padding} y2={height - padding} className="axis" />
        <polyline points={line("stress")} className="line stress" />
        <polyline points={line("fatigue")} className="line fatigue" />
        <polyline points={line("attention")} className="line attention" />
      </svg>
      <div className="legend">
        <span><i className="dot stressDot" />Stress</span>
        <span><i className="dot fatigueDot" />Fatigue</span>
        <span><i className="dot attentionDot" />Attention</span>
      </div>
    </section>
  );
}
