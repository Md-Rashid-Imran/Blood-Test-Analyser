from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, verification_task, nutrition_analysis, exercise_planning

app = FastAPI(title="Blood Test Report Analyser")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

async def run_crew(query: str, file_path: str):
    """Run the crew asynchronously"""
    medical_crew = Crew(
        agents=[doctor, verifier, nutritionist, exercise_specialist],
        tasks=[help_patients, verification_task, nutrition_analysis, exercise_planning],
        process=Process.sequential,  # Changed from hierarchical
        verbose=True
    )
    
    result = await medical_crew.kickoff_async(inputs={'query': query, 'path': file_path})
    return result

@app.get("/")
async def root():
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarize my Blood Test Report")
):
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    print(f"Received file: {file.filename}")  # Debug log
    print(f"Query: {query}")  # Debug log
    
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"File saved to: {file_path}")  # Debug log
        
        if not query.strip():
            query = "Summarize my Blood Test Report"
        
        print("Starting crew analysis...")  # Debug log
        response = await run_crew(query=query.strip(), file_path=file_path)
        print("Crew analysis completed")  # Debug log
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug log
        print(f"Error type: {type(e)}")  # Debug log
        import traceback
        traceback.print_exc()  # Print full traceback
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")  # Debug log
            except:
                pass

# Remove the uvicorn run from here to avoid the warning
# Run the server using: uvicorn main:app --host 0.0.0.0 --port 8000 --reload