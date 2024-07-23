from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import PyPDF2
from transformers import pipeline

app = FastAPI()

# Initialize the Hugging Face pipeline
question_answerer = pipeline("question-answering")

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

class QueryRequest(BaseModel):
    query: str
    text: str

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    text = extract_text_from_pdf(file)
    return {"text": text}

@app.post("/query_pdf/")
async def query_pdf(request: QueryRequest):
    response = question_answerer(question=request.query, context=request.text)
    return JSONResponse(content={"response": response['answer']})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
