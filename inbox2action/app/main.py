from fastapi import FastAPI
from pydantic import BaseModel
from app.email_agent import process_email_agent


app = FastAPI()

class EmailInput(BaseModel):
    email_text: str

@app.post("/process-email")
def process_email(email: EmailInput):
    result = process_email_agent(email.email_text)
    return {"status": "success", "result": result}
