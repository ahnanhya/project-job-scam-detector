import React from "react";

function DetectionReport({ jobData }) {
  const signals = jobData.signals?.length
    ? jobData.signals
    : ["Suspicious recruitment behavior detected."];

  const scamDNA = jobData.scam_dna?.length
    ? jobData.scam_dna
    : [
        "Payment request before onboarding",
        "Urgent hiring without interview",
        "Personal data collection before verification"
      ];

  const explanations = jobData.explanations?.length
    ? jobData.explanations
    : ["The job posting contains several strong scam indicators."];

  const campaignIndicators = jobData.campaign_indicators?.length
    ? jobData.campaign_indicators
    : [
        "Shared recruiter identity patterns",
        "Repeated remote-only job messaging",
        "High-risk fee and verification language"
      ];

  const emails = jobData.entities?.emails?.length
    ? jobData.entities.emails
    : [];

  const phones = jobData.entities?.phones?.length
    ? jobData.entities.phones
    : [];

  const basis = [
    "Looked for urgent language such as 'immediate hiring' or 'reply now'.",
    "Checked for requests to pay money before joining.",
    "Looked for personal data requests like ID, bank details, or passport photos.",
    "Checked whether the role uses fake remote-job patterns or repeated scam language."
  ];

  return (
    <div className="report-page">
      <div className="page-heading">
        <span className="small-label">SCAM RISK REPORT</span>
        <h1>Job Safety Analysis</h1>
        <p className="report-subtitle">
          Simple and clear review of the job opportunity based on common scam indicators.
        </p>
      </div>

      <div className="report-grid">
        <div className="risk-card">
          <div className="warning-symbol">⚠️</div>
          <p className="risk-title">RISK SCORE</p>
          <div className="risk-score">
            {jobData.score}
            <span>/100</span>
          </div>
          <div className="risk-level">🔴 {jobData.risk}</div>
          <p className="risk-note">This job shows strong signs of a fraudulent recruitment pattern.</p>
        </div>

        <div className="signals-card">
          <h2>What raised concern</h2>
          <div className="signal-list">
            {signals.map((signal, index) => (
              <div className="signal-item" key={index}>
                <span>✓</span>
                <p>{signal}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="report-section">
        <h2>🚨 Campaign pattern</h2>
        <div className="campaign-alert">
          <strong>Potential coordinated scam network</strong>
          <p>Several job ads may share the same scam setup and tactics.</p>
        </div>

        <div className="shared-grid">
          {campaignIndicators.slice(0, 4).map((item, index) => (
            <div key={index}>
              <span>{["📱", "📧", "🌐", "💳"][index % 4]}</span>
              <strong>{["Phone", "Email", "Domain", "Payment"][index % 4]}</strong>
              <span>{item}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="report-section">
        <h2>🛡️ Safety guidance</h2>
        <div className="warning-grid">
          <div className="warning-card">
            <span>💰</span>
            <h3>Do not pay</h3>
            <p>Do not pay registration, training, or verification fees before confirming the employer.</p>
          </div>

          <div className="warning-card">
            <span>🔐</span>
            <h3>Do not share</h3>
            <p>Never share bank details, passwords, or identity documents without verification.</p>
          </div>

          <div className="warning-card">
            <span>🔗</span>
            <h3>Do not click</h3>
            <p>Avoid unknown payment or verification links sent through messaging apps.</p>
          </div>
        </div>
      </div>

      <div className="report-section">
        <h2> Evidence summary</h2>
        <div className="summary-grid">
          <div className="summary-box">
            <h3>Why this was flagged</h3>
            <ul className="summary-list">
              {explanations.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="summary-box">
            <h3>Contact details found</h3>
            <ul className="summary-list">
              {emails.length > 0 ? (
                emails.map((email, index) => <li key={`email-${index}`}>{email}</li>)
              ) : (
                <li>No email address detected in the submitted text.</li>
              )}

              {phones.length > 0 ? (
                phones.map((phone, index) => <li key={`phone-${index}`}>{phone}</li>)
              ) : (
                <li>No phone number detected in the submitted text.</li>
              )}
            </ul>
          </div>
        </div>
      </div>

      <div className="report-section report-flow">
        <h2>How the analysis works</h2>
        <div className="analysis-flow">
          <div className="flow-step">
            <div className="flow-icon">🧾</div>
            <h3>1. Read the post</h3>
            <p>We review the wording and pattern of the job ad.</p>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">🔎</div>
            <h3>2. Check red flags</h3>
            <p>We scan for payment requests, fake urgency, and personal data demands.</p>
          </div>
          <div className="flow-arrow">→</div>
          <div className="flow-step">
            <div className="flow-icon">📊</div>
            <h3>3. Score the risk</h3>
            <p>Each warning adds to the final risk score.</p>
          </div>
        </div>
      </div>

      <div className="report-section">
        <h2>📌 Basis of this analysis</h2>
        <div className="basis-grid">
          {basis.map((item, index) => (
            <div className="basis-card" key={index}>
              <span className="basis-bullet">●</span>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DetectionReport;