import React, { useEffect, useState } from "react";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/dashboard");

        if (!response.ok) {
          throw new Error("Dashboard data unavailable");
        }

        const result = await response.json();
        setDashboard(result.data || {});
      } catch (fetchError) {
        console.error("Dashboard fetch error:", fetchError);
        setError("Dashboard data unavailable. Start the backend to load the prototype intelligence dataset.");
      }
    };

    loadDashboardData();
  }, []);

  const data = dashboard || {};
  const metrics = [
    { label: "Total analyzed jobs", value: data.total_analyzed_jobs ?? 0, icon: "🔍" },
    { label: "Suspicious jobs", value: data.suspicious_jobs ?? 0, icon: "⚠️" },
    { label: "High-risk jobs", value: data.high_risk_jobs ?? 0, icon: "🔴" },
    { label: "Potential scam campaigns", value: data.potential_campaigns ?? 0, icon: "🧭" }
  ];

  const sharedIndicators = data.shared_indicators || {};
  const phoneIndicators = Array.isArray(sharedIndicators.phones) ? sharedIndicators.phones : [];
  const paymentIndicators = Array.isArray(sharedIndicators.payment_ids) ? sharedIndicators.payment_ids : [];
  const emailIndicators = Array.isArray(sharedIndicators.emails) ? sharedIndicators.emails : [];
  const domainIndicators = Array.isArray(sharedIndicators.domains) ? sharedIndicators.domains : [];
  const behaviorIndicators = Array.isArray(sharedIndicators.behavioral_patterns) ? sharedIndicators.behavioral_patterns : [];
  const recentCases = Array.isArray(data.prototype_cases) ? data.prototype_cases : [];

  return (
    <div className="dashboard-page">
      <div className="page-heading">
        <span className="small-label">PROTOTYPE DASHBOARD</span>
        <h1>Job Scam Intelligence Overview</h1>
        <p>
          Monitoring suspicious recruitment patterns from the current local prototype dataset and
          submitted job analyses.
        </p>
      </div>

      {error ? (
        <div className="empty-state">
          <h3>No analysis history available</h3>
          <p>{error}</p>
        </div>
      ) : (
        <>
          <div className="stats-grid">
            {metrics.map((metric) => (
              <div className="stat-card" key={metric.label}>
                <span className="stat-icon" aria-hidden="true">{metric.icon}</span>
                <h3>{metric.label}</h3>
                <strong>{metric.value}</strong>
              </div>
            ))}
          </div>

          <div className="report-section dashboard-section">
            <h2>Potential Campaign Connections</h2>

            <div className="campaign-alert compact-alert">
              <strong>Prototype campaign pattern</strong>
              <p>
                This dashboard highlights suspicious links between job postings. It does not confirm that
                the same actor or criminal organization created them.
              </p>
            </div>

            <div className="shared-grid dashboard-shared-grid">
              <div>
                <strong>Connected suspicious cases</strong>
                <span>{data.connected_suspicious_cases ?? 0}</span>
              </div>

              <div>
                <strong>Potential campaign groups</strong>
                <span>{data.potential_campaigns ?? 0}</span>
              </div>

              <div>
                <strong>Shared phone numbers</strong>
                <span>{phoneIndicators.length}</span>
              </div>

              <div>
                <strong>Shared payment IDs</strong>
                <span>{paymentIndicators.length}</span>
              </div>
            </div>
          </div>

          <div className="report-section dashboard-section">
            <h2>Shared Indicators</h2>

            <div className="shared-grid dashboard-indicator-grid">
              <div>
                <strong>Phone numbers</strong>
                {phoneIndicators.length ? (
                  <span>{phoneIndicators.join(", ")}</span>
                ) : (
                  <span>No shared phone indicators available</span>
                )}
              </div>

              <div>
                <strong>Payment IDs</strong>
                {paymentIndicators.length ? (
                  <span>{paymentIndicators.join(", ")}</span>
                ) : (
                  <span>No shared payment identifiers available</span>
                )}
              </div>

              <div>
                <strong>Emails / domains</strong>
                {emailIndicators.length || domainIndicators.length ? (
                  <span>{[...emailIndicators, ...domainIndicators].slice(0, 4).join(", ")}</span>
                ) : (
                  <span>No shared email/domain indicators available</span>
                )}
              </div>

              <div>
                <strong>Behavior patterns</strong>
                {behaviorIndicators.length ? (
                  <span>{behaviorIndicators.slice(0, 3).join(" • ")}</span>
                ) : (
                  <span>No common behavioral pattern detected</span>
                )}
              </div>
            </div>
          </div>

          <div className="recent-section">
            <h2>Prototype Threat Intelligence</h2>

            {recentCases.length ? (
              <div className="job-table">
                <div className="job-row header">
                  <span>Job</span>
                  <span>Risk</span>
                  <span>Campaign link</span>
                </div>

                {recentCases.map((job) => (
                  <div className="job-row" key={job.id || job.title}>
                    <span>
                      <strong>{job.title}</strong>
                      <small>
                        {job.company} • {job.location}
                      </small>
                    </span>

                    <span className={job.risk === "High Risk" ? "high-risk" : "suspicious"}>
                      {job.risk || "Suspicious"}
                    </span>

                    <span>
                      {job.campaign_connection || "Prototype dataset"}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <h3>No analyzed jobs yet</h3>
                <p>Run a job analysis to start building your local analysis history.</p>
              </div>
            )}
          </div>

          <div className="report-section dashboard-section">
            <h2>System Status</h2>
            <p className="dashboard-note">
              Analysis is based on the current prototype dataset and submitted job analyses. The dashboard
              highlights potential campaign links and shared indicators, not confirmed criminal activity.
            </p>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard;