import os
import re
import json
from datetime import datetime

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

# ---------------------------
# LLM CONFIG
# ---------------------------

gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

groq_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)


def get_llm():
    return gemini_llm


# ---------------------------
# SAFE LLM INVOCATION
# ---------------------------

def invoke_with_fallback(prompt: str) -> str:

    # Gemini
    try:
        response = gemini_llm.invoke(
            [HumanMessage(content=prompt)]
        )

        return response.content

    except Exception as gemini_error:

        print(
            f"Gemini failed: {gemini_error} — switching to Groq!"
        )

        # Groq fallback
        try:
            response = groq_llm.invoke(
                [HumanMessage(content=prompt)]
            )

            return response.content

        except Exception as groq_error:

            print(
                f"Groq failed: {groq_error}"
            )

            return json.dumps({
                "transfers": [],
                "summary": "LLM unavailable",
                "overall_score": 0
            })


# ---------------------------
# FILTER ARTICLES
# ---------------------------

def filter_articles(team: str, articles: list[dict]) -> list[dict]:

    articles_text = ""

    for i, article in enumerate(articles):
        articles_text += (
            f"{i + 1}. {article.get('title', '')}\n"
            f"{article.get('content', '')[:800]}\n\n"
        )

    prompt = f"""
You are a football transfer news filter.

Team: {team}

Articles:
{articles_text}

Return ONLY the article numbers where {team}
is directly involved in a transfer.

Include:
- buying player
- selling player
- contract extension
- loan deals
- player currently belongs to {team}

Return format:
1,3,5

Nothing else.
"""

    try:

        content = invoke_with_fallback(prompt)

        indices = []

        for x in content.split(","):
            x = x.strip()

            if x.isdigit():
                indices.append(int(x) - 1)

        filtered = [
            articles[i]
            for i in indices
            if 0 <= i < len(articles)
        ]

        if filtered:
            return filtered

        return articles

    except Exception as e:

        print(f"Filter error: {e}")

        return articles


# ---------------------------
# ANALYSE NEWS
# ---------------------------

def analyse_news(team: str, articles: list[dict]) -> dict:

    articles_text = ""

    for i, article in enumerate(articles):

        articles_text += (
            f"{i + 1}. {article.get('title', '')}\n"
            f"{article.get('url', '')}\n"
            f"{article.get('content', '')[:250]}\n\n"
        )

    current_month = datetime.now().strftime("%B %Y")
    current_year = datetime.now().year

    prompt = f"""
You are a football transfer analyst.

Team: {team}

Today:
{datetime.now().strftime("%B %d, %Y")}

Articles:
{articles_text}

STRICT RULES:
- ONLY include transfers where {team} is DIRECTLY involved
- ONLY include news from {current_month} — IGNORE anything older
- If player name is not clearly mentioned, SKIP that transfer completely
- Never write "Unnamed player" or "Unknown player" — skip instead
- Confirmed transfers = minimum score 8
- Robertson/Konate already left — SKIP completed old transfers
- Pick TOP 10 most reliable CURRENT transfers only
- Sort by reliability score descending
- "unknown" destination write "Free Agent" instead

Return ONLY valid JSON.

{{
  "transfers": [
    {{
      "player": "Player Name",
      "from": "Club",
      "to": "Club",
      "type": "Confirmed/Rumour/Contract",
      "detail": "Short detail",
      "score": 8
    }}
  ],
  "summary": "2-3 lines",
  "overall_score": 7
}}
"""

    try:

        content = invoke_with_fallback(prompt)

        # Extract JSON block if model adds junk
        match = re.search(
            r"\{[\s\S]*\}",
            content
        )

        if match:

            try:

                parsed_json = json.loads(
                    match.group()
                )

                return {
                    "team": team,
                    "analysis": parsed_json
                }

            except Exception as json_error:

                print(
                    f"JSON Parse Error: {json_error}"
                )

        return {
            "team": team,
            "analysis": {
                "transfers": [],
                "summary": str(content),
                "overall_score": 0
            }
        }

    except Exception as e:

        print(f"Analysis error: {e}")

        return {
            "team": team,
            "analysis": {
                "transfers": [],
                "summary": f"Analysis failed: {str(e)}",
                "overall_score": 0
            }
        }