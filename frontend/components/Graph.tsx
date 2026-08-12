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
  const visibleLabels = fallback.length <= 3 ? fallback.map((_, index) => index) : [0, Math.floor((fallback.length - 1) / 2), fallback.length - 1];

  const burdenLabel = purpose === "concussion" ? "Symptom burden" : "Wellbeing strain";
  const toleranceLabel = purpose === "concussion" ? "Activity tolerance" : "Capacity estimate";
  return <section className="panel"><div className="panelHeader"><div><p className="eyebrow">Personal timeline</p><h2>{purpose === "concussion" ? "Recovery trend" : "Wellbeing trend"}</h2></div><span className="timelineCount">{points.length} saved {points.length === 1 ? "check-in" : "check-ins"}</span></div><p className="timelineExplain">Each plotted position represents one saved check-in. The horizontal direction shows your saved check-ins over time; it does not record every slider change.</p><div className="chartWrap"><svg className="chart" viewBox={`0 0 ${width} ${height + 24}`} role="img" aria-label={`${purpose === "concussion" ? "Recovery" : "Wellbeing"} trend over ${points.length} saved check-ins`}><line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} className="axis" /><line x1={padding} y1={padding} x2={padding} y2={height - padding} className="axis" /><text x="5" y={height - padding + 4} className="chartLabel">0</text><text x="5" y={height / 2 + 4} className="chartLabel">5</text><text x="5" y={padding + 4} className="chartLabel">10</text>{points.length > 0 && <><polyline points={line("symptom_burden")} className="line burden" /><polyline points={line("activity_tolerance")} className="line tolerance" />{fallback.map((point, index) => <g key={`${point.label}-${index}`}><circle cx={toX(index)} cy={toY(point.symptom_burden)} r="4" className="point burdenPoint" /><circle cx={toX(index)} cy={toY(point.activity_tolerance)} r="4" className="point tolerancePoint" /></g>)}{visibleLabels.map((index) => <text key={`label-${index}`} x={toX(index)} y={height + 10} textAnchor={index === 0 ? "start" : index === fallback.length - 1 ? "end" : "middle"} className="chartLabel">{fallback[index].label}</text>)}</>}</svg>{points.length === 0 && <div className="chartEmpty">Your first saved check-in will appear here as Day 1.</div>}</div><p className="chartHint">Lower {purpose === "concussion" ? "symptoms" : "strain"} and higher {purpose === "concussion" ? "tolerance" : "capacity"} generally indicate improvement. This is a personal trend, not a medical measurement.</p><div className="legend"><span><i className="dot burdenDot" />{burdenLabel}</span><span><i className="dot toleranceDot" />{toleranceLabel}</span></div></section>;
}
