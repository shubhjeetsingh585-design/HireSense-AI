import { useLocation } from "react-router-dom";
import { Pie, Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);
export default function Results() {

const location = useLocation();
const data = location.state;
if (!data) return <h2>No data available</h2>;
const matched = data.matched_skills || [];
const missing = data.missing_skills || [];
const resumeSkills = (data.resume_skills || []);
const jdSkills = (data.jd_keywords || []);
 return (
  <div className="results-page">
    <h1 className="results-title">Analysis Results</h1>
    {/* ATS Score */}
    <div className="card">
      <h2>ATS Score: {data.ats_score_after}</h2>
    </div>
    {/* Bar Chart */}
    <div className="card chart-card">
      <Bar
        data={{
          labels: ["Before", "After"],
          datasets: [{
            label: "ATS Score",
            data: [
              data.ats_score_before,
              data.ats_score_after
            ],
            backgroundColor: ["#FF9800", "#2196F3"],
          }]
        }}
        options={{
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }}
      />
    </div>
    {/* Skills */}
    <div className="grid-2">
      <div className="card">
        <h3 style={{ color: "#22c55e" }}>Matched Skills</h3>
        <ul>
          {matched.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h3 style={{ color: "#ef4444" }}>Missing Skills</h3>
        <ul>
          {missing.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      </div>
    </div>
    {/* Pie Chart */}
    <div className="card chart-card">
         <h3>Skill Match</h3>
        <div className="chart-center">
      <Pie
        data={{
          labels: ["Matched", "Missing"],
          datasets: [{
            data: [matched.length, missing.length],
            backgroundColor: ["#4CAF50", "#F44336"],
          }]
        }}
      />
      </div>
    </div>
    {/* Resume vs JD */}
    <div className="grid-2">
      <div className="card chart-card">
        <h3>Resume Skills</h3>
        <div className="chart-center">
        <Pie
          data={{
            labels: resumeSkills,
            datasets: [{
              data: resumeSkills.map(() => 1),
              backgroundColor: [
                "#2196F3", "#4CAF50", "#FFC107",
                "#FF5722", "#9C27B0", "#00BCD4"
              ],
            }]
          }}
        />
        </div>
      </div>
      <div className="card chart-card">
        <h3>JD Skills</h3>
        <div className="chart-center">
        <Pie
          data={{
            labels: jdSkills,
            datasets: [{
              data: jdSkills.map(() => 1),
              backgroundColor: [
                "#E91E63", "#3F51B5", "#009688",
                "#CDDC39", "#FFEB3B", "#795548"
              ],
            }]
          }}
        />
        </div>
      </div>
    </div>
    {/* Suggestions */}
    <div className="card">
      <h3>Suggestions</h3>
      <ul>
        {(data.suggestions || []).map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
    {/* Resume */}
    <div className="card">
      <h3>Rewritten Resume</h3>
      <p>{data.rewritten_resume}</p>
    </div>
  </div>
);
}