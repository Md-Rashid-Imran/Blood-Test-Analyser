import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from crewai_tools import SerperDevTool
from tools import BloodTestReportTool

## os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
## os.environ["OPENAI_MODEL_NAME"]="gpt-4o-mini"

from crewai import LLM

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=os.getenv("GEMINI_API_KEY")
)

# Tools initialization - Create instances of the tools
search_tool = SerperDevTool()
blood_report_tool = BloodTestReportTool()

# Manager agent should NOT have tools in hierarchical process
doctor = Agent(
    role="Senior Medical Doctor",
    goal="Analyze blood test reports and provide medical insights",
    verbose=True,
    memory=True,
    backstory=(
        "You're an experienced medical doctor specialized in interpreting blood test reports. "
        "You provide accurate and professional medical advice based on lab results. "
        "You coordinate with other specialists to provide comprehensive health analysis."
    ),
    # Remove tools from manager agent
    tools=[blood_report_tool],  # Add this line
    llm=llm,
    allow_delegation=True
)

verifier = Agent(
    role="Report Verifier",
    goal="Validate blood test reports",
    verbose=True,
    memory=True,
    backstory=(
        "You specialize in verifying medical reports and ensuring their validity "
        "for accurate diagnosis."
    ),
    tools=[blood_report_tool],
    llm=llm
)

nutritionist = Agent(
    role="Nutrition Specialist",
    goal="Provide dietary recommendations based on blood test results",
    verbose=True,
    memory=True,
    backstory=(
        "You're a certified nutritionist with expertise in creating "
        "personalized diet plans based on medical reports."
    ),
    tools=[blood_report_tool],
    llm=llm
)

exercise_specialist = Agent(
    role="Fitness Expert",
    goal="Develop exercise plans based on health conditions",
    verbose=True,
    memory=True,
    backstory=(
        "You're a fitness specialist with medical knowledge who creates "
        "safe exercise routines tailored to individual health status."
    ),
    llm=llm,
    tools=[blood_report_tool]
)