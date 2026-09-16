import React, { useEffect, useState } from "react";

function Analyzing({ onComplete }) {

  const [progress, setProgress] = useState(0);

  useEffect(() => {

    const interval = setInterval(() => {

      setProgress((previous) => {

        if (previous >= 100) {

          clearInterval(interval);

          setTimeout(() => {
            onComplete();
          }, 500);

          return 100;
        }

        return previous + 5;
      });

    }, 100);

    return () => clearInterval(interval);

  }, [onComplete]);

  return (
    <div className="analysis-page">

      <div className="analysis-animation">
        🛡️
      </div>

      <h1>
        Analyzing Job...
      </h1>

      <p>
        Our detection engine is examining the recruitment
        signals in this job.
      </p>

      <div className="progress-container">

        <div
          className="progress-bar"
          style={{
            width: `${progress}%`
          }}
        ></div>

      </div>

      <div className="progress-number">
        {progress}%
      </div>

      <div className="analysis-steps">

        <p className={progress >= 10 ? "completed" : ""}>
          {progress >= 10 ? "✓" : "○"} Extracting job information
        </p>

        <p className={progress >= 25 ? "completed" : ""}>
          {progress >= 25 ? "✓" : "○"} Checking recruiter details
        </p>

        <p className={progress >= 40 ? "completed" : ""}>
          {progress >= 40 ? "✓" : "○"} Checking salary patterns
        </p>

        <p className={progress >= 55 ? "completed" : ""}>
          {progress >= 55 ? "✓" : "○"} Detecting suspicious demands
        </p>

        <p className={progress >= 70 ? "completed" : ""}>
          {progress >= 70 ? "✓" : "○"} Checking company/domain
        </p>

        <p className={progress >= 85 ? "completed" : ""}>
          {progress >= 85 ? "✓" : "○"} Searching similar scam cases
        </p>

        <p className={progress >= 100 ? "completed" : ""}>
          {progress >= 100 ? "✓" : "○"} Building detection report
        </p>

      </div>

    </div>
  );
}

export default Analyzing;