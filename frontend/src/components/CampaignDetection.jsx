import React from "react";

function CampaignDetection({ onNext, campaignAnalysis, campaign_analysis }) {
  const analysis = campaignAnalysis || campaign_analysis || {};
  const campaignDetected = Boolean(analysis.campaign_detected);
  const confidence = Number(analysis.campaign_confidence ?? 0);
  const connectedCases = Number(
    analysis.connected_cases ??
      (Array.isArray(analysis.matches) ? analysis.matches.length : 0)
  );
  const sharedEntities = Array.isArray(analysis.shared_entities)
    ? analysis.shared_entities
    : [];
  const sharedBehavior = Array.isArray(analysis.shared_behavior)
    ? analysis.shared_behavior
    : [];
  const matches = Array.isArray(analysis.matches) ? analysis.matches : [];

  const statusText = campaignDetected
    ? "Potential Campaign Connection"
    : "No Strong Campaign Connection";

  const statusMessage =
    analysis.message ||
    (campaignDetected
      ? "Potential connection to existing scam campaigns found."
      : "No strong campaign connection was found in the historical scam dataset.");

  const pageStyle = {
    maxWidth: "1100px",
    margin: "30px auto",
    padding: "0 20px 40px",
    color: "#111827",
    fontFamily: "Arial, Helvetica, sans-serif"
  };

  const headingStyle = {
    marginBottom: "24px",
    padding: "28px 30px",
    background: "linear-gradient(135deg, #0f172a 0%, #111827 100%)",
    borderRadius: "22px",
    boxShadow: "0 18px 42px rgba(15, 23, 42, 0.12)",
    color: "#f8fafc"
  };

  const labelStyle = {
    display: "inline-block",
    padding: "7px 12px",
    background: "rgba(148, 163, 184, 0.18)",
    borderRadius: "999px",
    fontSize: "12px",
    fontWeight: 700,
    letterSpacing: "1.4px",
    marginBottom: "12px"
  };

  const boxStyle = {
    background: "#ffffff",
    border: "1px solid #e5e7eb",
    borderRadius: "20px",
    boxShadow: "0 10px 28px rgba(15, 23, 42, 0.06)",
    padding: "22px 20px"
  };

  const metricGridStyle = {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: "16px",
    marginBottom: "24px"
  };

  const metricCardStyle = {
    ...boxStyle,
    minHeight: "150px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center"
  };

  return (
    <div style={pageStyle}>
      <div style={headingStyle}>
        <div style={labelStyle}>THREAT INTELLIGENCE</div>
        <h1 style={{ margin: "0 0 10px", fontSize: "2.2rem" }}>
          {campaignDetected ? "🚨" : "🛡️"} {statusText}
        </h1>
        <p style={{ margin: 0, color: "#cbd5e1", lineHeight: 1.6 }}>
          {statusMessage}
        </p>
      </div>

      <div style={metricGridStyle}>
        <div style={{ ...metricCardStyle, borderColor: campaignDetected ? "#fecaca" : "#bbf7d0" }}>
          <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.4px", color: "#64748b", marginBottom: "10px" }}>
            CAMPAIGN STATUS
          </div>
          <div style={{ fontSize: "1.8rem", fontWeight: 800, color: campaignDetected ? "#b91c1c" : "#15803d" }}>
            {campaignDetected ? "ACTIVE" : "CLEAR"}
          </div>
          <div style={{ marginTop: "8px", color: "#475569" }}>
            {campaignDetected ? "Historical link detected" : "No strong pattern found"}
          </div>
        </div>

        <div style={metricCardStyle}>
          <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.4px", color: "#64748b", marginBottom: "10px" }}>
            CONFIDENCE SCORE
          </div>
          <div style={{ fontSize: "2.4rem", fontWeight: 800, color: "#111827" }}>
            {confidence}
            <span style={{ fontSize: "1.2rem", color: "#64748b" }}> / 100</span>
          </div>
          <div style={{ marginTop: "8px", color: "#475569" }}>
            Based on matching infrastructure and behavior
          </div>
        </div>

        <div style={metricCardStyle}>
          <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.4px", color: "#64748b", marginBottom: "10px" }}>
            CONNECTED CASES
          </div>
          <div style={{ fontSize: "2.4rem", fontWeight: 800, color: "#111827" }}>
            {connectedCases}
          </div>
          <div style={{ marginTop: "8px", color: "#475569" }}>
            Historical scam cases linked to this pattern
          </div>
        </div>
      </div>

      <div style={{ ...boxStyle, marginBottom: "24px" }}>
        <h2 style={{ margin: "0 0 18px", fontSize: "1.5rem" }}>Shared entities</h2>

        {sharedEntities.length > 0 ? (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "14px" }}>
            {sharedEntities.map((item, index) => {
              const type = item?.type || "Entity";
              const value = item?.value || "Unknown";
              const isEmail = String(type).toLowerCase() === "email";
              const isLink = isEmail && value.includes("@");

              return (
                <div
                  key={`${type}-${value}-${index}`}
                  style={{
                    background: "#f8fafc",
                    border: "1px solid #e2e8f0",
                    borderRadius: "16px",
                    padding: "16px",
                    minHeight: "120px"
                  }}
                >
                  <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.2px", color: "#64748b", marginBottom: "10px" }}>
                    {String(type).toUpperCase()}
                  </div>

                  {isLink ? (
                    <a
                      href={`mailto:${value}`}
                      style={{ color: "#1d4ed8", fontWeight: 700, wordBreak: "break-word" }}
                    >
                      {value}
                    </a>
                  ) : (
                    <div style={{ fontWeight: 700, wordBreak: "break-word" }}>{value}</div>
                  )}

                  {item?.reason ? (
                    <div style={{ marginTop: "10px", color: "#475569", fontSize: "0.9rem", lineHeight: 1.5 }}>
                      {item.reason}
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        ) : (
          <p style={{ margin: 0, color: "#475569", lineHeight: 1.6 }}>
            No shared phone, email, or payment identifiers were found in the campaign analysis.
          </p>
        )}
      </div>

      <div style={{ ...boxStyle, marginBottom: "24px" }}>
        <h2 style={{ margin: "0 0 18px", fontSize: "1.5rem" }}>Shared scam behaviors</h2>

        {sharedBehavior.length > 0 ? (
          <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
            {sharedBehavior.map((behavior, index) => (
              <span
                key={`${behavior}-${index}`}
                style={{
                  display: "inline-block",
                  padding: "9px 14px",
                  borderRadius: "999px",
                  background: "#eff6ff",
                  border: "1px solid #bfdbfe",
                  color: "#1d4ed8",
                  fontWeight: 700,
                  fontSize: "0.86rem"
                }}
              >
                {behavior}
              </span>
            ))}
          </div>
        ) : (
          <p style={{ margin: 0, color: "#475569", lineHeight: 1.6 }}>
            No repeated scam behavior pattern was detected in the current campaign match.
          </p>
        )}
      </div>

      <div style={{ ...boxStyle }}>
        <h2 style={{ margin: "0 0 18px", fontSize: "1.5rem" }}>Connected scam cases</h2>

        {matches.length > 0 ? (
          <div style={{ display: "grid", gap: "18px" }}>
            {matches.map((match, index) => {
              const historicalCase = match?.historical_case || {};
              const title = historicalCase.title || "Historical scam case";
              const company = historicalCase.company || "Unknown company";
              const score = Number(match?.campaign_score ?? 0);
              const similarity = Number(match?.similarity ?? 0);
              const caseSharedEntities = Array.isArray(match?.shared_entities)
                ? match.shared_entities
                : [];
              const caseSharedBehavior = Array.isArray(match?.shared_behavior)
                ? match.shared_behavior
                : [];

              return (
                <div
                  key={`${title}-${index}`}
                  style={{
                    border: "1px solid #e5e7eb",
                    borderRadius: "18px",
                    background: "#f8fafc",
                    padding: "18px"
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", gap: "12px", flexWrap: "wrap", marginBottom: "12px" }}>
                    <div>
                      <h3 style={{ margin: 0, fontSize: "1.2rem" }}>{title}</h3>
                      <div style={{ color: "#64748b", marginTop: "4px" }}>{company}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ color: "#64748b", fontSize: "12px", fontWeight: 700, letterSpacing: "1.2px" }}>CAMPAIGN SCORE</div>
                      <div style={{ fontSize: "1.5rem", fontWeight: 800, color: "#111827" }}>{score}</div>
                    </div>
                  </div>

                  <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: "12px", marginBottom: "14px" }}>
                    <div style={{ background: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "12px", padding: "12px" }}>
                      <div style={{ color: "#64748b", fontSize: "12px", fontWeight: 700, letterSpacing: "1.1px" }}>SIMILARITY</div>
                      <div style={{ fontWeight: 800, marginTop: "8px" }}>{similarity}%</div>
                    </div>

                    <div style={{ background: "#ffffff", border: "1px solid #e2e8f0", borderRadius: "12px", padding: "12px" }}>
                      <div style={{ color: "#64748b", fontSize: "12px", fontWeight: 700, letterSpacing: "1.1px" }}>SHARED ITEMS</div>
                      <div style={{ fontWeight: 800, marginTop: "8px" }}>{caseSharedEntities.length}</div>
                    </div>
                  </div>

                  {caseSharedEntities.length > 0 ? (
                    <div style={{ marginBottom: "12px" }}>
                      <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.1px", color: "#64748b", marginBottom: "8px" }}>
                        SHARED ENTITIES
                      </div>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                        {caseSharedEntities.map((entity, entityIndex) => (
                          <span
                            key={`${entity?.type || "entity"}-${entity?.value || "unknown"}-${entityIndex}`}
                            style={{
                              display: "inline-flex",
                              padding: "7px 10px",
                              borderRadius: "10px",
                              background: "#fff7ed",
                              border: "1px solid #fdba74",
                              color: "#9a5b00",
                              fontWeight: 700,
                              fontSize: "0.8rem"
                            }}
                          >
                            {entity?.type || "Entity"}: {entity?.value || "Unknown"}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : null}

                  {caseSharedBehavior.length > 0 ? (
                    <div>
                      <div style={{ fontSize: "12px", fontWeight: 700, letterSpacing: "1.1px", color: "#64748b", marginBottom: "8px" }}>
                        SHARED BEHAVIOR
                      </div>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
                        {caseSharedBehavior.map((behavior, behaviorIndex) => (
                          <span
                            key={`${behavior}-${behaviorIndex}`}
                            style={{
                              display: "inline-block",
                              padding: "7px 10px",
                              borderRadius: "999px",
                              background: "#eff6ff",
                              border: "1px solid #bfdbfe",
                              color: "#1d4ed8",
                              fontWeight: 700,
                              fontSize: "0.8rem"
                            }}
                          >
                            {behavior}
                          </span>
                        ))}
                      </div>
                    </div>
                  ) : null}
                </div>
              );
            })}
          </div>
        ) : (
          <p style={{ margin: 0, color: "#475569", lineHeight: 1.6 }}>
            No connected historical scam cases were found for this job posting.
          </p>
        )}
      </div>

      <button
        className="primary-button"
        style={{
          display: "block",
          width: "100%",
          marginTop: "24px",
          borderRadius: "14px",
          padding: "16px 18px",
          fontWeight: 700,
          fontSize: "1rem",
          background: "#111827",
          border: "none",
          color: "#ffffff"
        }}
        onClick={onNext}
      >
        🛡️ View Safety Warning
      </button>
    </div>
  );
}

export default CampaignDetection;