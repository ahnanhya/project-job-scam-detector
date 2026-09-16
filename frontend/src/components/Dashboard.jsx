import React from "react";

function Dashboard() {

  return (
    <div className="dashboard-page">

      <div className="page-heading">

        <span className="small-label">
          SAFETY DASHBOARD
        </span>

        <h1>
          Your Job Safety Overview
        </h1>

        <p>
          Track the jobs you've analyzed and suspicious
          campaigns detected.
        </p>

      </div>

      <div className="stats-grid">

        <div className="stat-card">

          <span>🔍</span>

          <h3>
            Jobs Checked
          </h3>

          <strong>
            24
          </strong>

        </div>

        <div className="stat-card">

          <span>🟢</span>

          <h3>
            Safe
          </h3>

          <strong>
            12
          </strong>

        </div>

        <div className="stat-card">

          <span>🟡</span>

          <h3>
            Suspicious
          </h3>

          <strong>
            5
          </strong>

        </div>

        <div className="stat-card">

          <span>🔴</span>

          <h3>
            High Risk
          </h3>

          <strong>
            7
          </strong>

        </div>

      </div>

      <div className="recent-section">

        <h2>
          Recent Checks
        </h2>

        <div className="job-table">

          <div className="job-row header">

            <span>Job</span>
            <span>Risk</span>
            <span>Status</span>

          </div>

          <div className="job-row">

            <span>
              Amazon Work From Home
            </span>

            <span>
              87/100
            </span>

            <span className="high-risk">
              🔴 High Risk
            </span>

          </div>

          <div className="job-row">

            <span>
              TCS Internship
            </span>

            <span>
              12/100
            </span>

            <span className="safe">
              🟢 Safe
            </span>

          </div>

          <div className="job-row">

            <span>
              Data Entry Assistant
            </span>

            <span>
              64/100
            </span>

            <span className="suspicious">
              🟡 Suspicious
            </span>

          </div>

          <div className="job-row">

            <span>
              Remote Back Office
            </span>

            <span>
              91/100
            </span>

            <span className="high-risk">
              🔴 High Risk
            </span>

          </div>

        </div>

      </div>

      <div className="campaign-summary">

        <h2>
          🚨 Active Scam Campaigns
        </h2>

        <div>

          <strong>
            3
          </strong>

          <span>
            campaigns detected
          </span>

        </div>

        <div>

          <strong>
            12
          </strong>

          <span>
            connected reports
          </span>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;