import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

def analyse_news(team: str, articles: list[dict]) -> dict:
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"{i+1}. {article['title']}\n{article['url']}\n{article.get('content', '')[:3000]}\n\n"

        prompt = f"""
    You are a football transfer news analyst.

    Team: {team}
    Articles:
    {articles_text}

    STRICT RULES:
    - ONLY include transfers where {team} is DIRECTLY involved
    - Pick TOP 10 most reliable/important transfers only
    - Sort by reliability score descending
    - Skip minor youth/loan moves unless highly reliable

    CRITICAL: Return ONLY raw JSON. No explanation. No preamble. No markdown. No backticks. Just the JSON object starting with {{ and ending with }}.
    {{
        "transfers": [
            {{
                "player": "Player Name",
                "from": "Club Name",
                "to": "Club Name",
                "type": "Confirmed/Rumour/Contract",
                "detail": "One line detail",
                "score": 8
            }}
        ],
        "summary": "2-3 line overall summary",
        "overall_score": 7
    }}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        import json
        clean = response.content.strip().replace("```json", "").replace("```", "")
        return {"team": team, "analysis": json.loads(clean)}
    except:
        return {"team": team, "analysis": response.content}

def filter_articles(team: str, articles: list[dict]) -> list[dict]:
    articles_text = ""
    for i, article in enumerate(articles):
        articles_text += f"{i+1}. {article['title']}\n{article.get('content', '')[:1000]}\n\n"

        prompt = f"""
    You are a football news filter.

    Team: {team}
    Articles:
    {articles_text}

    Return ONLY the numbers (e.g. 1,3,5,7) of articles where {team} is DIRECTLY involved in a transfer — as buyer, seller, or the player plays for {team}.

    Return just the numbers separated by commas, nothing else.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    
    try:
        indices = [int(x.strip()) - 1 for x in response.content.strip().split(",")]
        filtered = [articles[i] for i in indices if 0 <= i < len(articles)]
    except:
        filtered = articles

    return filtered