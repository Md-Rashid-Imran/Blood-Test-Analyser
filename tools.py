import re
from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class BloodTestReportInput(BaseModel):
    """Input schema for BloodTestReportTool."""
    file_path: str = Field(..., description="Path to the blood test PDF file")

class BloodTestReportTool(BaseTool):
    name: str = "BloodTestReportTool"
    description: str = "Reads and returns content from a PDF blood test report."
    args_schema: Type[BaseModel] = BloodTestReportInput

    def _run(self, file_path: str) -> str:
        try:
            docs = PyPDFLoader(file_path=file_path).load()
            full_report = ""
            
            for data in docs:
                content = data.page_content
                # Remove redundant whitespace and headers
                content = re.sub(r'\n{3,}', '\n\n', content)  # Compress newlines
                content = re.sub(r'Report Status.*?Page \d+ of \d+', '', content, flags=re.DOTALL)
                full_report += content + "\n"
            
            return full_report[:10000]  # Limit to 10k characters
        except Exception as e:
            return f"Error reading PDF: {str(e)}"