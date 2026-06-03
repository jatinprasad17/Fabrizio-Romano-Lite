from graph import build_graph

app = build_graph()

result = app.invoke({"team": "Manchester City"})

print("FILTERED ARTICLES COUNT:", len(result["filtered_articles"]))
print("\n--- FINAL ANALYSIS ---\n")
print(result["analysis"])