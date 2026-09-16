SCAM_CAMPAIGNS = [
    {
        "id": "scam-campaign-01",
        "title": "Remote Data Entry Assistant",
        "company": "FlexiWorks Global",
        "location": "Remote",
        "salary": "₹15,000 - ₹25,000 / month",
        "snippet": "Hiring remote workers for online data entry tasks. Must pay a one-time registration fee of ₹299 through UPI. Contact +91 98765 43210 or flexiworks.jobs@outlook.com. WhatsApp only. Initial onboarding via payment ID flexiworks.pay@oksbi.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/flexiworks-job",
        "type": "Contract",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-02",
        "title": "Customer Support Executive",
        "company": "Nexa Careers",
        "location": "Remote",
        "salary": "₹18,000 - ₹30,000 / month",
        "snippet": "Immediate openings for work-from-home customer support. Selected candidates are expected to make a refundable deposit of ₹499. Contact +91 98765 43210, support@nexacareers.co.in, and UPI ID flexiworks.pay@oksbi. Join through WhatsApp messaging.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/nexa-career",
        "type": "Remote",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-03",
        "title": "Social Media Evaluator",
        "company": "MetroReach Jobs",
        "location": "Remote",
        "salary": "₹12,000 - ₹22,000 / month",
        "snippet": "Part-time social media evaluator opportunity. Register with your mobile number and pay a small activation fee of ₹350. Reach us on +91 98765 43210 or hr@metroreachjobs.com. Payment reference: flexiworks.pay@oksbi.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/metroreach-evaluator",
        "type": "Part-time",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-04",
        "title": "Online Form Filling Job",
        "company": "SkillBridge Hiring",
        "location": "Remote",
        "salary": "₹20,000 - ₹35,000 / month",
        "snippet": "No experience required. Submit your details to skillbridge.hiring@gmail.com and pay ₹650 for the training kit. Contact +91 98765 43210. UPI payment ID: flexiworks.pay@oksbi. Fast onboarding through WhatsApp.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/skillbridge-job",
        "type": "Freelance",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-05",
        "title": "Virtual Assistant - Work from Home",
        "company": "PrimeAssist Global",
        "location": "Remote",
        "salary": "₹16,000 - ₹28,000 / month",
        "snippet": "Need remote virtual assistants for basic admin work. Paid onboarding includes a ₹599 account activation charge. Send resume to primeassist.hr@gmail.com or WhatsApp +91 98765 43210. Payment to flexiworks.pay@oksbi.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/primeassist-virtual",
        "type": "Remote",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-06",
        "title": "Work From Home Typist",
        "company": "Allied Global Services",
        "location": "Remote",
        "salary": "₹14,000 - ₹24,000 / month",
        "snippet": "Urgent vacancies for home-based typist. Registration is quick and requires a ₹300 joining fee. Contact +91 98765 43210 or alliedjobs.hiring@outlook.com. Payment should be sent to UPI ID flexiworks.pay@oksbi. We will send the job letter by WhatsApp.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/allied-typist",
        "type": "Remote",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-07",
        "title": "Data Processing Operator",
        "company": "Zenith Hiring Desk",
        "location": "Remote",
        "salary": "₹17,000 - ₹26,000 / month",
        "snippet": "We are hiring online data processing operators. You have to pay ₹450 as verification fee before starting. Call +91 98765 43210 or email hiring@zenithdesk.in. Payment ID: flexiworks.pay@oksbi. Initial onboarding will be done on WhatsApp.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/zenith-processing",
        "type": "Contract",
        "updated": "2026-09-16"
    },
    {
        "id": "scam-campaign-08",
        "title": "Remote Customer Service Agent",
        "company": "BrightPath Careers",
        "location": "Remote",
        "salary": "₹19,000 - ₹32,000 / month",
        "snippet": "BrightPath Careers is hiring remote customer service agents with no prior experience required. Pay a refundable security fee of ₹500 before activation. Contact +91 98765 43210, careers@brightpathjobs.com, or WhatsApp. UPI payment ID flexiworks.pay@oksbi.",
        "source": "local-scam-campaign-db",
        "link": "https://example.invalid/brightpath-agent",
        "type": "Remote",
        "updated": "2026-09-16"
    }
]


def get_local_campaign_jobs():
    return [
        {
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "salary": job["salary"],
            "snippet": job["snippet"],
            "source": job["source"],
            "link": job["link"],
            "type": job["type"],
            "updated": job["updated"]
        }
        for job in SCAM_CAMPAIGNS
    ]