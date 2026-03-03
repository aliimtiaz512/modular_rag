import re
from generation import generate_query
from router import route_query
from tools import web_search, vector_db

def extract_urls(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)

def orchestrate_query(query: str):
    route = route_query(query)
    route_cleaned = route.strip()
    
    context = ""
    
    if "web_search" in route_cleaned:
        urls = extract_urls(query)
        if urls:
            url = urls[0]
            context = web_search(url)
        else:
            return "Please provide a valid URL in your query for the web search."
    elif "vector_db_query" in route_cleaned:
        context = vector_db(query)
        
    prompt = f"""
CONTEXT: {context}

QUERY: {query}

INSTRUCTIONS: You are a helpful answering assistant. Use the provided context to answer the user's QUERY accurately. If you cannot answer it based on the CONTEXT, state that you do not have enough information.
"""

    response = generate_query(query, prompt)
    return response

