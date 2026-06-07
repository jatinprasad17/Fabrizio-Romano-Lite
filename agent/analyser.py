import os
import re
import json
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

def get_llm():
    return gemini_llm

def invoke_with_fallback(prompt: str) -> str:
    try:
        response = gemini_llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        print(f"Gemini failed: {e} — switching to Groq!")
        response = groq_llm.invoke([HumanMessage(content=prompt)])
        return response.content

def filter_articles(team: str, articles: list[dict]) -> list[dict]:
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"{i+1}. {article['title']}\n{article.get('content', '')[:300]}\n\n"

    prompt = f"""
You are a football news filter.

Team: {team}
Articles:
{articles_text}

Return ONLY the numbers (e.g. 1,3,5,7) of articles where {team} is DIRECTLY involved in a transfer — as buyer, seller, or the player plays for {team}.

Return just the numbers separated by commas, nothing else.
"""

    try:
        content = invoke_with_fallback(prompt)
        indices = [int(x.strip()) - 1 for x in content.strip().split(",")]
        filtered = [articles[i] for i in indices if 0 <= i < len(articles)]
    except:
        filtered = articles

    return filtered

def analyse_news(team: str, articles: list[dict]) -> dict:
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"{i+1}. {article['title']}\n{article['url']}\n{article.get('content', '')[:800]}\n\n"

    current_month = datetime.now().strftime("%B %Y")
    current_year = datetime.now().year

    prompt = f"""
You are a football transfer news analyst.

Team: {team}
Today: {datetime.now().strftime("%B %d, %Y")}
Articles:
{articles_text}

STRICT RULES:
- ONLY include transfers where {team} is DIRECTLY involved
- ONLY include news from {current_month} — IGNORE anything older
- If transfer happened before {current_year}, SKIP IT completely
- Pick TOP 10 most reliable/important CURRENT transfers only
- Sort by reliability score descending
- "unknown" ko "Free Agent" likho
- Reliability guide: Romano/Ornstein = high, multiple sources = higher, single blog = low

CRITICAL: Return ONLY raw JSON. No explanation. No preamble. No markdown. No backticks. Just JSON.

{{
    "transfers": [
        {{
            "player": "Player Name",
            "from": "Club",
            "to": "Club",
            "type": "Confirmed/Rumour/Contract",
            "detail": "One line detail",
            "score": 8
        }}
    ],
    "summary": "2-3 lines",
    "overall_score": 7
}}
"""

    try:
        content = invoke_with_fallback(prompt)
        match = re.search(r'\{{[\s\S]*\}}', content)
        if match:
            return {"team": team, "analysis": json.loads(match.group())}
        else:
            return {"team": team, "analysis": content}
    except Exception as e:
        print(f"Analysis error: {e}")
        return {"team": team, "analysis": content}