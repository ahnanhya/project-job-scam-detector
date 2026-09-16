import React, { useState } from "react";

function AnalyzeJob({ onAnalyze }) {

  const [text, setText] = useState("");

  const submitJob = () => {

    if (!text.trim()) {
      alert("Please enter a job description.");
      return;
    }

    onAnalyze(text);
  };

  return (
    <div className="page-container">

      <div className="page-heading">

        <span className="small-label">
          JOB ANALYSIS
        </span>

        <h1>
          Check a job before you apply
        </h1>

        <p>
          Our system analyzes recruitment behavior,
          contact information and suspicious demands.
        </p>

      </div>

      <div className="analysis-input-card">

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste job description here..."
        />

        <button
          className="primary-button"
          onClick={submitJob}
        >
          🔍 Start Detection
        </button>

      </div>

    </div>
  );
}

export default AnalyzeJob;