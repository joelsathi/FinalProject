from ...VectorDB_chat.access_db import search_similarity

query = "Give contact number of your bank"
docs = search_similarity(query)
print(docs)