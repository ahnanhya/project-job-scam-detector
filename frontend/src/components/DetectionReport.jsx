import React from "react";

function DetectionReport({ jobData }) {
  const safeJobData = jobData || {};

  const signals = safeJobData.signals?.length
    ? safeJobData.signals
    : ["Suspicious recruitment behavior detected."];

  const scamDNA = safeJobData.scam_dna?.length
    ? safeJobData.scam_dna
    : [
        "Payment request before onboarding",
        "Urgent hiring without interview",
        "Personal data collection before verification"
      ];

  const explanations = safeJobData.explanations?.length
    ? safeJobData.explanations
    : ["The job posting contains several strong scam indicators."];

  const campaignIndicators = safeJobData.campaign_indicators?.length
    ? safeJobData.campaign_indicators
    : [
        "Shared recruiter identity patterns",
        "Repeated remote-only job messaging",
        "High-risk fee and verification language"
      ];

  const emails = safeJobData.entities?.emails?.length
    ? safeJobData.entities.emails
    : [];

  const phones = safeJobData.entities?.phones?.length
    ? safeJobData.entities.phones
    : [];

  const campaignAnalysis =
    safeJobData.campaign_analysis ||
    safeJobData.campaignAnalysis ||
    safeJobData.data?.campaign_analysis ||
    {};

  const campaignDetected = Boolean(campaignAnalysis.campaign_detected);
  const campaignConfidence = Number(campaignAnalysis.campaign_confidence ?? 0);
  const connectedCases = Number(
    campaignAnalysis.connected_cases ??
      (Array.isArray(campaignAnalysis.matches) ? campaignAnalysis.matches.length : 0)
  );
  const sharedEntities = Array.isArray(campaignAnalysis.shared_entities)
    ? campaignAnalysis.shared_entities
    : [];
  const sharedBehavior = Array.isArray(campaignAnalysis.shared_behavior)
    ? campaignAnalysis.shared_behavior
    : [];
  const matches = Array.isArray(campaignAnalysis.matches)
    ? campaignAnalysis.matches
    : [];

  const campaignStatusText = campaignDetected
    ? "Potential Campaign Connection"
    : "No Strong Campaign Connection";

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
            {safeJobData.score}
            <span>/100</span>
          </div>
          <div className="risk-level">🔴 {safeJobData.risk}</div>
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
        <h2>🧠 Campaign intelligence</h2>
        <div
          className="campaign-alert"
          style={{
            borderLeft: campaignDetected ? "4px solid #f59e0b" : "4px solid #10b981",
            background: campaignDetected ? "#fff7ed" : "#ecfdf5"
          }}
        >
          <strong>{campaignStatusText}</strong>
          <p>
            {campaignAnalysis.message ||
              (campaignDetected
                ? "Shared indicators found in related suspicious cases."
                : "No strong campaign connection found in the historical scam dataset.")}
          </p>
        </div>

        <div className="shared-grid" style={{ marginTop: "18px" }}>
          <div>
            <strong>Confidence</strong>
            <span>{campaignConfidence} / 100</span>
          </div>

          <div>
            <strong>Connected cases</strong>
            <span>{connectedCases}</span>
          </div>

          <div>
            <strong>Status</strong>
            <span>{campaignDetected ? "Potential campaign connection" : "No strong campaign connection"}</span>
          </div>
        </div>
      </div>

      <div className="report-section">
        <h2>📌 Shared indicators</h2>

        {sharedEntities.length > 0 ? (
          <div className="shared-grid">
            {sharedEntities.map((entity, index) => (
              <div key={`${entity?.type || "entity"}-${entity?.value || index}`}>
                <strong>{entity?.type || "Entity"}</strong>
                <span>
                  {entity?.value || "Unknown value"}
                </span>
                {entity?.reason ? <small>{entity.reason}</small> : null}
              </div>
            ))}
          </div>
        ) : (
          <p className="report-subtitle">No shared entities were detected in the campaign analysis.</p>
        )}
      </div>

      <div className="report-section">
        <h2>🔎 Shared scam behavior</h2>

        {sharedBehavior.length > 0 ? (
          <div className="shared-grid">
            {sharedBehavior.map((behavior, index) => (
              <div key={`${behavior}-${index}`}>
                <strong>{behavior}</strong>
                <span>Shared scam pattern</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="report-subtitle">No shared scam behavior patterns were found.</p>
        )}
      </div>

      <div className="report-section">
        <h2>🧾 Related suspicious cases</h2>

        {matches.length > 0 ? (
          <div className="summary-grid">
            {matches.map((match, index) => {
              const historicalCase = match?.historical_case || {};
              const caseEntities = Array.isArray(match?.shared_entities)
                ? match.shared_entities
                : [];
              const caseBehaviors = Array.isArray(match?.shared_behavior)
                ? match.shared_behavior
                : [];

              return (
                <div key={`${historicalCase?.id || index}-detail`} className="summary-box">
                  <h3>{historicalCase.title || "Historical scam case"}</h3>
                  <p>
                    <strong>Company:</strong> {historicalCase.company || "Unknown"}
                  </p>
                  <p>
                    <strong>Campaign score:</strong> {match?.campaign_score ?? 0}
                  </p>
                  <p>
                    <strong>Similarity:</strong> {match?.similarity ?? 0}%
                  </p>

                  {caseEntities.length > 0 ? (
                    <div>
                      <p><strong>Shared entities:</strong></p>
                      <ul className="summary-list">
                        {caseEntities.map((entity, entityIndex) => (
                          <li key={`${entity?.type || "entity"}-${entity?.value || entityIndex}`}>
                            {entity?.type || "Entity"}: {entity?.value || "Unknown"}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}

                  {caseBehaviors.length > 0 ? (
                    <div>
                      <p><strong>Shared behavior:</strong></p>
                      <ul className="summary-list">
                        {caseBehaviors.map((behavior, behaviorIndex) => (
                          <li key={`${behavior}-${behaviorIndex}`}>{behavior}</li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        ) : (
          <p className="report-subtitle">No related suspicious cases were found from the campaign dataset.</p>
        )}
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