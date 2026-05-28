import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

# Setup Gemini with verified model 'gemini-flash-latest'
# Passing api_key explicitly to ensure it uses the GitHub Secret
gemini_llm = LLM(
    model="gemini/gemini-flash-latest",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    verbose=True
)

# Setup Tools
search_tool = SerperDevTool()

# 1. Define Agents
sourcer = Agent(
    role='Lead Sourcer',
    goal='Find 10 mid-sized IoT/Hardware companies (50-300 employees) in safety-critical sectors (MedTech, Automotive, Industrial).',
    backstory='Expert in market research and identifying high-growth hardware firms with legacy systems or scaling pains.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

analyst = Agent(
    role='Technical & OSINT Analyst',
    goal='Analyze company pain points AND find contact info (Name/Email) for VPs of Engineering and Heads of HR.',
    backstory='Senior Embedded Systems Architect and OSINT expert. You can identify engineering bottlenecks and find the exact decision-makers (Engineering & HR) to solve them.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Outreach Copywriter',
    goal='Draft highly personalized, technical emails to VPs of Engineering and HR leads based on pain points.',
    backstory='Expert in consultative selling for high-ticket engineering services. Known for extreme personalization, technical credibility, and multi-threaded outreach.',
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# 2. Define Tasks
processed_file = "processed_companies.txt"
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        already_processed = [line.strip() for line in f.readlines() if line.strip()]
else:
    already_processed = []

exclude_list = ", ".join(already_processed) if already_processed else "None"

source_task = Task(
    description=f'Find 10 NEW companies meeting the criteria in the IoT/Embedded space. Do NOT include any of these already processed companies: {exclude_list}. Focus on those with products in market for 5+ years or hiring firmware leads.',
    expected_output='A list of 10 companies with their website, size, and primary product.',
    agent=sourcer
)

analysis_task = Task(
    description='''For each of the 10 companies identified:
1. Hypothesize a specific technical pain point related to safety, reliability, or AI-native modernization.
2. Find the name and professional email of the VP of Engineering or CTO.
3. Find the name and professional email of the Head of HR or Talent Acquisition.
If the exact email is not found, use common company patterns (e.g., first.last@company.com) and mark as "Predicted".''',
    expected_output='A report containing 10 company profiles, each with a "Pain Point Hypothesis", "VP Engineering Name & Email", and "HR Lead Name & Email".',
    agent=analyst,
    context=[source_task]
)

write_task = Task(
    description='''Write two personalized outreach emails for each company:
1. A technical email to the VP of Engineering using the "Technical Audit Map" template.
2. A culture/hiring focused email to the HR Lead about scaling their engineering team safely.
Include the recipient's name and email clearly at the top of each email.''',
    expected_output='A markdown file containing 20 personalized emails (2 per company) with clear recipient details.',
    agent=writer,
    context=[analysis_task]
)

# 3. Form the Crew
crew = Crew(
    agents=[sourcer, analyst, writer],
    tasks=[source_task, analysis_task, write_task],
    process=Process.sequential,
    verbose=True
)

# 4. Execute and Save
result = crew.kickoff()

# Extract company names for tracking
date_str = datetime.now().strftime("%Y-%m-%d")
output_file = f"daily_hits_{date_str}.md"

with open(output_file, 'w') as f:
    f.write(f"# Daily Sniper Hits - {date_str}\n\n")
    f.write(str(result))

# Update processed companies list
extractor_agent = Agent(
    role='Data Cleaner',
    goal='Extract exactly the 10 company names from the report.',
    backstory='Precision-focused data entry specialist.',
    llm=gemini_llm
)

extract_task = Task(
    description='Extract ONLY the 10 company names from the following report. Return them as a simple newline-separated list. No numbering, no bullets.',
    expected_output='A simple list of 10 company names, one per line.',
    agent=extractor_agent,
    context=[source_task] # Using source_task context as it's cleaner for names
)

cleanup_crew = Crew(agents=[extractor_agent], tasks=[extract_task])
new_companies_result = cleanup_crew.kickoff()

# Convert result to string and clean it
new_companies_list = str(new_companies_result).strip().split('\n')

with open(processed_file, "a") as f:
    for company in new_companies_list:
        if company.strip():
            f.write(company.strip() + "\n")

print(f"Done! Results saved to {output_file} and {processed_file} updated.")
