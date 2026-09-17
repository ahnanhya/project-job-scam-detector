# 🛡️ Job Scam Detector

> **Intelligent Detection of Fraudulent Recruitment & Emerging Scam Campaigns**

Job Scam Detector is a full-stack prototype designed to help job seekers identify suspicious recruitment offers **before they share sensitive information or make payments**.

Unlike a traditional job scam checker that only asks *“Is this job suspicious?”*, this project also investigates **whether a suspicious job is connected to other scam activity**.

The system analyzes recruitment content, extracts important indicators, evaluates suspicious behaviour, generates a risk score, and compares the submitted job against known suspicious cases to identify potential **scam campaigns**.

---

## 🚨 Problem Statement

Online job scams are becoming increasingly sophisticated.

Scammers may:

* Post fake job advertisements
* Impersonate legitimate companies or recruiters
* Promise unusually attractive salaries
* Demand registration or onboarding fees
* Move recruitment conversations to WhatsApp or other messaging platforms
* Request identity documents or sensitive information
* Create multiple advertisements using different company or job names
* Reuse the same phone numbers, email addresses, payment identifiers, domains, or recruitment patterns

A conventional scam detector may analyze each job independently.

This creates a major limitation:

```text
Job A → Suspicious

Job B → Suspicious

Job C → Suspicious
```

The system may never recognize that:

```text
Job A ─┐
       ├── Shared Indicators ──→ Potential Scam Campaign
Job B ─┤
       │
Job C ─┘
```

### The goal of Job Scam Detector

Move from:

> **Individual Job Detection**

to:

> **Campaign-Level Scam Intelligence**

---

# 🎯 Key Features

### 🔍 Job Scam Analysis

Analyzes submitted recruitment text and identifies suspicious characteristics.

The system produces:

* Risk score
* Risk level
* Suspicious signals
* Explanations
* Extracted entities
* Scam DNA indicators

---

### 🧠 Scam Signal Detection

The detector looks for suspicious recruitment patterns such as:

* Registration fees
* Activation fees
* Advance payments
* Urgent hiring
* Immediate joining
* Suspicious recruitment channels
* Unusual onboarding processes
* Requests for sensitive information
* Potential impersonation indicators

---

### 🧬 Scam DNA

The application represents recurring characteristics of suspicious recruitment attempts as a **Scam DNA profile**.

This helps describe *how* a recruitment scam behaves instead of relying only on a single classification result.

Example:

```text
Scam DNA

├── Urgent Hiring
├── Upfront Payment
├── WhatsApp Recruitment
├── Remote Onboarding
└── Sensitive Information Request
```

---

### 🕸️ Campaign Detection

The most important differentiating feature.

The system compares a submitted job with available suspicious cases to identify potential relationships.

Possible shared indicators include:

```text
Phone Number
Email Address
Domain
Payment Identifier
Recruitment Behaviour
Scam Patterns
```

Example:

```text
Job A
  │
  ├── Phone: +91 XXXXX XXXXX
  │
  └──────────────┐
                 │
Job B            │
  │              │
  ├── Same Phone ┘
  │
  └── Similar Recruitment Behaviour
          │
          ▼
   Potential Campaign
```

---

### 🔗 Shared Indicator Analysis

The system can identify recurring indicators across suspicious cases.

These include:

* Phone numbers
* Email addresses
* Domains
* Payment-related identifiers
* Behavioural patterns

A shared indicator is treated as **supporting evidence**, not automatic proof that two advertisements belong to the same person or organization.

---

### 🛡️ Job Verification

The application provides a separate job verification workflow for checking recruitment information against available listings.

---

### 📊 Intelligence Dashboard

The dashboard provides an overview of analyzed cases.

It can display:

* Total analyzed jobs
* Suspicious jobs
* High-risk jobs
* Potential campaigns
* Connected suspicious cases
* Shared phone numbers
* Shared emails
* Shared domains
* Behavioural patterns
* Prototype campaign cases

---

### 🌗 Light & Dark Mode

The frontend includes a persistent light/dark theme.

