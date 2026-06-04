import sys
import os
sys.path.append(os.path.dirname(__file__))

from agent.graph import build_graph
from mailer.smtp import send_transfer_email
from database.supabase_client import get_all_subscribers

def run_for_all():
    subscribers = get_all_subscribers()
    
    if not subscribers:
        print("No subscribers found!")
        return
    
    app = build_graph()
    
    team_cache = {}
    
    for subscriber in subscribers:
        team = subscriber["team"]
        email = subscriber["email"]
        
        if team not in team_cache:
            print(f"Running agent for {team}...")
            result = app.invoke({"team": team})
            team_cache[team] = result["analysis"]
        
        send_transfer_email(
            to_email=email,
            team=team,
            analysis=team_cache[team]
        )
        print(f"Email sent to {email} for {team}!")

if __name__ == "__main__":
    run_for_all()