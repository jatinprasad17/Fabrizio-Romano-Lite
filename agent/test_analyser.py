from search import search_transfer_news
from analyser import analyse_news

articles = search_transfer_news("Manchester City")
result = analyse_news("Manchester City", articles)
print(result["analysis"])