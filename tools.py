from extraction import extract_with_langchain
from ingestion import collection

def web_search(url: str):
    return extract_with_langchain(url)

def vector_db(query: str):
    try:
        results = collection.query(query_texts=[query], n_results=1)
        if results and 'documents' in results and len(results['documents']) > 0:
            docs = results['documents'][0]
            distances = results['distances'][0] if 'distances' in results and results['distances'] else [2.0]
            
            doc = docs[0] if isinstance(docs, list) and len(docs) > 0 else docs if isinstance(docs, str) else ""
            dist = distances[0] if isinstance(distances, list) and len(distances) > 0 else distances if isinstance(distances, (int, float)) else 2.0
            
            return doc, dist
    except Exception as e:
        print(f"Error querying vector DB: {e}")
        
    return "", 2.0  