from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.parser import parse_resume
from app.schemas import ParseResult

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/healthz/")
def healthz():
    return {"status": "ok"}

@app.post("/parse-resume/", response_model=ParseResult)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    return parse_resume(file)
