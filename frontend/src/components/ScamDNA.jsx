import React from "react";

function ScamDNA({ onNext }) {

  return (
    <div className="dna-page">

      <div className="page-heading">

        <span className="small-label">
          BEHAVIORAL ANALYSIS
        </span>

        <h1>
          🧬 Scam DNA
        </h1>

        <p>
          We detected a recurring recruitment scam pattern.
        </p>

      </div>

      <div className="dna-pattern">

        <div className="dna-step">
          <div className="dna-icon">
            💰
          </div>

          <h3>PAY</h3>

          <p>
            Processing fee requested
          </p>
        </div>

        <div className="dna-arrow">
          →
        </div>

        <div className="dna-step">
          <div className="dna-icon">
            ⚡
          </div>

          <h3>SELECT</h3>

          <p>
            Immediate selection
          </p>
        </div>

        <div className="dna-arrow">
          →
        </div>

        <div className="dna-step">
          <div className="dna-icon">
            📄
          </div>

          <h3>DATA</h3>

          <p>
            Personal information requested
          </p>
        </div>

      </div>

      <div className="dna-details">

        <div className="dna-detail-card">

          <h2>
            Detected Scam Pattern
          </h2>

          <div className="pattern-name">
            Pay-to-get-hired
          </div>

          <p>
            This pattern identifies recruitment offers
            that demand payment before employment.
          </p>

        </div>

        <div className="dna-detail-card">

          <h2>
            Pattern Similarity
          </h2>

          <div className="similarity">
            91%
          </div>

          <p>
            Similar behavior found in previous scam cases.
          </p>

        </div>

      </div>

      <div className="common-signals">

        <h2>
          Common Behavioral Signals
        </h2>

        <div className="tag-container">

          <span>High Salary</span>
          <span>Instant Selection</span>
          <span>No Interview</span>
          <span>Payment Request</span>
          <span>Document Request</span>

        </div>

      </div>

      <button
        className="primary-button centered-button"
        onClick={onNext}
      >
        🔗 Check Scam Campaign
      </button>

    </div>
  );
}

export default ScamDNA;