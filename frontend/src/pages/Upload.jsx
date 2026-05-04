import { useState } from "react";
import { useNavigate } from "react-router-dom";
export default function Upload() {
  const [resume, setResume] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const handleSubmit = async () => {
    if (!resume) {
      alert("Upload resume");
      return;
    }
    if (!jdFile && !jdText.trim()) {
      alert("Upload JD or paste text");
      return;
    }
    const formData = new FormData();
    formData.append("resume", resume);
    if (jdFile) {
      formData.append("jd_file", jdFile);
    } else {
      formData.append("job_description", jdText);
    }
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      navigate("/results", { state: data });
    } catch (err) {
      alert("Error");
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="upload-page">
        <div style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0,0,0,0.65)",
        zIndex: 1
      }} />
     <div className="upload-card" style={{ position: "relative", zIndex: 2 }}>
       <h2 className="upload-title">
  Upload Resume & Job Description
</h2>
        <label>Resume</label>
        <input type="file" onChange={(e) => setResume(e.target.files[0])} />
        <label>JD File (optional)</label>
        <input type="file" onChange={(e) => setJdFile(e.target.files[0])} />
        <p style={{ marginTop: "10px" }}>OR</p>
        <textarea
          placeholder="Paste Job Description..."
          rows="5"
          onChange={(e) => setJdText(e.target.value)}
        />
        <button onClick={handleSubmit} className="upload-btn">
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>
    </div>
  );
}