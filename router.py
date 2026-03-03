from generation import generate_query

def route_query(query: str):
    SYSTEM_PROMPT = """
You're an agent who is going to analyse the user query and decide which tools to select based on user query
return 'web_search' if you analyse the query and user is asking related to some other website or url
return 'vector_db_query' if you find that user want's you to search from the provided context in the database

INSTRUCTIONS: Please provide me single word responses for return I mentioned above For example, if you find user is talking about rizviz then you will return 'vector_db_query'
"""

    response = generate_query(query, SYSTEM_PROMPT)
    return response.strip()
