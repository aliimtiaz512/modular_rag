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
    elif "vector_db_query" in route_cleaned:
        context, distance = vector_db(query)
        
        confidence_score = max(0.0, 100.0 * (1.0 - (distance / 2.0)))
        
        if confidence_score < 40.0:
            msg = "I am sorry, I am agent of Rizvi's International Impex. Kindly question me about them."
            add_to_memory(query, msg)
            return msg
        
    memory_context = get_memory_context()
        
    prompt = f"""
{memory_context}

CONTEXT: {context}

QUERY: {query}

INSTRUCTIONS: You are a helpful answering assistant. Use the provided CONTEXT to answer the user's QUERY accurately in concise and too the point manner.Generate the response in a single paragraph.Don't add pre texts like "According to my context etc". If the user's query has already been answered previously in the 'Previous Conversation Context',don't mention text like that it is answered previously. If you cannot answer it based on the CONTEXT, state that you do not have enough information.
"""

    response = generate_query(query, prompt)
    add_to_memory(query, response)
    
    return response

