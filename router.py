from generation import generate_query

def route_query(query: str):
    SYSTEM_PROMPT = """
You're an agent who is going to analyse the user query and decide which tools to select based on user query.

return 'vector_db_query' if the user is asking about "Rizvi International Impex" or its services, history, Contact info, or anything related to Rizvis company.
return 'web_search' if the user is asking you to search the web or asking about a DIFFERENT/EXTERNAL company (e.g., providing a URL).
return 'weather_api_call' if you find that user is asking about weather.

INSTRUCTIONS: please provide me single word responses for return I mentioned above. 
For example, if you find user is talking about weather so please return 'weather_api_call'
For example, if the query is "tell me about rizvi's international impex", return 'vector_db_query'
"""

    response = generate_query(query, SYSTEM_PROMPT)
    return response.strip()

if __name__ == "__main__":
    print(route_query("how old is sabrina carpenter"))
