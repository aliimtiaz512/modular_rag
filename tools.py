from extraction import extract_from_website
from ingestion import collection

def web_search(url: str):
    """Extracts text from the provided URL."""
    return extract_from_website(url)

def vector_db(query: str):
    """Queries the chromaDB collection for context."""
    try:
        results = collection.query(query_texts=[query], n_results=1)
        if results and 'documents' in results and len(results['documents']) > 0:
            # results['documents'] is a list of lists e.g., [['doc1', 'doc2']]
            docs = results['documents'][0]
            if isinstance(docs, list) and len(docs) > 0:
                return docs[0]
            elif isinstance(docs, str):
                return docs
    except Exception as e:
        print(f"Error querying vector DB: {e}")
    return ""
