import React from "react";

function CampaignDetection({ onNext }) {

  return (
    <div className="campaign-page">

      <div className="page-heading">

        <span className="small-label">
          THREAT INTELLIGENCE
        </span>

        <h1>
          🚨 Scam Campaign Detected
        </h1>

        <p>
          These seemingly different job offers share
          hidden characteristics.
        </p>

      </div>

      <div className="campaign-alert">

        <strong>
          Potential Coordinated Scam Campaign
        </strong>

        <p>
          3 job advertisements appear to be connected.
        </p>

      </div>

      <div className="network-container">

        <div className="job-node">
          <span>💼</span>
          <strong>JOB #1</strong>
          <small>
            Amazon WFH
          </small>
        </div>

        <div className="connection">
          ↔
        </div>

        <div className="central-node">
          <span>🕵️</span>
          <strong>SCAM NETWORK</strong>
          <small>
            89% similarity
          </small>
        </div>

        <div className="connection">
          ↔
        </div>

        <div className="job-node">
          <span>💼</span>
          <strong>JOB #2</strong>
          <small>
            E-Commerce Support
          </small>
        </div>

      </div>

      <div className="shared-signals">

        <h2>
          Common Hidden Signals
        </h2>

        <div className="shared-grid">

          <div>
            📱
            <strong>Phone</strong>
            <span>Shared contact</span>
          </div>

          <div>
            📧
            <strong>Email</strong>
            <span>Similar recruiter</span>
          </div>

          <div>
            🌐
            <strong>Domain</strong>
            <span>Related domain</span>
          </div>

          <div>
            💳
            <strong>Payment ID</strong>
            <span>Shared account</span>
          </div>

        </div>

      </div>

      <div className="target-profile">

        <h2>
          🎯 Likely Target
        </h2>

        <div className="target-tags">

          <span>🎓 Fresh Graduates</span>

          <span>🎓 Students</span>

          <span>🏠 Remote Job Seekers</span>

        </div>

      </div>

      <button
        className="primary-button centered-button"
        onClick={onNext}
      >
        🛡️ View Safety Warning
      </button>

    </div>
  );
}

export default CampaignDetection;