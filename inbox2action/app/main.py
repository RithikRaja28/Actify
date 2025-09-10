from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.auth import get_current_user
from app.email_agent import process_email_agent

app = FastAPI()

class EmailInput(BaseModel):
    email_text: str

@app.post("/process-email")
def process_email(email: EmailInput, user=Depends(get_current_user)):
    result = process_email_agent(email.email_text)
    return {"status": "success", "result": result}
