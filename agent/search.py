import os
from datetime import datetime
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_transfer_news(team: str) -> list[dict]:
    today = datetime.now().strftime("%B %d %Y")
    
    results = []
    
    queries = [
        f"Fabrizio Romano {team} transfer {today}",
        f"David Ornstein {team} transfer {today}",
        f"{team} transfer news June 2026"
    ]
    
    for query in queries:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=4,
            days=7
        )
        results.extend(response["results"])
    
    seen = set()
    unique_results = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique_results.append(r)
    
    return unique_results