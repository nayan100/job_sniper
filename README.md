# 🎯 IoT/Hardware Sniper Bot

An automated lead generation and outreach engine designed to find high-match safety-critical IoT and hardware companies. It identifies technical pain points and drafts consultative outreach emails for VPs of Engineering and CTOs.

---

## 🚀 How It Works
Every morning at 08:00 AM UTC, a GitHub Action wakes up and triggers the **CrewAI Sniper Bot**.

1.  **Lead Sourcing:** Finds 10 mid-sized IoT/Hardware companies in safety-critical sectors (MedTech, Automotive, Industrial).
2.  **Duplicate Prevention:** Uses `processed_companies.txt` to ensure you never apply to the same company twice.
3.  **Technical Analysis:** Hypothesizes deep technical pain points (e.g., MISRA compliance, thermal throttling, multi-core sync) by analyzing product lines.
4.  **Copywriting:** Drafts a highly professional email using your "Technical Audit Map" template.
5.  **Delivery:** Saves the results as a Markdown file (e.g., `daily_hits_2026-05-26.md`) directly in your repository.

---

## 📋 Setup Guide

### 1. API Keys (GitHub Secrets)
Add the following keys to your repository: **Settings > Secrets and variables > Actions > New repository secret**.

*   `GEMINI_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/).
*   `SERPER_API_KEY`: Get from [Serper.dev](https://serper.dev/) (Used for web searching).

### 2. Permissions
Ensure the bot has permission to push files back to your repo:
1.  **Settings > Actions > General**.
2.  Set **Workflow permissions** to **"Read and write permissions"**.
3.  Check **"Allow GitHub Actions to create and approve pull requests"**.

---

## 🛠 Daily Workflow (Your 10-Minute Morning Routine)

1.  **Review Leads:** Open the latest `daily_hits_YYYY-MM-DD.md` file in your repo.
2.  **Fact Check:** Spend 60 seconds verifying the "Pain Point Hypothesis" for each company.
3.  **Send Emails:** Copy the custom email and send it from your Professional Gmail.
4.  **LinkedIn Warm-up:** Click the LinkedIn profiles found by the bot and follow the VPs.

---

## 📈 Next Steps & Refinements

- [ ] **Portfolio Integration:** Link your `asciinema` traces directly in the email templates as they are recorded.
- [ ] **Custom Sectors:** Modify `main.py` to target specific niches (e.g., "AgriTech" or "EV Charging") on different weeks.
- [ ] **CRM Sync:** Integrate with a tool like Notion or Airtable to track response rates and follow-ups.

---

## 🛡 Disclaimer
This bot is a **Force Multiplier**, not a spam machine. It is designed to minimize your research time so you can focus on **Human-to-Human technical relationship building.**
