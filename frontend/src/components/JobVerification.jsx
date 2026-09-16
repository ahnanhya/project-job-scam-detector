import React, { useState } from "react";

function JobVerification({ onBack }) {

  const [text, setText] = useState("");

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const verifyJob = async () => {

    if (!text.trim()) {

      alert(
        "Please enter the job or offer details."
      );

      return;
    }

    setLoading(true);
    setResult(null);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/verify-job",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            text: text
          })
        }
      );

      const data =
        await response.json();

      if (data.status !== "success") {

        alert(
          data.message ||
          "Verification failed."
        );

        return;
      }

      setResult(data);

    } catch (error) {

      console.error(
        "Verification Error:",
        error
      );

      alert(
        "Unable to connect to backend."
      );

    } finally {

      setLoading(false);
    }
  };


  return (

    <div className="page-container">

      <div className="page-heading">

        <span className="small-label">
          REAL JOB VERIFICATION
        </span>

        <h1>
          Verify this job against existing listings
        </h1>

        <p>
          Our system searches available job listings
          and compares them with the submitted offer.
        </p>

      </div>


      <div className="analysis-input-card">

        <textarea
          value={text}
          onChange={(e) =>
            setText(e.target.value)
          }
          placeholder={
            "Paste a job advertisement, message or offer letter text here..."
          }
        />

        <button
          className="primary-button"
          onClick={verifyJob}
          disabled={loading}
        >

          {loading
            ? "🔎 Searching..."
            : "🔍 Verify Against Real Jobs"}

        </button>

      </div>


      {result && (

        <div className="verification-results">

          <div className="risk-card">

            <h2>
              Extracted Job
            </h2>

            <p>
              <strong>
                Job:
              </strong>{" "}
              {result.submitted_job.job_title ||
                "Not detected"}
            </p>

            <p>
              <strong>
                Company:
              </strong>{" "}
              {result.submitted_job.company ||
                "Not detected"}
            </p>

            <p>
              <strong>
                Location:
              </strong>{" "}
              {result.submitted_job.location ||
                "Not detected"}
            </p>

          </div>


          <div className="signals-card">

            <h2>
              Verification Result
            </h2>

            <h3>
              {result.job_search.match_status}
            </h3>

            <p>
              Listings found:
              {" "}
              {result.job_search.total_found}
            </p>

          </div>


          <div className="signals-card">

            <h2>
              Similar Existing Jobs
            </h2>

            {result.matching_jobs.length === 0 ? (

              <p>
                No matching listings were found.
              </p>

            ) : (

              result.matching_jobs.map(
                (job, index) => (

                  <div
                    className="signal-item"
                    key={index}
                  >

                    <div>

                      <strong>
                        {job.title}
                      </strong>

                      <p>
                        {job.company}
                      </p>

                      <p>
                        {job.location}
                      </p>

                      <p>
                        Match:
                        {" "}
                        {job.match_score}%
                      </p>

                      {job.link && (

                        <a
                          href={job.link}
                          target="_blank"
                          rel="noreferrer"
                        >
                          View Listing
                        </a>

                      )}

                    </div>

                  </div>

                )
              )

            )}

          </div>


          <div className="risk-card">

            <h2>
              Scam Analysis
            </h2>

            <div className="risk-score">

              {result.scam_analysis.risk_score}

              <span>
                /100
              </span>

            </div>

            <div className="risk-level">

              {result.scam_analysis.risk}

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default JobVerification;