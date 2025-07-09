from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from crewai_tools import SerperDevTool
from tools import BloodTestReportTool

# Tools initialization
search_tool = SerperDevTool()
blood_report_tool = BloodTestReportTool()

# Verification task
verification_task = Task(
    description="Verify the validity of the blood test report at {file_path}",
    expected_output="Verification report confirming document validity and extracting key blood test parameters",
    agent=verifier,
    tools=[blood_report_tool]
)

# Nutrition analysis task
nutrition_analysis = Task(
    description=(
        "Analyze blood test results at {file_path} "
        "and create personalized nutrition recommendations based on the findings"
    ),
    expected_output="Detailed nutrition plan with dietary recommendations based on blood test results",
    agent=nutritionist,
    tools=[blood_report_tool]
)

# Exercise planning task
exercise_planning = Task(
    description=(
        "Develop a safe exercise plan based on blood test results at {file_path} "
        "considering any health conditions or abnormal values found"
    ),
    expected_output="Personalized exercise routine with intensity guidelines based on health status",
    agent=exercise_specialist,
    tools=[blood_report_tool]
)

# Main task that will coordinate everything (no tools needed as manager delegates)
help_patients = Task(
    description=(
        "Coordinate the analysis of the blood test report located at {file_path} "
        "to address the patient's query: {query}. "
        "Synthesize findings from verification, nutrition, and exercise specialists "
        "to provide comprehensive health analysis and recommendations."
    ),
    expected_output=(
        "Complete medical report including:\n"
        "1. Summary of blood test findings\n"
        "2. Potential health concerns and abnormal values\n"
        "3. Recommended next steps and follow-up\n"
        "4. Personalized nutrition recommendations\n"
        "5. Safe exercise guidelines\n"
        "6. Overall health assessment and action plan"
    ),
    agent=doctor
)