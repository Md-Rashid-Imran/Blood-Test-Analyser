# Blood Test Report Analyzer

A fun and functional AI-powered web app that analyzes blood test reports using LLM agents. Upload a PDF report, ask any health-related question (or not), and get a dramatic AI response — diagnosis, nutrition advice, workout suggestions, and verification. Completely over-the-top and occasionally helpful.

---

## Bugs and Fixes

# agents.py:
1 Bug/Issue - from crewai.agents import Agent
  Explanation - Agent is not found in crewai.agents in latest versions
  Fix Applied - Changed to from crewai import Agent
2 Bug/Issue - llm = llm	
  Explanation - Variable llm is used before definition (NameError)
  Fix Applied - Defined a proper llm using LLM() class
3 Bug/Issue - No LLM() initialization
  Explanation - Missing LLM model config and API setup
  Fix Applied - Added proper LLM(...) from crewai and set environment variable
4 Bug/Issue - tools=[BloodTestReportTool().read_data_tool]
  Explanation - Improper tool usage (calls async method instead of assigning tool instance)	
  Fix Applied - Refactored BloodTestReportTool to class-based and passed instance directly
5 Bug/Issue - Doctor agent had tools even though it’s a manager
  Explanation -	In hierarchical processes, manager agents should not have tools
  Fix Applied -	Moved tools assignment to only worker agents
6 Bug/Issue - search_tool was imported but unused
  Explanation -	Unnecessary import clutter
  Fix Applied -	Removed or assigned properly only if needed
7 Bug/Issue - memory=True inconsistently set
  Explanation -	Not all agents had memory=True
  Fix Applied -	Ensured consistent use of memory=True
8 Bug/Issue - Missing tools in nutritionist and exercise_specialist
  Explanation -	Tasks fail because agents lack access to required tools
  Fix Applied -	Added tools=[blood_report_tool]

# tools.py:
1 Bug/Issue - Used async def for tool
  Explanation -	CrewAI tools expect a sync .run() or _run() method
  Fix Applied -	Replaced with _run() in BaseTool class
2 Bug/Issue - No schema for tool inputs
  Explanation -	No validation or structure for input args
  Fix Applied -	Introduced BloodTestReportInput with pydantic
3 Bug/Issue - Not subclassing BaseTool
  Explanation -	Tool wouldn't be recognized by CrewAI
  Fix Applied -	Refactored to subclass BaseTool
4 Bug/Issue - Hardcoded default path
  Explanation -	Inflexible for actual usage
  Fix Applied -	Made file_path required argument
5 Bug/Issue - Deprecated PyPDFLoader import
  Explanation -	Causes warning
  Fix Applied -	Updated to langchain_community loader
6 Bug/Issue - No output length control
  Explanation -	Could crash with large PDFs
  Fix Applied -	Added truncation at 10,000 characters
7 Bug/Issue - No error handling
  Explanation -	Crashed on corrupted or missing PDF
  Fix Applied - Added try/except with error message
8 Bug/Issue - Inefficient string cleanup
  Explanation -	Used loops for cleaning
  Fix Applied -	Replaced with re.sub() for newline/header cleanup

# task.py:
1 Bug/Issue - All tasks assigned to doctor
  Explanation - Even nutrition, exercise, verification tasks
  Fix Applied - Assigned to correct agents
2 Bug/Issue - Used tool as static method
  Explanation - read_data_tool was not compatible with tools=[]
  Fix Applied - Passed actual BaseTool instance
3 Bug/Issue - Manager agent had tools
  Explanation - Not ideal in hierarchical logic
  Fix Applied -	Removed tools from help_patients
4 Bug/Issue - search_tool was unused
  Explanation - Cluttered the imports
  Fix Applied -	Removed
5 Bug/Issue - async_execution=False used
  Explanation - Deprecated or unnecessary
  Fix Applied -	Removed this argument
6 Bug/Issue - Missing {path} input reference
  Explanation - Tasks lacked context of file path
  Fix Applied -	Added (file path: {path}) to description
7 Bug/Issue - Task named verification (bad name)
  Explanation -Could collide with Python's ideas of validation
  Fix Applied -	Renamed to verification_task

