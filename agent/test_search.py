from search import search_transfer_news

results = search_transfer_news("Manchester City")
for r in results:
    print(r["title"])
    print(r["url"])
    print("---")