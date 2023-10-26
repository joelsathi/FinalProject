from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="db", embedding_function=embeddings)

def search_similarity(query):
    
    print("Similarity search started...")
    docs = vectordb.similarity_search(query)
    print("Similarity search done...")

    context = ""

    for chunk in docs:
        context += chunk.page_content + "\n"

    return context