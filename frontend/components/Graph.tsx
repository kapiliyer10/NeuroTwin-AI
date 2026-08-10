type GraphPoint = { label: string; symptom_burden: number; activity_tolerance: number };

type GraphProps = { points: GraphPoint[]; purpose: "concussion" | "mental_wellbeing" };

export default function Graph({ points, purpose }: GraphProps) {
  const width = 600;
  const height = 220;
  const padding = 28;
  const fallback = points.length ? points : [{ label: "Start", symptom_burden: 2, activity_tolerance: 7.5 }];
  const toX = (index: number) => fallback.length <= 1 ? padding : padding + (index * (width - padding * 2)) / (fallback.length - 1);
  const toY = (value: number) => height - padding - (value / 10) * (height - padding * 2);
  const line = (key: "symptom_burden" | "activity_tolerance") => fallback.map((point, index) => `${toX(index)},${toY(point[key])}`).join(" ");

  const burdenLabel = purpose === "concussion" ? "Symptom burden" : "Wellbeing strain";
  const toleranceLabel = purpose === "concussion" ? "Activity tolerance" : "Capacity estimate";
  return <section className="panel"><div className="panelHeader"><div><p className="eyebrow">Personal timeline</p><h2>{purpose === "concussion" ? "Recovery trend" : "Wellbeing trend"}</h2></div></div><div className="chartWrap"><svg className="chart" viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${purpose === "concussion" ? "Recovery" : "Wellbeing"} trend over check-ins`}><line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} className="axis" /><line x1={padding} y1={padding} x2={padding} y2={height - padding} className="axis" /><text x="5" y={height - padding + 4} className="chartLabel">0</text><text x="5" y={height / 2 + 4} className="chartLabel">5</text><text x="5" y={padding + 4} className="chartLabel">10</text>{points.length > 0 && <><polyline points={line("symptom_burden")} className="line burden" /><polyline points={line("activity_tolerance")} className="line tolerance" /></>}</svg>{points.length === 0 && <div className="chartEmpty">Submit a check-in to start your personal timeline.</div>}</div><p className="chartHint">This is a personal trend across check-ins, not a medical measurement.</p><div className="legend"><span><i className="dot burdenDot" />{burdenLabel}</span><span><i className="dot toleranceDot" />{toleranceLabel}</span></div></section>;
}
