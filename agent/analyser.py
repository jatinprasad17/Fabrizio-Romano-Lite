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
    You are a football transfer news analyst. Be extremely strict.

    Team: {team}
    Articles:
    {articles_text}

    STRICT RULES:
    - ONLY include transfers where {team} is DIRECTLY involved as buyer, seller, or the player currently plays for {team}
    - If {team} is only mentioned in passing in another club's transfer story, IGNORE IT completely
    - Do not include transfers from other clubs unless {team} is directly linked
    - For From → To: if destination unknown write "Exit/Free Agent" not "Unknown"
    - If source club unknown write "Incoming" not "Unknown"  
    - Always mention fee if available

    Give me:
    1. ALL TRANSFERS & RUMOURS (every single one where {team} is directly involved)
    - For each: Player name, From → To, Type (Rumour/Confirmed/Contract), Details, Reliability Score (1-10)
    - Reliability guide: Romano/Ornstein source = high, random blog = low, multiple sources = higher
    2. OVERALL RELIABILITY SCORE (1-10)
    3. SUMMARY (3-4 lines, only about {team})
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "team": team,
        "analysis": response.content
    }

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