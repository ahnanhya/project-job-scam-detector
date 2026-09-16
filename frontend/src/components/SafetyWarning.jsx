import React from "react";

function SafetyWarning({ onHome }) {

  return (
    <div className="warning-page">

      <div className="warning-icon">
        🚨
      </div>

      <span className="small-label">
        EARLY WARNING SYSTEM
      </span>

      <h1>
        This Job Looks Dangerous
      </h1>

      <p className="warning-description">
        Our analysis found multiple indicators
        associated with recruitment scams.
      </p>

      <div className="warning-grid">

        <div className="warning-card">

          <span>💰</span>

          <h3>
            DO NOT PAY
          </h3>

          <p>
            Do not pay registration, training,
            verification or processing fees.
          </p>

        </div>

        <div className="warning-card">

          <span>🔐</span>

          <h3>
            DO NOT SHARE
          </h3>

          <p>
            Never share bank details, passwords
            or identity documents unnecessarily.
          </p>

        </div>

        <div className="warning-card">

          <span>🔗</span>

          <h3>
            DO NOT CLICK
          </h3>

          <p>
            Avoid unknown payment and
            verification links.
          </p>

        </div>

      </div>

      <div className="warning-actions">

        <button
          className="danger-button"
          onClick={() => alert(
            "Thank you. This suspicious job has been reported."
          )}
        >
          🚩 Report Scam
        </button>

        <button
          className="secondary-button"
          onClick={onHome}
        >
          🔍 Check Another Job
        </button>

      </div>

    </div>
  );
}

export default SafetyWarning;