# main.py:
1 Bug/Issue - Only one agent/task used
  Explanation -	Limited functionality
  Fix Applied -	Added 4 agents and 4 tasks
2 Bug/Issue - Used blocking kickoff()
  Explanation -	Not compatible with async FastAPI
  Fix Applied - Switched to await kickoff_async(...)
3 Bug/Issue - No CORS middleware
  Explanation -	Frontend failed due to browser policy
  Fix Applied -	Added CORSMiddleware with wildcard
4 Bug/Issue - Debug info missing
  Explanation -	No visibility during execution
  Fix Applied -	Added print() debug logs
5 Bug/Issue - Traceback hidden
  Explanation -	Errors were vague
  Fix Applied - Used traceback.print_exc()
6 Bug/Issue - Default query was "Summarise"
  Explanation - Inconsistent spelling with frontend
  Fix Applied - Changed to "Summarize"
7 Bug/Issue - Included uvicorn.run(...)
  Explanation - Not needed when running via CLI
  Fix Applied - Removed from script bottom

---

## Features

-  Upload blood test reports in **PDF format**
-  Analyze with **CrewAI agents**: doctor, verifier, nutritionist, fitness coach
-  Results include:
  - Made-up but medically-sounding insights
  - Nutritional recommendations
  - Workout suggestions (even if you're sick!)
  - Report verification (even if it’s not a report)
-  Built with **FastAPI**, **LangChain**, and **CrewAI**
-  Beautiful responsive frontend (HTML + JS)

---

## Project Structure

```
├── agents.py              # Agent roles (Doctor, Verifier, etc.)
├── task.py                # CrewAI tasks for each agent
├── tools.py               # PDF reader, nutrition, and exercise logic
├── main.py                # FastAPI backend server
├── requirements.txt       # Python dependencies
├── data/                  # Temporary file storage
└── .env                   # Contains your Gemini API key (not committed)
```

---

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/Md-Rashid-Imran/Blood-Test-Analyser.git
cd blood-test-analyzer
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your `.env` file
Create a `.env` file in the root with:
```
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Running the App

### Start the FastAPI server:
```bash
uvicorn main:app --reload
```


---

## Sample Agent Roles

- **Doctor**: Overconfident, possibly hallucinating diagnoses
- **Verifier**: Approves anything as a medical document
- **Nutritionist**: Pushes supplements and superfoods
- **Fitness Coach**: Demands extreme workouts for all

---

## Tech Stack

- **Python 3.11+**
- [FastAPI](https://fastapi.tiangolo.com/)
- [CrewAI](https://github.com/joaomdmoura/crewai)
- [LangChain](https://www.langchain.com/)
- [Gemini API](https://aistudio.google.com/)

---

## API Documentation

### `GET /`

**Purpose:** Health check endpoint to confirm the API is running.

**Response:**
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

---

### `POST /analyze`

**Purpose:** Upload a blood test report (PDF) and receive a multi-agent AI-powered analysis.

#### Request

- **Method:** `POST`
- **Endpoint:** `/analyze`
- **Content-Type:** `multipart/form-data`

| Field  | Type        | Required | Description                                    |
|--------|-------------|----------|------------------------------------------------|
| file   | File (.pdf) | ✅       | The blood test report in PDF format           |
| query  | string      | ❌       | (Optional) User query like "Is my iron low?"  |

#### Example `curl` Command:
```bash
curl -X POST http://localhost:8000/analyze \
  -F "file=@data/sample.pdf" \
  -F "query=Summarize my blood test"
```

#### Response (Success):
```json
{
  "status": "success",
  "query": "Summarize my blood test",
  "analysis": "<multi-agent analysis result here>",
  "file_processed": "sample.pdf"
}
```

#### Response (Error):
```json
{
  "detail": "Error processing blood report: <error details>"
}
```

---

### CORS

> Cross-Origin Resource Sharing (CORS) is **enabled** for all origins, so the API works with any web frontend.

---

## Disclaimer

This project is **for educational/fun purposes only**. It **does not provide real medical advice** and should not be used for actual diagnostics.