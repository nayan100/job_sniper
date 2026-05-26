# The "Sniper" Lead Generation Engine (10-a-Day Quality Stack)

This engine is designed to find "Best Match" companies where your AI-native modernization and safety-critical expertise solve a specific, high-value problem. 

---

## The "Best Match" Criteria
Target companies that meet at least two of these:
1.  **Legacy Debt:** They have a product that's been in market for 5+ years (needs modernization).
2.  **Safety-Critical:** They operate in MedTech, Automotive, or Industrial IoT (needs compliance).
3.  **Hiring Signal:** They are hiring for "Embedded Software Engineer" or "Firmware Lead."
4.  **Scale Pain:** They are moving from prototype to "high-scale" deployment.

---

## Daily Workflow: The "Deep Search" Prompts

Run these prompts in sequence to generate your 10 targets for the day.

### Step 1: Find the "High-Match" 10
```bash
gemini "Find 10 mid-sized IoT/Hardware companies (50-300 employees) currently working on [e.g., EV Charging, Wearable MedTech]. Prioritize companies that have recently released a new version of their product or are expanding their engineering team. Provide: Company Name, Website, and their primary Product Line."
```

### Step 2: The "Pain Point" Deep Dive (Run for each of the 10)
```bash
gemini "Analyze [Company Name]'s public engineering blog, recent job postings for 'Firmware Engineer', and product manuals. What are 3 likely technical bottlenecks they face regarding [e.g., MISRA compliance, OTA update reliability, or Unit Test coverage]? Provide a 'Pain Point Hypothesis' for a VP of Engineering."
```

### Step 3: Finding the "Decision Maker"
```bash
gemini "Who is the current VP of Engineering, CTO, or Head of Embedded at [Company Name]? Find their LinkedIn profile and any recent public talks or articles they've written."
```

---

## The "Zero-Cost" Extraction Stack

| Step | Action | Tool |
| :--- | :--- | :--- |
| **1. Find Email** | Enter the name/domain into the search bar. | [Apollo.io](https://apollo.io) (Free Tier) |
| **2. Verify** | Check if the email is active (Green checkmark). | [Hunter.io](https://hunter.io) (Free Tier) |
| **3. Professional Context** | View their LinkedIn and find one "Non-Generic" detail to mention. | LinkedIn |

---

## Example "Sniper" Log (Tracking your 10)

| Company | Decision Maker | Pain Point Hypothesis | Hook Status |
| :--- | :--- | :--- | :--- |
| **EcoCharge** | Jane Doe (VP Eng) | Struggling with ISO 15118-20 security compliance for new chargers. | Email Sent |
| **PulseMed** | John Smith (CTO) | Manual validation of BLE stack is slowing down FDA submission. | LinkedIn Followed |

---

## Pro Tip: The "Job Board" Reverse-Search
Instead of searching for companies, search for **Job Postings** on LinkedIn or Indeed. If a company is hiring 3+ Firmware Engineers, they are in a "Scaling Crisis." That is your best moment to reach out with a "Force Multiplier" pitch.

```bash
gemini "Based on this job description [Paste Link/Text], what is the #1 technical challenge this team is trying to solve with this hire? Draft a short 'Consultative Hook' for the hiring manager."
```