The selected theme is stored locally so the interface can remember the user's preference.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │    React 19 + Vite   │
                         └──────────┬───────────┘
                                    │
                              HTTP / JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │       Python         │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐       ┌──────────────┐       ┌──────────────┐
      │ Scam        │       │ Campaign     │       │ Job          │
      │ Detector    │       │ Detector     │       │ Verification │
      └──────┬──────┘       └──────┬───────┘       └──────────────┘
             │                      │
             ▼                      ▼
      Risk + Signals        Shared Entities
      + Explanations        + Behaviour
             │                      │
             └───────────┬──────────┘
                         ▼
                ┌──────────────────┐
                │ Campaign Cases   │
                │ SQL / Local Data │
                └──────────────────┘
```

---

# 🔄 Application Workflow

```text
User submits job posting
          │
          ▼
   Text preprocessing
          │
          ▼
   Scam signal analysis
          │
          ▼
   Entity extraction
          │
          ▼
      Risk scoring
          │
          ▼
      Scam DNA
          │
          ▼
   Campaign comparison
          │
          ▼
 Shared indicators detected?
          │
       ┌──┴──┐
      YES    NO
       │      │
       ▼      ▼
 Connected   Individual
   Cases      Analysis
       │      │
       └──┬───┘
          ▼
   Detection Report
          │
          ▼
       Dashboard
```

---

# 🧰 Technology Stack

## Frontend

### React 19

Used to build the interactive user interface using reusable components.

### Vite

Used as the frontend development server and build tool.

### JavaScript / JSX

Used for application logic and React components.

### HTML / CSS

Used for page structure, layout, styling, and responsive interface design.

---

## Backend

### Python

Used for the core backend and scam-detection logic.

### FastAPI

Used to build the REST API connecting the frontend with the detection system.

### Uvicorn

Used as the ASGI server for running the FastAPI application.

### Requests

Used for HTTP requests where required by backend services.

### python-dotenv

Used for environment-variable configuration.

### python-multipart

Provides multipart/form-data support.

---

## Database

The project includes SQL schema and sample data for storing suspicious campaign/job information.

Stored information can include:

```text
Job ID
Job Title
Company
Location
Salary
Job Description
Contact Phone
Contact Email
Payment ID
Source
Created Timestamp
```

---

# 🧠 Detection Methodology

The detection system is designed around multiple signals rather than relying on a single keyword or indicator.

## 1. Recruitment Text Analysis

The submitted job description is analyzed for suspicious recruitment characteristics.

For example:

```text
"Immediate joining.
Work from home.
Pay ₹499 registration fee
to activate your employee account."
```

Possible signals:

```text
✓ Urgent hiring
✓ Work-from-home recruitment
✓ Registration fee
✓ Payment request
```

These signals contribute to the overall risk analysis.

---

# 2. Risk Scoring

The system generates a numerical risk score.

The score is accompanied by:

* Risk level
* Signals
* Explanations
* Extracted information

Conceptually:

```text
                    Job Posting
                         │
                         ▼
                 Detect Signals
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Payment         Urgency       Contact
       Request         Language      Pattern
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                   Risk Analysis
                         │
                         ▼
                    Risk Score
```

The risk score is a **screening indicator**, not proof that a company or individual is fraudulent.

---

# 3. Entity Extraction

Important entities are extracted from recruitment content.

```text
Job Posting
     │
     ├── Phone Number
     │
     ├── Email Address
     │
     ├── Domain
     │
     ├── Payment Identifier
     │
     ├── Company Information
     │
     └── Recruiter Information
```

These entities become useful when comparing multiple cases.

---

# 4. Campaign Detection

After analyzing the individual job, the system compares its extracted information and behavioural characteristics with available suspicious cases.

For example:

```text
Submitted Job
      │
      ├── Phone Number ───────────┐
      │                           │
      ├── Email ──────────────────┤
      │                           │
      ├── Payment ID ─────────────┤
      │                           ▼
      ├── Domain ───────────→ Existing Cases
      │                           │
      └── Behaviour ──────────────┘
                                  │
                                  ▼
                       Potential Campaign
