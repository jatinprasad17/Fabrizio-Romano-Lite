from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from database.supabase_client import add_subscriber, remove_subscriber, subscriber_exists, get_all_subscribers

app = FastAPI(title="Fabrizio Romano Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubscribeRequest(BaseModel):
    email: str
    team: str

@app.get("/")
def root():
    return {"status": "farzi romano API is running"}

@app.post("/subscribe")
def subscribe(req: SubscribeRequest):
    if subscriber_exists(req.email):
        raise HTTPException(status_code=409, detail="Email already subscribed")
    add_subscriber(req.email, req.team)
    return {"message": f"Subscribed successfully for {req.team}"}

@app.get("/subscriber/{email}")
def check_subscriber(email):
    exists = subscriber_exists(email)
    return {"exists": exists}

@app.delete("/unsubscribe/{email}")
def unsubscribe(email):
    if not subscriber_exists(email):
        raise HTTPException(status_code=404, detail="Email not found")
    remove_subscriber(email)
    return {"message": "Unsubscribed successfully"}

@app.get("/subscribers")
def list_subscribers():
    return get_all_subscribers()

@app.post("/run-agent")
def run_agent():
    from runner import run_for_all
    run_for_all()
    return {"message": "Agent run complete"}