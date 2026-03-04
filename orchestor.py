import re
from generation import generate_query
from router import route_query
from tools import web_search, vector_db
from memory import add_to_memory, get_memory_context, check_if_asked

def extract_urls(text):
    url_pattern = re.compile(r'(https?://[^\s]+)')
    return url_pattern.findall(text)

def orchestrate_query(query: str):
    if check_if_asked(query):
        return "I have already answered this question earlier."
        
    route = route_query(query)
    route_cleaned = route.strip()
    
    context = ""
    
    if "web_search" in route_cleaned:
        urls = extract_urls(query)
        if urls:
            url = urls[0]
            context = web_search(url)
        else:
            return "I am sorry, but I am Rizvi's assistant so I did not answer your question. This is out of my context. Please ask something related to Rizvi's website or information."
    elif "vector_db_query" in route_cleaned:
        context = vector_db(query)
        
    memory_context = get_memory_context()
        
    prompt = f"""
{memory_context}

CONTEXT: {context}

QUERY: {query}

INSTRUCTIONS: You are a helpful and concise assistant. Your goal is to provide direct answers based on the CONTEXT. You must limit your entire response to a maximum of 4 to 5 sentences. Regardless of how many separate questions the user asks in a single QUERY, ensure you address all of them together within this strict sentence limit. Do not use line breaks or bullet points.
"""

    response = generate_query(query, prompt)
    add_to_memory(query, response)
    
    return response