```

The campaign analysis can return:

* Campaign detected
* Campaign confidence
* Connected cases
* Shared entities
* Shared behaviour
* Matching cases

---

# 5. Behavioural Analysis

Direct identifiers can change.

For example, a scammer might change their:

```text
Phone number
Email
Company name
Job title
```

while keeping similar recruitment behaviour.

Therefore, the system can also consider patterns such as:

* Urgent hiring
* Advance payment
* Activation fees
* WhatsApp-only recruitment
* Remote-only onboarding

This provides an additional layer of campaign intelligence.

---

# 🧬 Campaign Intelligence Concept

The central idea of the project can be represented as:

```text
                   ┌───────────────┐
                   │    Job A      │
                   └───────┬───────┘
                           │
                    Shared Phone
                           │
                           ▼
                   ┌───────────────┐
                   │    Job B      │
                   └───────┬───────┘
                           │
                    Similar Behaviour
                           │
                           ▼
                   ┌───────────────┐
                   │    Job C      │
                   └───────┬───────┘
                           │
                    Shared Payment ID
                           │
                           ▼
                ┌──────────────────────┐
                │ Potential Scam       │
                │ Campaign Cluster     │
                └──────────────────────┘
```

This approach helps move the application from:

**Job-level detection → Relationship-level intelligence**

---

# 📁 Project Structure

```text
project-job-scam-detector/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── test_job_api.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── routes/
│   │   ├── job_verification.py
│   │   ├── analyze.py
│   │   ├── campaigns.py
│   │   └── reports.py
│   │
│   └── services/
│       ├── scam_detector.py
│       ├── campaign_detector.py
│       ├── scam_campaigns.py
│       ├── job_extractor.py
│       ├── job_matcher.py
│       ├── job_search.py
│       ├── scam_dna.py
│       └── similarity.py
│
├── database/
│   ├── schema.sql
│   └── sample_data.sql
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   │
│   └── src/
│       ├── App.jsx
│       │
│       └── components/
│           ├── Navbar.jsx
│           ├── Home.jsx
│           ├── AnalyzeJob.jsx
│           ├── Analyzing.jsx
│           ├── DetectionReport.jsx
│           ├── Dashboard.jsx
│           └── JobVerification.jsx
│
└── README.md
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /
```

Returns the current API status.

Example response:

```json
{
  "message": "Job Scam Detector API is running",
  "status": "success"
}
```

---

## Analyze Job

```http
POST /analyze
Content-Type: application/json
```

Example request:

```json
{
  "text": "Work from home job. Immediate joining. Pay a registration fee to activate your employee account."
}
```

The API returns:

* Scam analysis
* Risk score
* Risk level
* Signals
* Explanations
* Extracted entities
* Scam DNA
* Campaign analysis

---

## Dashboard

```http
GET /dashboard
```

Returns dashboard information including:

* Total analyzed jobs
* Suspicious jobs
* High-risk jobs
* Potential campaigns
* Connected suspicious cases
* Shared indicators
* Prototype campaign cases

---

## Job Verification

The backend also provides a job-verification route used by the frontend's verification workflow.

---

# 🚀 Getting Started

## Prerequisites

Make sure the following are installed:

* Python 3.10+
* Node.js
* npm
* SQL database if using the database-backed workflow

---

## 1. Clone the Repository

```bash
git clone https://github.com/ahnanhya/project-job-scam-detector.git

cd project-job-scam-detector
```

---

# 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 3. Frontend Setup

Open another terminal.

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will display the local frontend URL in the terminal.

---

# 4. Database Setup

SQL files are available inside:

```text
database/
├── schema.sql
└── sample_data.sql
```

Run:

```text
schema.sql
```

first, followed by:

```text
sample_data.sql
```

when using the database-backed campaign dataset.

The campaign schema contains fields such as:

```text
id
title
company
location
salary
snippet
contact_phone
contact_email
payment_id
source
created_at
```

---

# 🧪 Testing

A lightweight API test script is included:

```text
backend/test_job_api.py
```

Make sure the FastAPI backend is running before executing tests that communicate with the local API.

---

# 📌 Example Use Case

Imagine a student receives this job advertisement:

```text
URGENT HIRING!!!

Work from home.
Earn ₹50,000 per month.
No interview required.

Selected candidates must pay
₹999 as a registration fee.

