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
    role='Technical Analyst',
    goal='Analyze company product lines and job descriptions to identify specific technical "Pain Points" like legacy debt or compliance hurdles.',
    backstory='Senior Embedded Systems Architect who can read between the lines of job postings and product manuals to find engineering bottlenecks.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Outreach Copywriter',
    goal='Draft highly personalized, technical emails to VPs of Engineering based on the analyzed pain points.',
    backstory='Expert in consultative selling for high-ticket engineering services. Known for extreme personalization and technical credibility.',
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# 2. Define Tasks
processed_file = "processed_companies.txt"
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        already_processed = f.read().splitlines()
else:
    already_processed = []

exclude_list = ", ".join(already_processed) if already_processed else "None"

source_task = Task(
    description=f'Find 10 NEW companies meeting the criteria in the IoT/Embedded space. Do NOT include any of these already processed companies: {exclude_list}. Focus on those with products in market for 5+ years or hiring firmware leads.',
    expected_output='A list of 10 companies with their website, size, and primary product.',
    agent=sourcer
)

analysis_task = Task(
    description='For each of the 10 companies, hypothesize a specific technical pain point related to safety, reliability, or AI-native modernization.',
    expected_output='A report containing 10 company profiles, each with a "Pain Point Hypothesis" and the name of the VP of Engineering or CTO.',
    agent=analyst,
    context=[source_task]
)

write_task = Task(
    description='Write a personalized outreach email for each company using the "Technical Audit Map" template. Ensure it mentions the specific pain point.',
    expected_output='A markdown file containing 10 personalized emails ready to be reviewed and sent.',
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

# Extract company names for tracking (assuming they are in the result)
# We'll use a simple heuristic or ask the agent to format them clearly
date_str = datetime.now().strftime("%Y-%m-%d")
output_file = f"daily_hits_{date_str}.md"

with open(output_file, 'w') as f:
    f.write(f"# Daily Sniper Hits - {date_str}\n\n")
    f.write(str(result))

# Update processed companies list
# Since we want to be safe, we'll ask the LLM to extract the names specifically
extractor_agent = Agent(
    role='Data Cleaner',
    goal='Extract exactly 10 company names from the provided text.',
    backstory='Precision-focused data entry specialist.',
    llm=gemini_llm
)

extract_task = Task(
    description='Extract only the company names from the following report. Return them as a simple newline-separated list.',
    expected_output='A list of 10 company names, one per line.',
    agent=extractor_agent,
    context=[write_task]
)

cleanup_crew = Crew(agents=[extractor_agent], tasks=[extract_task])
new_companies = cleanup_crew.kickoff()

with open(processed_file, "a") as f:
    f.write("\n" + str(new_companies))

print(f"Done! Results saved to {output_file} and {processed_file} updated.")
