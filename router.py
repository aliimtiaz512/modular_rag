from generation import generate_query

def route_query(query: str):
    SYSTEM_PROMPT = """
You're an agent who is going to analyse the user query and decide which tools to select based on user query.
- Return 'web_search' ONLY IF the user provides a specific URL or explicitly asks to search an external web address.
- Return 'vector_db_query' for ALL OTHER queries, including questions about the company, products, general greetings, or ambiguous questions related to rizvi's.

INSTRUCTIONS: Please provide me single word responses for return I mentioned above. For example, if you find user is asking a general question related to rizvi's, return 'vector_db_query'.
"""

    response = generate_query(query, SYSTEM_PROMPT)
    return response.strip()
