import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div style={{
      height: "100vh",
      backgroundImage: "url('/homebg.jpg')",
      backgroundSize: "cover",
      backgroundPosition: "center",
      display: "flex",
      flexDirection: "column",
      justifyContent: "flex-start",   
      alignItems: "center",
      paddingTop: "120px",
      color: "white",
      position: "relative"
    }}>

      {/* Dark overlay */}
      <div style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0,0,0,0.65)",
        zIndex: 1
      }} />

      {/* Content */}
      <div style={{ zIndex: 2, textAlign: "center" }}>

        {/* Heading */}
      <h1 className="hero-title">
  Welcome to HireSense AI
</h1>

        {/* Animated Paragraph */}
      <p className="hero-text">
  Enhance your resume with AI-driven insights. Upload your resume and job description 
  to analyze skill gaps, improve ATS compatibility, and boost your chances of selection.
</p>

        {/* Button */}
        <button className="bubble-btn" onClick={() => navigate("/upload")}>
  Start Analysis
</button>

      </div>
      {/* Animation */}
      <style>
        {`
          @keyframes slideIn {
            0% {
              transform: translateX(-100px);
              opacity: 0;
            }
            100% {
              transform: translateX(0);
              opacity: 1;
            }
          }
        `}
      </style>

    </div>
  );
}