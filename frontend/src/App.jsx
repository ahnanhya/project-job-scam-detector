import React, { useEffect, useState } from "react";

import Navbar from "./components/Navbar";
import Home from "./components/Home";
import AnalyzeJob from "./components/AnalyzeJob";
import Analyzing from "./components/Analyzing";
import DetectionReport from "./components/DetectionReport";
import Dashboard from "./components/Dashboard";
import JobVerification from "./components/JobVerification";


function App() {

  const [page, setPage] = useState("home");
  const [theme, setTheme] = useState(() => localStorage.getItem("jobguard-theme") || "light");

  useEffect(() => {
    localStorage.setItem("jobguard-theme", theme);
  }, [theme]);


  const [jobData, setJobData] = useState({
    text: "",
    score: 0,
    risk: "",
    signals: [],
    scam_dna: [],
    explanations: [],
    entities: {
      emails: [],
      phones: []
    },
    campaign_indicators: [],
    message: "",
    campaign_analysis: {}
  });


  // --------------------------------------------------
  // EXISTING JOB ANALYSIS
  // --------------------------------------------------

  const startAnalysis = async (text) => {

    setJobData({
      ...jobData,
      text: text
    });

    setPage("analyzing");


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            text: text
          })
        }
      );


      if (!response.ok) {
        throw new Error(
          "Backend server error"
        );
      }


      const result =
        await response.json();


      console.log(
        "Backend Result:",
        result
      );


      if (result.status !== "success") {

        alert(
          result.message ||
          "Unable to analyze the job."
        );

        setPage("analyze");

        return;
      }


      const data = result.data;


      setJobData({
        text: text,

        score: data.risk_score,

        risk: data.risk,

        signals: data.signals,

        scam_dna: data.scam_dna,

        explanations: data.explanations,

        entities: data.entities,

        campaign_indicators:
          data.campaign_indicators,

        message: data.message,

        campaign_analysis: result.campaign_analysis || {}
      });


      setPage("report");

    }

    catch (error) {

      console.error(
        "Analysis Error:",
        error
      );


      alert(
        "Unable to connect to the Job Scam Detector backend. Make sure FastAPI is running."
      );


      setPage("analyze");
    }
  };


  // --------------------------------------------------
  // PAGE DISPLAY
  // --------------------------------------------------

  return (

    <div className={theme === "dark" ? "app dark-mode" : "app"}>


      {/* NAVBAR */}

      <Navbar
        currentPage={page}
        onNavigate={setPage}
        theme={theme}
        onToggleTheme={() => setTheme(theme === "dark" ? "light" : "dark")}
      />


      {/* HOME */}

      {page === "home" && (

        <Home
          onAnalyze={startAnalysis}
        />

      )}


      {/* NORMAL JOB ANALYSIS */}

      {page === "analyze" && (

        <AnalyzeJob
          onAnalyze={startAnalysis}
        />

      )}


      {/* ANALYZING */}

      {page === "analyzing" && (

        <Analyzing
          onComplete={() => {}}
        />

      )}


      {/* DETECTION REPORT */}

      {page === "report" && (

        <DetectionReport
          jobData={jobData}
        />

      )}


      {/* DASHBOARD */}

      {page === "dashboard" && (

        <Dashboard />

      )}


      {/* REAL JOB VERIFICATION */}

      {page === "verification" && (

        <JobVerification
          onBack={() =>
            setPage("home")
          }

        />

      )}

    </div>
  );
}


export default App;