Contact recruiter through WhatsApp.
```

The system can identify signals such as:

```text
⚠ Urgent hiring
⚠ Unrealistic earning claim
⚠ No interview
⚠ Registration fee
⚠ WhatsApp recruitment
```

The application then generates a risk assessment.

If the extracted contact information or behaviour matches existing suspicious cases:

```text
Campaign Connection Detected

Connected Cases: 4

Shared Indicators:
• Phone number
• Payment identifier
• Recruitment behaviour
```

The user therefore receives more context than simply:

```text
SCAM / NOT SCAM
```

---

# ⚠️ Prototype Limitations

This project is currently a prototype.

It should **not** be treated as a definitive fraud-verification service.

Important limitations include:

* A high risk score does not prove that a job is fraudulent.
* A shared phone number or email does not automatically prove that two cases belong to the same operator.
* Campaign connections depend on the available suspicious-case dataset.
* Detection quality depends on the quality and variety of available examples.
* Some modules are currently structured as placeholders for future development.
* The frontend currently communicates with a locally running backend.
* The prototype does not guarantee detection of every type of job scam.

The system should therefore be used as an **early-warning and decision-support tool**.

---

# 🔮 Future Improvements

The project can be extended with:

### 📷 OCR

Analyze:

* Screenshots
* Offer letters
* WhatsApp messages
* Recruitment posters
* Images of job advertisements

---

### 🧠 Semantic Similarity

Use text embeddings to identify advertisements that are semantically similar even when the exact words are different.

Example:

```text
"Registration fee required"

vs.

"Pay onboarding activation charges"
```

The wording is different, but the underlying behaviour may be similar.

---

### 🧩 Unsupervised Campaign Clustering

Automatically group suspicious advertisements into clusters based on:

* Text similarity
* Shared entities
* Behaviour
* Recruitment patterns

---

### 🕸️ Graph-Based Relationship Analysis

Represent relationships as a graph:

```text
Phone
  │
  ├── Job A
  │
  ├── Job B
  │
  └── Job C

Email
  │
  ├── Job B
  └── Job D

Payment ID
  │
  ├── Job A
  └── Job C
```

This can help identify larger scam networks.

---

### 🌐 Company & Domain Verification

Verify:

* Company domains
* Recruiter emails
* Company identity
* Website authenticity
* Domain age and reputation

---

### 🌍 Crowdsourced Scam Intelligence

Allow users to report suspicious recruitment activity and contribute additional cases to the dataset.

---

### 🧩 Browser Extension

A future browser extension could allow users to analyze job advertisements directly while browsing job platforms.

---

### 💬 Messaging Platform Assistant

Future versions could provide verification assistance for recruitment messages received through platforms such as WhatsApp or Telegram.

---

### 🔔 Continuous Monitoring

Monitor known scam indicators and notify users when new recruitment advertisements appear to reuse known campaign characteristics.

---

# 🔐 Responsible Use

Job Scam Detector is intended to provide **early warnings and supporting evidence**.

Users should independently verify a job opportunity before:

* Sending money
* Sharing identity documents
* Sharing passwords or credentials
* Providing banking information
* Sharing other sensitive personal information

The system's output should not be used as the sole basis for accusing an individual, recruiter, or organization of fraud.

---

# 🎓 Project Context

**Job Scam Detector**

### Intelligent Detection of Fraudulent Recruitment & Emerging Scam Campaigns

Developed as a **BCA Final Year Project**.

The project focuses on combining:

```text
Recruitment Scam Detection
          +
Entity Extraction
          +
Risk Analysis
          +
Behavioural Analysis
          +
Campaign Detection
          +
Relationship Intelligence
```

to provide a more informative approach to job-scam detection.

---

# 👨‍💻 Author

**Ahnanhya**

BCA Final Year

GitHub:
https://github.com/ahnanhya

**Amirtha Varshini**

BCA Final Year

GitHub:
https://github.com/Amirthavarshini10

---

# 📄 License

No open-source license has currently been specified for this repository.

If you intend to distribute the project publicly or accept external contributions, consider adding an appropriate license.

---

## ⭐ Project Vision

> **Don't just detect the scam. Detect the pattern behind it.**

Job Scam Detector aims to evolve from a simple job-classification tool into a **campaign-level recruitment fraud intelligence system** capable of connecting suspicious activities and helping users identify warning signs before financial or personal loss occurs.


