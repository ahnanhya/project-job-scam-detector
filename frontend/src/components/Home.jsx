
import React, { useRef, useState } from "react";

function Home({ onAnalyze }) {

  const [jobText, setJobText] = useState("");
  const screenshotInputRef = useRef(null);
  const offerLetterInputRef = useRef(null);

  const handleAnalyze = () => {

    if (jobText.trim() === "") {
      alert("Please enter a job description first.");
      return;
    }

    onAnalyze(jobText);
  };

  const handleScreenshotUpload = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      alert("Please upload an image file.");
      return;
    }

    /*
      The screenshot is selected here.

      Since your current backend does not have an OCR service,
      we do not pretend to extract text from the image.

      For now, the image is passed through the frontend as a
      selected file and the user is asked to enter/paste the
      text from it for analysis.
    */

    alert(
      `Screenshot "${file.name}" selected.\n\n` +
      `Please paste the job/recruiter text from the screenshot into the text box and click Analyze Job.`
    );

    event.target.value = "";
  };

  const handleOfferLetterUpload = (event) => {

    const file = event.target.files[0];

    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword"
    ];

    if (!allowedTypes.includes(file.type)) {
      alert("Please upload a PDF or Word offer letter.");
      event.target.value = "";
      return;
    }

    /*
      Your current backend does not contain PDF/DOCX text extraction.
      Therefore we don't falsely claim that the offer letter has
      been analyzed.

      The selected document can be connected to a backend
      document-extraction endpoint later.
    */

    alert(
      `Offer letter "${file.name}" selected.\n\n` +
      `Please copy/paste the offer letter text into the text box and click Analyze Job.`
    );

    event.target.value = "";
  };

  return (
    <main className="home-page">

      <section className="hero-section">

        <div className="hero-badge">
          🛡️ AI-POWERED JOB SAFETY
        </div>

        <h1>
          Is this job
          <span> really safe?</span>
        </h1>

        <p className="hero-description">
          Detect suspicious recruitment patterns before
          you lose money or personal information.
        </p>

        <div className="input-card">

          <div className="input-header">

            <div>
              <h3>Check a Job</h3>

              <p>
                Paste a job description or recruiter message
              </p>
            </div>

            <span className="input-icon">
              🔍
            </span>

          </div>

          <textarea
            value={jobText}
            onChange={(e) => setJobText(e.target.value)}
            placeholder="Paste the job description, recruiter message or offer details here..."
          />

          <button
            className="primary-button"
            onClick={handleAnalyze}
          >
            🔍 Analyze Job
          </button>

          <div className="upload-options">

            {/* Screenshot upload */}

            <input
              type="file"
              ref={screenshotInputRef}
              accept="image/*"
              style={{ display: "none" }}
              onChange={handleScreenshotUpload}
            />

            <button
              className="upload-button"
              onClick={() => screenshotInputRef.current.click()}
            >
              📷
              <span>
                Upload Screenshot
              </span>
            </button>


            {/* Offer letter upload */}

            <input
              type="file"
              ref={offerLetterInputRef}
              accept=".pdf,.doc,.docx"
              style={{ display: "none" }}
              onChange={handleOfferLetterUpload}
            />

            <button
              className="upload-button"
              onClick={() => offerLetterInputRef.current.click()}
            >
              📄
              <span>
                Upload Offer Letter
              </span>
            </button>

          </div>

        </div>

      </section>

      <section className="features-section">

        <h2>
          More than just a fake-job checker
        </h2>

        <p>
          JobGuard analyzes behavior, connects suspicious
          cases and identifies emerging scam campaigns.
        </p>

        <div className="feature-grid">

          <div className="feature-card">
            <div className="feature-icon">🎯</div>

            <h3>Risk Detection</h3>

            <p>
              Identify suspicious signals and calculate
              an explainable risk score.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🧬</div>

            <h3>Scam DNA</h3>

            <p>
              Detect recurring scam behaviors instead of
              relying only on keywords.
            </p>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔗</div>

            <h3>Campaign Detection</h3>

            <p>
              Connect seemingly different job scams through
              hidden shared signals.
            </p>
          </div>

        </div>

      </section>

    </main>
  );
}

export default Home;
