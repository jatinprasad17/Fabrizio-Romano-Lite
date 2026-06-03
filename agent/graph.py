import os
from typing import TypedDict
from langgraph.graph import StateGraph,END
from search import search_transfer_news
from analyser import analyse_news,filter_articles
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    team:str
    raw_articles:list[dict]
    filtered_articles:list[dict]
    analysis:str

def search_node(state:AgentState)->AgentState:
    articles = search_transfer_news(state["team"])
    return {**state,"raw_articles":articles}

def filter_node(state: AgentState) -> AgentState:
    filtered = filter_articles(state["team"], state["raw_articles"])
    return {**state, "filtered_articles": filtered}

def analyse_node(state: AgentState) -> AgentState:
    result = analyse_news(state["team"], state["filtered_articles"])
    return {**state, "analysis": result["analysis"]}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("search",search_node)
    graph.add_node("filter",filter_node)
    graph.add_node("analyse",analyse_node)

    graph.set_entry_point("search")
    graph.add_edge("search","filter")
    graph.add_edge("filter", "analyse")
    graph.add_edge("analyse", END)

    return graph.compile()

        
